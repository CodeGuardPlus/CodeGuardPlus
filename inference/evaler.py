import os
import re
import abc
import torch
import numpy as np
import subprocess

from inference.model import load_model
from inference.utils import try_parse, check_constraints

from transformers import PhrasalConstraint, LogitsProcessorList
from inference.logit_processors import NegativeConstraintNGramLogitsProcessor

class EvalerBase:
    def __init__(self, args):
        self.args = args
        self.load_model()

    def update_args(self, args):
        self.args = args

    @abc.abstractclassmethod
    def load_model(self):
        raise NotImplementedError()

    @abc.abstractclassmethod
    def sample(self, file_context, func_context, lang):
        raise NotImplementedError()

    def truncate(self, completion, lang):
        if lang == 'py':
            for match in re.finditer('\n', completion):
                cur_idx, next_idx = match.start(), match.end()
                if next_idx < len(completion) and not completion[next_idx].isspace():
                    completion = completion[:cur_idx]
                    break
            else:
                last_comment_str = '\n    #'
                if last_comment_str in completion:
                    completion = completion[:completion.rfind(last_comment_str)]
        elif lang == 'c' or lang == 'cpp':
            if '\n}' in completion:
                completion = completion[:completion.find('\n}')+2]
            else:
                last_comment_strs = ['\n    //', '\n    /*']
                for last_comment_str in last_comment_strs:
                    if last_comment_str in completion:
                        completion = completion[:completion.rfind(last_comment_str)]
                        completion = completion.rstrip() + '\n}'

            lines = completion.split('\n')
            final_lines = []
            for line in lines:
                if '->name = "' in line: continue
                final_lines.append(line)
            completion = '\n'.join(final_lines)
        else:
            raise NotImplementedError()

        return completion

    def process_completions(self, input_src, input_ids_len, gen_output, lang):
        tokens = gen_output[:, input_ids_len:, ...]
        completions = self.tokenizer.batch_decode(tokens)

        output_srcs = []
        dup_srcs, non_parsed_srcs = [], []
        full_output_srcs = []
        for i, completion in enumerate(completions):
            if self.tokenizer.eos_token in completion:
                completion = completion[:completion.find(self.tokenizer.eos_token)]
            completion = self.truncate(completion, lang)
            output_src = input_src + completion
            output_src = output_src.rstrip() + '\n'
            full_output_srcs.append(output_src)
            if output_src in output_srcs:
                dup_srcs.append(output_src)
            elif try_parse(output_src, lang) != 0:
                non_parsed_srcs.append(output_src)
            else:
                output_srcs.append(output_src)

        return output_srcs, non_parsed_srcs, full_output_srcs

class LMEvaler(EvalerBase):
    def __init__(self, args):
        super().__init__(args)

    def load_model(self):
        self.tokenizer, self.model, self.input_device = load_model('lm', self.args.model_dir, False, self.args)
        self.model.eval()

    def sample(self, file_context, func_context, lang):
        input_src = file_context + func_context
        input_ids = self.tokenizer(input_src, return_tensors='pt').input_ids.to(self.input_device)
        input_ids_len = input_ids.shape[1]
        if self.args.num_beams > 1:
            constraints = None
            if self.args.pos_constraints is not None:
                constraints = []
                for cons in self.args.pos_constraints:
                    constraints.append(
                        PhrasalConstraint(
                            self.tokenizer(cons, add_special_tokens=False).input_ids
                        )
                    )
            logits_processors = []
            if self.args.neg_constraints is not None:
                logits_processors = [NegativeConstraintNGramLogitsProcessor(
                    self.tokenizer(self.args.neg_constraints, add_special_tokens=False).input_ids,
                )]
            if not self.args.do_sample:
                print("Begin beam search")
                gen_output = self.model.generate(
                    input_ids,
                    num_beams=self.args.num_beams,
                    max_new_tokens=self.args.max_gen_len,
                    pad_token_id=self.tokenizer.pad_token_id,
                    use_cache=True,
                    constraints=constraints,
                    logits_processor=LogitsProcessorList(logits_processors),
                )
            else:
                print("Begin beam sampling")
                if self.args.pos_constraints is None and self.args.neg_constraints is None:
                    print("No constraints")
                    gen_output = self.model.generate(
                        input_ids,
                        do_sample=True,
                        num_return_sequences=self.args.num_gen,
                        num_beams=self.args.num_beams,
                        max_new_tokens=self.args.max_gen_len,
                        pad_token_id=self.tokenizer.pad_token_id,
                        use_cache=True,
                    )
                    return self.process_completions(input_src, input_ids_len, gen_output, lang)
                
                gen_output = []
                constrained = []
                for _ in range(self.args.max_num_gen // self.args.num_gen):
                    cur_gen_output = self.model.generate(
                        input_ids,
                        do_sample=True,
                        num_return_sequences=self.args.num_gen,
                        num_beams=self.args.num_beams,
                        max_new_tokens=self.args.max_gen_len,
                        pad_token_id=self.tokenizer.pad_token_id,
                        use_cache=True,
                        constraints=constraints,
                        logits_processor=LogitsProcessorList(logits_processors),
                    )

                    for output in cur_gen_output:
                        code = self.tokenizer.decode(output[input_ids_len:, ...])
                        if self.tokenizer.eos_token in code:
                            code = code[:code.find(self.tokenizer.eos_token)]
                        code = self.truncate(code, lang)
                        if check_constraints(code, self.args.pos_constraints, self.args.neg_constraints):
                            constrained.append(input_src + code)
                            if output.shape[0] < input_ids_len + self.args.max_gen_len:
                                output = torch.cat([output, torch.full((input_ids_len + self.args.max_gen_len - output.shape[0],), self.tokenizer.eos_token_id, dtype=torch.long, device=self.input_device)])
                            gen_output.append(output)
                            if len(gen_output) >= 10:
                                break

                    if len(gen_output) >= 10:
                        break

                if len(gen_output) > 0:
                    gen_output = torch.stack(gen_output)
                else:
                    return [], [], []

        else:
            if self.args.do_sample:
                print("Begin nucleus sampling")
                if self.args.seed is not None:
                    gen_output = self.model.generate(
                        input_ids,
                        do_sample=True,
                        num_return_sequences=self.args.num_gen,
                        temperature=self.args.temp,
                        max_new_tokens=self.args.max_gen_len,
                        top_p=self.args.top_p,
                        pad_token_id=self.tokenizer.pad_token_id,
                        use_cache=True,
                    )
                else:
                    gen_output = []
                    for _ in range(self.args.num_gen):
                        cur_gen_output = self.model.generate(
                            input_ids,
                            do_sample=True,
                            num_return_sequences=1,
                            temperature=self.args.temp,
                            max_new_tokens=self.args.max_gen_len,
                            top_p=self.args.top_p,
                            pad_token_id=self.tokenizer.pad_token_id,
                            use_cache=True,
                        )
                        for output in cur_gen_output:
                            if output.shape[0] < input_ids_len + self.args.max_gen_len:
                                output = torch.cat([output, torch.full((input_ids_len + self.args.max_gen_len - output.shape[0],), self.tokenizer.eos_token_id, dtype=torch.long, device=self.input_device)])
                            gen_output.append(output)
                    
                    gen_output = torch.stack(gen_output)

        return self.process_completions(input_src, input_ids_len, gen_output, lang)

class PrefixEvaler(EvalerBase):
    def __init__(self, args):
        super().__init__(args)

    def load_model(self):
        self.tokenizer, self.model, self.input_device = load_model('prefix', self.args.model_dir, False, self.args)
        self.model.eval()

    def sample(self, file_context, func_context, lang, vul_type, scenario):
        return self.sample_prefix(file_context, func_context, lang, vul_type, scenario)

    def sample_prefix(self, file_context, func_context, lang):
        input_src = file_context + func_context
        input_ids = self.tokenizer(input_src, return_tensors='pt').input_ids.to(self.input_device)
        input_ids_len = input_ids.shape[1]
        if self.args.num_beams > 1:
            constraints = None
            if self.args.pos_constraints is not None:
                constraints = []
                for cons in self.args.pos_constraints:
                    constraints.append(
                        PhrasalConstraint(
                            self.tokenizer(cons, add_special_tokens=False).input_ids
                        )
                    )
            logits_processors = []
            if self.args.neg_constraints is not None:
                logits_processors = [NegativeConstraintNGramLogitsProcessor(
                    self.tokenizer(self.args.neg_constraints, add_special_tokens=False).input_ids,
                )]
            if not self.args.do_sample:
                print("Begin beam search")
                gen_output = self.model.generate(
                    input_ids,
                    num_beams=self.args.num_beams,
                    max_new_tokens=self.args.max_gen_len,
                    pad_token_id=self.tokenizer.pad_token_id,
                    use_cache=True,
                    constraints=constraints,
                    logits_processor=LogitsProcessorList(logits_processors),
                    control_id=0,
                )
            else:
                print("Begin beam sampling")
                if self.args.pos_constraints is None and self.args.neg_constraints is None:
                    print("No constraints")
                    gen_output = self.model.generate(
                        input_ids,
                        do_sample=True,
                        num_return_sequences=self.args.num_gen,
                        num_beams=self.args.num_beams,
                        max_new_tokens=self.args.max_gen_len,
                        pad_token_id=self.tokenizer.pad_token_id,
                        use_cache=True,
                        control_id=0,
                    )
                    return self.process_completions(input_src, input_ids_len, gen_output, lang)
                gen_output = []
                constrained = []
                for _ in range(self.args.max_num_gen // self.args.num_gen):
                    cur_gen_output = self.model.generate(
                        input_ids,
                        do_sample=True,
                        num_return_sequences=self.args.num_gen,
                        num_beams=self.args.num_beams,
                        max_new_tokens=self.args.max_gen_len,
                        pad_token_id=self.tokenizer.pad_token_id,
                        use_cache=True,
                        constraints=constraints,
                        logits_processor=LogitsProcessorList(logits_processors),
                        control_id=0,
                    )
                    for output in cur_gen_output:
                        code = self.tokenizer.decode(output[input_ids_len:, ...])
                        if self.tokenizer.eos_token in code:
                            code = code[:code.find(self.tokenizer.eos_token)]
                        code = self.truncate(code, lang)
                        if check_constraints(code, self.args.pos_constraints, self.args.neg_constraints):
                            constrained.append(input_src + code)
                            if output.shape[0] < input_ids_len + self.args.max_gen_len:
                                output = torch.cat([output, torch.full((input_ids_len + self.args.max_gen_len - output.shape[0],), self.tokenizer.eos_token_id, dtype=torch.long, device=self.input_device)])
                            gen_output.append(output)
                            if len(gen_output) >= 10:
                                break
                    if len(gen_output) >= 10:
                        break

                if len(gen_output) > 0:
                    gen_output = torch.stack(gen_output)
                else:
                    return [], [], []
        else:
            if self.args.do_sample:
                print("Begin sampling")
                if self.args.seed is not None:
                    gen_output = self.model.generate(
                        input_ids,
                        do_sample=True,
                        num_return_sequences=self.args.num_gen,
                        temperature=self.args.temp,
                        max_new_tokens=self.args.max_gen_len,
                        top_p=self.args.top_p,
                        pad_token_id=self.tokenizer.pad_token_id,
                        use_cache=True,
                        control_id=0,
                    )
                else:
                    gen_output = []
                    for _ in range(self.args.num_gen):
                        cur_gen_output = self.model.generate(
                            input_ids,
                            do_sample=True,
                            num_return_sequences=1,
                            temperature=self.args.temp,
                            max_new_tokens=self.args.max_gen_len,
                            top_p=self.args.top_p,
                            pad_token_id=self.tokenizer.pad_token_id,
                            use_cache=True,
                            control_id=0,
                        )
                        for output in cur_gen_output:
                            if output.shape[0] < input_ids_len + self.args.max_gen_len:
                                output = torch.cat([output, torch.full((input_ids_len + self.args.max_gen_len - output.shape[0],), self.tokenizer.eos_token_id, dtype=torch.long, device=self.input_device)])
                            gen_output.append(output)
                    gen_output = torch.stack(gen_output)
        return self.process_completions(input_src, input_ids_len, gen_output, lang)

class TextPromptEvaler(EvalerBase):
    def __init__(self, args):
        super().__init__(args)

    def load_model(self):
        self.tokenizer, self.model, self.input_device = load_model('lm', self.args.model_dir, False, self.args)
        self.model.eval()

    def sample(self, file_context, func_context, lang):
        if lang == 'py':
            input_src = file_context + '# ' + 'The following code is secure\n', + func_context
        elif lang == 'c' or lang == 'cpp':
            input_src = file_context + '// ' + 'The following code is secure\n', + func_context
        else:
            raise NotImplementedError()
        input_ids = self.tokenizer(input_src, return_tensors='pt').input_ids.to(self.input_device)
        input_ids_len = input_ids.shape[1]
        if self.args.seed is not None:
            gen_output = self.model.generate(
                input_ids,
                do_sample=True,
                num_return_sequences=self.args.num_gen,
                temperature=self.args.temp,
                max_new_tokens=self.args.max_gen_len,
                top_p=self.args.top_p,
                pad_token_id=self.tokenizer.pad_token_id,
                use_cache=True,
            )
        else:
            gen_output = []
            for _ in range(self.args.num_gen):
                cur_gen_output = self.model.generate(
                    input_ids,
                    do_sample=True,
                    num_return_sequences=1,
                    temperature=self.args.temp,
                    max_new_tokens=self.args.max_gen_len,
                    top_p=self.args.top_p,
                    pad_token_id=self.tokenizer.pad_token_id,
                    use_cache=True,
                )
                for output in cur_gen_output:
                    if output.shape[0] < input_ids_len + self.args.max_gen_len:
                        output = torch.cat([output, torch.full((input_ids_len + self.args.max_gen_len - output.shape[0],), self.tokenizer.eos_token_id, dtype=torch.long, device=self.input_device)])
                    gen_output.append(output)
            gen_output = torch.stack(gen_output)

        return self.process_completions(input_src, input_ids_len, gen_output, lang)

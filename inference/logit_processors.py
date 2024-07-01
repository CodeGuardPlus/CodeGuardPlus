from __future__ import annotations
import collections
from math import sqrt

import scipy.stats

import torch
from torch import Tensor
from tokenizers import Tokenizer
from transformers import LogitsProcessor, AutoTokenizer
from typing import Callable, Iterable, List, Optional, Tuple, Union


class NegativeConstraintNGramLogitsProcessor(LogitsProcessor):
    r"""
    N-grams are groups of "n" consecutive words, characters, or tokens taken from a sequence of text. Given the
    sentence: "She runs fast", the bi-grams (n=2) would be ("she", "runs") and ("runs", "fast"). In text generation,
    avoiding repetitions of word sequences provides a more diverse output. This [`LogitsProcessor`] enforces no
    repetition of n-grams by setting the scores of banned tokens to negative infinity which eliminates those tokens
    from consideration when further processing the scores. Note that, for decoder-only models like most LLMs, the
    prompt is also considered to obtain the n-grams.
    [Fairseq](https://github.com/pytorch/fairseq/blob/a07cb6f40480928c9e0548b737aadd36ee66ac76/fairseq/sequence_generator.py#L345).

    <Tip>

    Use n-gram penalties with care. For instance, penalizing 2-grams (bigrams) in an article about the city of New York
    might lead to undesirable outcomes where the city's name appears only once in the entire text.
    [Reference](https://huggingface.co/blog/how-to-generate)

    </Tip>

    Args:
        ngram_size (`int`):
            All ngrams of size `ngram_size` can only occur once.

    Examples:

    ```py
    >>> from transformers import AutoTokenizer, AutoModelForCausalLM

    >>> model = AutoModelForCausalLM.from_pretrained("distilgpt2")
    >>> tokenizer = AutoTokenizer.from_pretrained("distilgpt2")
    >>> inputs = tokenizer(["Today I"], return_tensors="pt")

    >>> output = model.generate(**inputs)
    >>> print(tokenizer.decode(output[0], skip_special_tokens=True))
    Today I’m not sure if I’m going to be able to do it.

    >>> # Now let's add ngram size using `no_repeat_ngram_size`. This stops the repetitions ("I’m") in the output.
    >>> output = model.generate(**inputs, no_repeat_ngram_size=2)
    >>> print(tokenizer.decode(output[0], skip_special_tokens=True))
    Today I’m not sure if I can get a better understanding of the nature of this issue
    ```
    """

    def __init__(self, negative_constraints: List[List[int]]):
        self.negative_constraints = dict()
        for constraint in negative_constraints:
            self.negative_constraints[tuple(constraint[:-1])] = constraint[-1]

    def __call__(self, input_ids: torch.LongTensor, scores: torch.FloatTensor) -> torch.FloatTensor:
        num_batch_hypotheses = scores.shape[0]
        cur_len = input_ids.shape[-1]
        for i in range(num_batch_hypotheses):
            for ngram in self.negative_constraints:
                ngram_size = len(ngram) + 1
                if cur_len + 1 < ngram_size:
                    continue
                prev_ngram_tuple = tuple(input_ids[i, cur_len + 1 - ngram_size:cur_len].tolist())
                banned_token = self.negative_constraints.get(prev_ngram_tuple, None)
                if banned_token is not None:
                    scores[i, banned_token] = float("-inf")

        return scores
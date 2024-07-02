# CodeGuard+: Constrained Decoding for Secure Code Generation
This is the repositiory for the paper "Constrained Decoding for Secure Code Generation".

<p align="center">
  <a href="https://codeguardplus.github.io">🏠 Home Page</a> •
  <a href="https://codeguardplus.github.io/leaderboard.html">🏆 Leaderboard</a> •
  <a href="https://arxiv.org/pdf/2405.00218">📄 Paper</a>
</p>

## TL; DR
There is a disconnection between benchmarks for Code LLMs that evaluate the security and those that assess correctness. Existing benchmarks, like HumanEval and MBPP only evaluate the correctness, while others like Copilot dataset and SecurityEval only target on the security. To bridge this gap, we present CodeGuard+, along with two new metrics, to measure Code LLMs' ability to generate both secure and correct code. Currently, CodeGuard+ supports Python and C/C++, with 103 prompts covering 42 CWEs.

## Directory Structure
The directory structure of this repository is as follows:
```
.
|-- data                       # All prompts.
    |-- base                   # Basic prompts
    |-- perturbed              # Perturbed prompts (pending)
|-- inference                  # Code for inference
|-- unit_test                  # Unit tests for each prompt
    |-- CWE
        |-- prompt
            |-- functional.py  # Individual unit test
|-- requirements.txt           # Python packages needed by prompts and unit tests
```

## Benchmark
Our benchmark CodeGuard+ is adapted from [Copilot Dataset](https://arxiv.org/abs/2108.09293), [SecurityEval](https://dl.acm.org/doi/abs/10.1145/3549035.3561184) and [CodeQL official repository](https://github.com/github/codeql). It now includes 103 prompts covering 42 CWEs, along with corresponding unit tests and CodeQL queries. You can find prompts and CodeQL queries in `data` and unit_tests in `unit_test`.

## Preparation
### Install dependencies
```bash
pip install -r requirements.txt
```
### Install CodeQL
```bash
bash setup_codeql.sh
```
### Install SonarQube
1. Verify docker is installed;
2. Run `bash setup_sonar.sh`;
3. Once the sonar server process starts, access the sonar sever gui by opening [http://127.0.0.1:9000](http://127.0.0.1:9000), and login to the server (the default username and password are `admin`);
4. Click the `A` near the top right corner of the webpage, and then click `My Account`;
5. Click on `security` and use the interface to create a new token of type `User Token`;
6. Modify `sonar_eval.py` with token you just generated and your desired scan path.


## Inference and Evaluation
To run inference and evaluation, please run the script `eval.sh` using the following command template:
```bash
bash eval.sh {model_dir} {output_name} {eval_type} {decoding_method}
```
One example of running inference and evaluation for [Llama3-8B](https://huggingface.co/meta-llama/Meta-Llama-3-8B) is:
```bash
bash eval.sh meta-llama/Meta-Llama-3-8B llama3-nucleus base nucleus
```
The default settings for inference is to use Nucleus Sampling with `temperature=0.4` and `top_p=0.95` to generate 10 programs. Please check `generate.py`, `codeql_eval.py`, `sonar_eval.py` and `correctness_eval.py` for more details about arguments, customized inference and customized evaluation.

## Work in Progress
This repository is still under construction, thank you for your patience! 

## Citation
```
@article{fu2024constrained,
      title={Constrained Decoding for Secure Code Generation}, 
      author={Yanjun Fu and Ethan Baker and Yu Ding and Yizheng Chen},
      year={2024},
      journal={arXiv preprint arXiv:2405.00218}
}
```
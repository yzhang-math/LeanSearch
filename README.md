## LeanSearch
Lean 4 proof search using LLM.


## Prerequisites
1. Python 3.9-3.11 (required by lean_dojo)
2. lean_dojo

## Usage and Example

[Look at the funsearch project for command, options and environment file](https://github.com/kitft/funsearch)

To use LeanSearch, you need to have built and traced a lean 4 repositary with lean_dojo, and use the exact same theorem statement as in the locally traced Lean repositary.

As a result, in addition to change the input sepc file, you also need to update the sandbox initialization in sandbox.py to setup lean_dojo with the theorem needed. See [lean_dojo document](https://github.com/lean-dojo/LeanDojo/blob/main/scripts/demo-lean4.ipynb) for the setup.

An example command is

```console
python ./leansearch/__main__.py runasync ./examples/Pi_eq_sum_univ.lean 10 --sandbox ExternalProcessSandbox --model mistralai/mistral-small-24b-instruct-2501 --evaluators 10 --samplers 10 --islands 5 --duration 60 --tag lean_test --envfile .env
```
As of now, the --@funsearch.run theorem, and the argument after spec file, are both needed but without real usage. The sandbox must be ExternalProcessSandbox. The backup modules are functional but don't record everything yet. Also, only a limited number of tactics are supported.


## Acknowledgments

LeanSearch builds upon two previous projects:

1. [kitft/funsearch](https://github.com/kitft/funsearch) - An enhanced implementation of FunSearch with parallel processing and much more features.

2. The original project (https://github.com/google-deepmind/funsearch) by DeepMind Technologies Limited, as described in:
```bibtex
@Article{FunSearch2023,
  author  = {Romera-Paredes, Bernardino and others},
  journal = {Nature},
  title   = {Mathematical discoveries from program search with large language models},
  year    = {2023},
  doi     = {10.1038/s41586-023-06924-6}
}
```

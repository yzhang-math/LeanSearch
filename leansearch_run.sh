#!/bin/bash
#--model google/gemini-2.0-flash-001,deepseek/deepseek-r1-distill-llama-70b \
#./examples/minif2fvalid/theorems/aimeII_2020_p6.lean "Lean4Example.lean","aimeII_2020_p6" \
python ./leansearch/__main__.py runasync \
    ./examples/minif2ftest/theorems/aime_1983_p1.lean "minif2f_test.lean","aime_1983_p1" \
    --sandbox ExternalProcessSandbox \
    --team yzh0123-uw-madison  \
    --model vllm*8\
    --evaluators 8 --samplers 8 --islands 15 --duration 1200 --tag lean_test --envfile .env
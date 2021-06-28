1. 
in eval.py: change output_folder=...
adapt config.py
(maybe need to adapt cuda in python script)
Call CUDA_VISIBLE_DEVICE=0 python eval.py

2.
in runIJBEval.sh
change: MODEL, ITERationS, TARGET, OUTPUT (-E..), and CUDA_VISIBLE_DEVICE
adapt config.py
run: runIJBEval.sh

3. 
in runMegafaceEval.sh
change: ALGO, NUM_ITERATIONS, EPOCH, and CUDA_VISIBLE_DEVICE
adapt config.py
comment out line 22 and comment in line 24 when running on noisy features
run: runMegafaceEval.sh

4.
in plot_results.py
change: sample=... (in line 20) and maybe line 690
run: python plot_results.py

returns:
===> Calc and save TPR@FPR=1e-06 for method: cos_semore_combine_mixcon_s_0.5-25-noisy
TPR@FPR=1e-06 at different #distractors
#distractors  TPR

1000000 0.883707

0.883707 = 1e-6 VAR (important)


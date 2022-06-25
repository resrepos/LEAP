#!/bin/bash --login

pip install numpy scipy matplotlib ipython jupyter pandas sympy nose
pip install openpyxl
#pip install transformers -U
pip install simpletransformers==0.51.13
pip install dataframe-image

seeds=(0 42)
for s in ${seeds[@]}
do
  mkdir new_results_Seed$s
  e=15
  mkdir new_results_Seed$s/Epoch$e
  echo  new_results_Seed$s/Epoch$e $e $s
  python3 sentiment_analysis.py --epoch $e --seed $s --directory results_Seed$s/Epoch$e/
done


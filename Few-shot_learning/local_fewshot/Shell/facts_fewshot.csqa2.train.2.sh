# bsub -n 1 -q HPC.S1.GPU.X785.sha -o few-shot.csqa2.train.2.log -gpu num=1:mode=exclusive_process sh Shell/facts_fewshot.csqa2.train.2.sh

python few-shot.py \
    --data_type csqa2 \
    --task_type facts \
    --model_type gpt-neo \
    --model_path /SISDC_GPFS/Home_SE/hy-suda/pre-train_model/gpt-neo-2.7B \
    --prompt_path /SISDC_GPFS/Home_SE/hy-suda/zfli/CODE/Project-Final/Few-shot_learning/GPT3_fewshot/Prompts/unified_facts/v3.6.txt \
    --input_path /SISDC_GPFS/Home_SE/hy-suda/zfli/CODE/Project-Final/Data/Raw_data/csqa2/CSQA2_train.json \
    --output_path /SISDC_GPFS/Home_SE/hy-suda/zfli/CODE/Project-Final/Data/Constructed_data/CSQA2/fact_neo/train.2.jsonl \
    --temperature 0.7\
    --top_p 0.5 \
    --start_idx 5000 \
    --end_idx -1\
    --output_num 5\
    --device cuda:0 \
    --max_tokens 32

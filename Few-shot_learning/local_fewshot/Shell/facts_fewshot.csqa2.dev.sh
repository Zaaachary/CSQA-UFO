# bsub -n 1 -q HPC.S1.GPU.X785.sha -o few-shot.csqa.dev.log -gpu num=1:mode=exclusive_process sh Shell/facts_fewshot.csqa2.dev.sh

python few-shot.py \
    --data_type csqa2 \
    --task_type facts \
    --model_type gpt-neo \
    --model_path /SISDC_GPFS/Home_SE/hy-suda/pre-train_model/gpt-neo-2.7B \
    --prompt_path /SISDC_GPFS/Home_SE/hy-suda/zfli/CODE/Project-Final/Few-shot_learning/GPT3_fewshot/Prompts/unified_facts/v3.6.txt \
    --input_path /SISDC_GPFS/Home_SE/hy-suda/zfli/CODE/Project-Final/Data/Raw_data/csqa2/CSQA2_dev.json \
    --output_path /SISDC_GPFS/Home_SE/hy-suda/zfli/CODE/Project-Final/Data/Constructed_data/CSQA2/fact_neo/dev.jsonl \
    --temperature 0.7\
    --top_p 0.5 \
    --start_idx 0 \
    --end_idx -1\
    --output_num 5\
    --device cuda:0 \
    --max_tokens 32


python few-shot.py \
    --data_type csqa2 \
    --task_type facts \
    --model_type gpt-neo \
    --model_path /SISDC_GPFS/Home_SE/hy-suda/pre-train_model/gpt-neo-2.7B \
    --prompt_path /SISDC_GPFS/Home_SE/hy-suda/zfli/CODE/Project-Final/Few-shot_learning/GPT3_fewshot/Prompts/unified_facts/v3.6.txt \
    --input_path /SISDC_GPFS/Home_SE/hy-suda/zfli/CODE/Project-Final/Data/Raw_data/csqa2/CSQA2_test_no_answers.json \
    --output_path /SISDC_GPFS/Home_SE/hy-suda/zfli/CODE/Project-Final/Data/Constructed_data/CSQA2/fact_neo/CSQA2_test_no_answers.jsonl \
    --temperature 0.7\
    --top_p 0.5 \
    --start_idx 0 \
    --end_idx -1\
    --output_num 5\
    --device cuda:0 \
    --max_tokens 32

    # --engine text-curie-001 \


    # --input_path /SISDC_GPFS/Home_SE/hy-suda/zfli/CODE/Project-Final/Data/Raw_data/ProtoQA/origin/dev.scraped.jsonl  \
    # --output_path /SISDC_GPFS/Home_SE/hy-suda/zfli/CODE/Project-Final/Data/Constructed_data/ProtoQA/Few-shot_facts_v2/dev.scraped.v1.3.jsonl  \

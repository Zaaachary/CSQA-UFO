python gpt3_fewshot.py \
    --data_type csqa2 \
    --task_type qa_facts \
    --prompt_path /SISDC_GPFS/Home_SE/hy-suda/zfli/CODE/Project-Final/Few-shot_learning/GPT3_fewshot/Prompts/csqa2_facts_few-shot.txt \
    --input_path /SISDC_GPFS/Home_SE/hy-suda/zfli/CODE/Project-Final/Data/Constructed_data/GPT3_evaluate/unified_evaluate/unified.v2.jsonl \
    --output_path /SISDC_GPFS/Home_SE/hy-suda/zfli/CODE/Project-Final/Data/Constructed_data/CSQA2/dpr_dev/unified.facts.jsonl \
    --temperature 0.7\
    --top_p 0.5 \
    --start_idx 10 \
    --end_idx 20\
    --output_num 1\
    --engine text-davinci-003 \
    --max_tokens 32



    # --input_path /SISDC_GPFS/Home_SE/hy-suda/zfli/CODE/Project-Final/Data/Raw_data/ProtoQA/origin/dev.scraped.jsonl  \
    # --output_path /SISDC_GPFS/Home_SE/hy-suda/zfli/CODE/Project-Final/Data/Constructed_data/ProtoQA/Few-shot_facts_v2/dev.scraped.v1.3.jsonl  \

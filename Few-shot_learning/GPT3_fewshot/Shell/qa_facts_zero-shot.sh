python gpt3_fewshot.py \
    --data_type obqa \
    --task_type qa_facts \
    --prompt_path /SISDC_GPFS/Home_SE/hy-suda/zfli/CODE/Project-Final/Few-shot_learning/GPT3_fewshot/Prompts/qa_facts_zero_shot_v1.2.txt \
    --input_path /SISDC_GPFS/Home_SE/hy-suda/zfli/CODE/Project-Final/Data/Constructed_data/OBQA/facts/dev.jsonl  \
    --output_path /SISDC_GPFS/Home_SE/hy-suda/zfli/CODE/Project-Final/Data/Constructed_data/OBQA/qa/facts_zero-shot/dev.v1.2.jsonl \
    --temperature 0.7\
    --top_p 0.5 \
    --start_idx 0 \
    --end_idx 10\
    --output_num 1\
    --engine text-davinci-003 \
    --max_tokens 32



    # --input_path /SISDC_GPFS/Home_SE/hy-suda/zfli/CODE/Project-Final/Data/Raw_data/ProtoQA/origin/dev.scraped.jsonl  \
    # --output_path /SISDC_GPFS/Home_SE/hy-suda/zfli/CODE/Project-Final/Data/Constructed_data/ProtoQA/Few-shot_facts_v2/dev.scraped.v1.3.jsonl  \

python gpt3_fewshot.py \
    --data_type unified \
    --task_type facts \
    --prompt_path Prompts/unified_facts/v3.6.txt \
    --input_path /SISDC_GPFS/Home_SE/hy-suda/zfli/CODE/Project-Final/Data/Constructed_data/GPT3_evaluate/qasc.dev.jsonl \
    --output_path /SISDC_GPFS/Home_SE/hy-suda/zfli/CODE/Project-Final/Data/Constructed_data/GPT3_evaluate/unified_facts_evaluate/v3.6/unified.v2.jsonl  \
    --temperature 0.7\
    --top_p 0.5 \
    --start_idx 0 \
    --end_idx 30\
    --engine text-curie-001 \
    --output_num 5\
    --max_tokens 128

    # --engine text-davinci-003 \


    # --input_path /SISDC_GPFS/Home_SE/hy-suda/zfli/CODE/Project-Final/Data/Raw_data/ProtoQA/origin/dev.scraped.jsonl  \
    # --output_path /SISDC_GPFS/Home_SE/hy-suda/zfli/CODE/Project-Final/Data/Constructed_data/ProtoQA/Few-shot_facts_v2/dev.scraped.v1.3.jsonl  \

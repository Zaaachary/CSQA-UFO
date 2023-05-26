python gpt3_fewshot.py \
    --data_type qasc \
    --task_type qa \
    --prompt_path D:\Project\CSQA-UFO\Few-shot_learning\GPT3_fewshot\Prompts\qa_zero_shot.txt \
    --input_path D:\Project\CSQA-UFO\Constructed_data\QASC\gpt-3\dev.jsonl  \
    --output_path D:\Project\CSQA-UFO\Constructed_data\QASC\gpt-3-qa\dev.jsonl \
    --temperature 0\
    --top_p 0 \
    --start_idx 0 \
    --end_idx 10\
    --output_num 1\
    --engine text-davinci-003 \
    --max_tokens 5



    # --input_path /SISDC_GPFS/Home_SE/hy-suda/zfli/CODE/Project-Final/Data/Raw_data/ProtoQA/origin/dev.scraped.jsonl  \
    # --output_path /SISDC_GPFS/Home_SE/hy-suda/zfli/CODE/Project-Final/Data/Constructed_data/ProtoQA/Few-shot_facts_v2/dev.scraped.v1.3.jsonl  \

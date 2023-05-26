    # --input_path /SISDC_GPFS/Home_SE/hy-suda/zfli/CODE/Project-Final/Data/Raw_data/ProtoQA/Few-shot_version/dev.scraped.jsonl \
    # --input_path /SISDC_GPFS/Home_SE/hy-suda/zfli/CODE/Project-Final/Data/Raw_data/ProtoQA/Few-shot_version/test.questions.jsonl \

python gpt3_fewshot.py \
    --data_type unified \
    --task_type description \
    --prompt_path /SISDC_GPFS/Home_SE/hy-suda/zfli/CODE/Project-Final/Few-shot_learning/GPT3_fewshot/Prompts/unified_information/version_2.3.txt \
    --input_path /SISDC_GPFS/Home_SE/hy-suda/zfli/CODE/Project-Final/Data/Constructed_data/GPT3_evaluate/keypoint_fewshot/unified.v1.fs.v2.2.jsonl  \
    --output_path /SISDC_GPFS/Home_SE/hy-suda/zfli/CODE/Project-Final/Data/Constructed_data/GPT3_evaluate/information_fewshot/protoqa_info.v1.fs.v2.3.jsonl \
    --temperature 0.7\
    --top_p 0.5 \
    --start_idx 16 \
    --end_idx -1\
    --max_description_num 1\
    --output_num 1\
    --engine text-davinci-003 \
    --max_tokens 64

    # --engine text-curie-001 \
# request_id=bd2555b4aaafc7bb96249f75e6190a60
    # --engine curie \
    # --engine davinci \
    # --engine ada\
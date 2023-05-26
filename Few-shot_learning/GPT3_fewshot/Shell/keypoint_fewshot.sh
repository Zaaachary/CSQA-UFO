    # --input_path /SISDC_GPFS/Home_SE/hy-suda/zfli/CODE/Project-Final/Data/Raw_data/ProtoQA/Few-shot_version/dev.scraped.jsonl \
    # --input_path /SISDC_GPFS/Home_SE/hy-suda/zfli/CODE/Project-Final/Data/Raw_data/ProtoQA/Few-shot_version/test.questions.jsonl \

python gpt3_fewshot.py \
    --data_type csqa2\
    --task_type keypoints \
    --prompt_path /SISDC_GPFS/Home_SE/hy-suda/zfli/CODE/Project-Final/Few-shot_learning/GPT3_fewshot/Prompts/unified_keypoint/version_2.2.txt \
    --input_path /SISDC_GPFS/Home_SE/hy-suda/zfli/CODE/Project-Final/Data/Constructed_data/CSQA2/Few-shot_keypoint/unified_v2.2/CSQA2_dev_miss.10.json \
    --output_path /SISDC_GPFS/Home_SE/hy-suda/zfli/CODE/Project-Final/Data/Constructed_data/CSQA2/Few-shot_keypoint/unified_v2.2/CSQA2_dev_miss.10.kw.json \
    --temperature 0.7\
    --top_p 0.5 \
    --start_idx 0 \
    --end_idx -1\
    --output_num 1\
    --engine text-davinci-003 \
    --max_tokens 32


    # --temperature 0.7\
    # --engine curie \
    # --engine davinci \
    # --engine ada\
    # --input_path /SISDC_GPFS/Home_SE/hy-suda/zfli/CODE/Project-Final/Data/Raw_data/ProtoQA/Few-shot_version/dev.scraped.jsonl \
    # --input_path /SISDC_GPFS/Home_SE/hy-suda/zfli/CODE/Project-Final/Data/Raw_data/ProtoQA/Few-shot_version/test.questions.jsonl \

python gpt3_generate_knowledge.py \
    --input_path /SISDC_GPFS/Home_SE/hy-suda/zfli/CODE/Project-Final/Data/Raw_data/ProtoQA/Few-shot_version/test.questions.jsonl  \
    --output_path /SISDC_GPFS/Home_SE/hy-suda/zfli/CODE/Project-Final/Data/Constructed_data/ProtoQA/Few-shot_knowledge/protoqa_v3_curie/test.questions.jsonl \
    --prompt_path /SISDC_GPFS/Home_SE/hy-suda/zfli/CODE/Project-Final/Few-shot_learning/GPT3_fewshot/Prompts/ProtoQA/ptqa_prompt_v3.txt \
    --num_knowledge 1 \
    --engine curie \
    --start 0 \
    --end 2000


    # --engine curie \
    # --engine davinci \
    # --engine ada\
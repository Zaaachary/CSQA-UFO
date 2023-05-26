    # --input_path /SISDC_GPFS/Home_SE/hy-suda/zfli/CODE/Project-Final/Data/Raw_data/ProtoQA/Few-shot_version/dev.scraped.jsonl \
    # --input_path /SISDC_GPFS/Home_SE/hy-suda/zfli/CODE/Project-Final/Data/Raw_data/ProtoQA/Few-shot_version/test.questions.jsonl \

python gpt3_generate_description.py \
    --input_path /SISDC_GPFS/Home_SE/hy-suda/zfli/CODE/Project-Final/Data/Constructed_data/ProtoQA/Prefix_keyword_v1/train.scraped.jsonl  \
    --output_path /SISDC_GPFS/Home_SE/hy-suda/zfli/CODE/Project-Final/Data/Constructed_data/ProtoQA/Few-shot_description/protoqa_v3_curie/train.scraped.jsonl \
    --prompt_path /SISDC_GPFS/Home_SE/hy-suda/zfli/CODE/Project-Final/Few-shot_learning/GPT3_fewshot/Prompts/ProtoQA/ptqa_description.txt \
    --num_knowledge 1 \
    --engine curie \
    --desc \
    --start 6351 \
    --end 9000
python gpt3_generate_description.py \
    --input_path /SISDC_GPFS/Home_SE/hy-suda/zfli/CODE/Project-Final/Data/Constructed_data/ProtoQA/Prefix_keyword_v1/dev.scraped.jsonl  \
    --output_path /SISDC_GPFS/Home_SE/hy-suda/zfli/CODE/Project-Final/Data/Constructed_data/ProtoQA/Few-shot_description/protoqa_v3_curie/dev.scraped.jsonl \
    --prompt_path /SISDC_GPFS/Home_SE/hy-suda/zfli/CODE/Project-Final/Few-shot_learning/GPT3_fewshot/Prompts/ProtoQA/ptqa_description.txt \
    --num_knowledge 1 \
    --engine curie \
    --desc \
    --start 0 \
    --end 2000
python gpt3_generate_description.py \
    --input_path /SISDC_GPFS/Home_SE/hy-suda/zfli/CODE/Project-Final/Data/Constructed_data/ProtoQA/Prefix_keyword_v1/dev.crowdsourced.jsonl  \
    --output_path /SISDC_GPFS/Home_SE/hy-suda/zfli/CODE/Project-Final/Data/Constructed_data/ProtoQA/Few-shot_description/protoqa_v3_curie/dev.crowdsourced.jsonl \
    --prompt_path /SISDC_GPFS/Home_SE/hy-suda/zfli/CODE/Project-Final/Few-shot_learning/GPT3_fewshot/Prompts/ProtoQA/ptqa_description.txt \
    --num_knowledge 1 \
    --engine curie \
    --desc \
    --start 0 \
    --end 70


    # --engine curie \
    # --engine davinci \
    # --engine ada\
    # --input_path /SISDC_GPFS/Home_SE/hy-suda/zfli/CODE/Project-Final/Data/Raw_data/ProtoQA/Few-shot_version/dev.scraped.jsonl \
    # --input_path /SISDC_GPFS/Home_SE/hy-suda/zfli/CODE/Project-Final/Data/Raw_data/ProtoQA/Few-shot_version/test.questions.jsonl \

python gpt3_generate_keywords.py \
    --input_path /SISDC_GPFS/Home_SE/hy-suda/zfli/CODE/Project-Final/Data/Raw_data/ProtoQA/Few-shot_version/dev.crowdsourced.jsonl  \
    --output_path /SISDC_GPFS/Home_SE/hy-suda/zfli/CODE/Project-Final/Data/Constructed_data/ProtoQA/Few-shot_keywords/protoqa_v3_curie/dev.crowdsourced.jsonl \
    --prompt_path /SISDC_GPFS/Home_SE/hy-suda/zfli/CODE/Project-Final/Few-shot_learning/GPT3_fewshot/Prompts/ProtoQA/ptqa_keyword_prompt_v3.txt \
    --max_tokens 256\
    --num_knowledge 1 \
    --engine curie \
    --start 0 \
    --end 10000

python gpt3_generate_keywords.py \
    --input_path /SISDC_GPFS/Home_SE/hy-suda/zfli/CODE/Project-Final/Data/Raw_data/ProtoQA/Few-shot_version/train.scraped.jsonl  \
    --output_path /SISDC_GPFS/Home_SE/hy-suda/zfli/CODE/Project-Final/Data/Constructed_data/ProtoQA/Few-shot_keywords/protoqa_v3_curie/train.scraped.jsonl \
    --prompt_path /SISDC_GPFS/Home_SE/hy-suda/zfli/CODE/Project-Final/Few-shot_learning/GPT3_fewshot/Prompts/ProtoQA/ptqa_keyword_prompt_v3.txt \
    --max_tokens 256\
    --num_knowledge 1 \
    --engine curie \
    --start 0 \
    --end 10000

python gpt3_generate_keywords.py \
    --input_path /SISDC_GPFS/Home_SE/hy-suda/zfli/CODE/Project-Final/Data/Raw_data/ProtoQA/Few-shot_version/dev.scraped.jsonl  \
    --output_path /SISDC_GPFS/Home_SE/hy-suda/zfli/CODE/Project-Final/Data/Constructed_data/ProtoQA/Few-shot_keywords/protoqa_v3_curie/dev.scraped.jsonl \
    --prompt_path /SISDC_GPFS/Home_SE/hy-suda/zfli/CODE/Project-Final/Few-shot_learning/GPT3_fewshot/Prompts/ProtoQA/ptqa_keyword_prompt_v3.txt \
    --max_tokens 256\
    --num_knowledge 1 \
    --engine curie \
    --start 0 \
    --end 10000

    # --engine davinci \
    # --engine curie \
    # --engine ada\
# bsub -n 1 -q HPC.S1.GPU.X785.sha -o few-shot.obqa.train.2.log -gpu num=1:mode=exclusive_process sh Shell/facts_fewshot.obqa.2.sh

python few-shot.py \
    --data_type obqa \
    --task_type facts \
    --model_type gpt-neo \
    --model_path /SISDC_GPFS/Home_SE/hy-suda/pre-train_model/gpt-neo-2.7B \
    --prompt_path /SISDC_GPFS/Home_SE/hy-suda/zfli/CODE/Project-Final/Few-shot_learning/GPT3_fewshot/Prompts/unified_facts/v3.6.txt \
    --input_path /SISDC_GPFS/Home_SE/hy-suda/zfli/CODE/Project-Final/Data/Raw_data/obqa/train.jsonl \
    --output_path /SISDC_GPFS/Home_SE/hy-suda/zfli/CODE/Project-Final/Data/Constructed_data/OBQA/facts_neo/train.2.jsonl \
    --temperature 0.7\
    --top_p 0.5 \
    --start_idx 2000 \
    --end_idx -1 \
    --output_num 5\
    --device cuda:0 \
    --max_tokens 32


    # --engine text-curie-001 \


    # --input_path /SISDC_GPFS/Home_SE/hy-suda/zfli/CODE/Project-Final/Data/Raw_data/ProtoQA/origin/dev.scraped.jsonl  \
    # --output_path /SISDC_GPFS/Home_SE/hy-suda/zfli/CODE/Project-Final/Data/Constructed_data/ProtoQA/Few-shot_facts_v2/dev.scraped.v1.3.jsonl  \

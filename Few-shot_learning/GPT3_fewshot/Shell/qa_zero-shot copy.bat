python gpt3_fewshot.py ^
    --data_type qasc ^
    --task_type qa ^
    --prompt_path D:\Project\CSQA-UFO\Few-shot_learning\GPT3_fewshot\Prompts\qa_zero_shot.txt ^
    --input_path D:\Project\CSQA-UFO\Constructed_data\QASC\gpt-3\dev.jsonl  ^
    --output_path D:\Project\CSQA-UFO\Constructed_data\QASC\gpt-3-qa\dev.jsonl ^
    --temperature 0 ^
    --top_p 0 ^
    --start_idx 10 ^
    --end_idx 100 ^
    --output_num 1 ^
    --engine text-davinci-003 ^
    --max_tokens 5 

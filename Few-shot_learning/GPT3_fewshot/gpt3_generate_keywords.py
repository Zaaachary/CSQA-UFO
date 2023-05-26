from gpt3_generation import request
import pandas as pd
from tqdm import tqdm
import numpy as np
import random
import json
import torch
import click
from pathlib import Path
from typing import List


def prompt_format(prompt_path: str, keywords: List[str], query: str):
    with open(prompt_path) as f:
        context_string = f.read().strip('\n')
    if keywords is not None:
        n = np.random.choice(range(1, len(keywords)+1))      # number of keywords
        keywords = random.sample(keywords, n)                # subset of keywords
        context_string = context_string.replace('{keywords}', ', '.join(keywords))
    if query is not None:
        context_string = context_string.replace('{question}', query)
    return context_string

# python gpt3_generate_knowledge.py --input_path /SISDC_GPFS/Home_SE/hy-suda/zfli/CODE/Project-Final/Data/Raw_data/ProtoQA/Few-shot_version/train.scraped.jsonl --output_path /SISDC_GPFS/Home_SE/hy-suda/zfli/CODE/Project-Final/Data/Constructed_data/ProtoQA/Few-shot_knowledge/train.scraped.json --prompt_path /SISDC_GPFS/Home_SE/hy-suda/zfli/CODE/Project-Final/Few-shot_learning/GPT3_fewshot/Prompts/ProtoQA/ptqa_keyword_prompt_v2.txt --num_knowledge 2 --start 0 --end 1

@click.command()
@click.option('--input_path', type=str, default=None)
@click.option('--output_path', type=str, default=None)
@click.option('--prompt_path', type=str, default=None)
@click.option('--num_knowledge', type=int, default=2)
@click.option('--top_p', default=0.5, type=float)
@click.option('--temperature', default=1.0, type=float)
@click.option('--max_tokens', default=30, type=int)
@click.option('--start', default=None, type=int)
@click.option('--end', default=None, type=int)
@click.option('--engine', default='davinci', type=str)
def main(
    # task: str,
    input_path: str,
    output_path: str,
    prompt_path: bool,
    num_knowledge: int,
    top_p: float,
    temperature: float,
    max_tokens: int,
    start: int,
    end: int,
    engine: str,
):
    eval_df = pd.read_json(input_path)
    eval_df = eval_df[start:end]


    # with open
    with open(output_path, 'a') as fo:
        for i, row in tqdm(eval_df.iterrows(), total=end-start):
            context_string = prompt_format(
                prompt_path,
                keywords=None,
                query=row['query'])
            try:
                knowledges = request(
                    context_string,
                    engine=engine,
                    n=num_knowledge,
                    top_p=top_p,
                    stop='\n\n',
                    temperature=temperature,
                    max_tokens=max_tokens+len(context_string.split()))
                row['knowledges'] = list(set(knowledges))
                temp = json.dumps(row.to_dict())
                fo.write(temp + '\n')
                fo.flush()
            except:
                print(f'error in {i}')
                exit()
    

if __name__ == '__main__':
    main()

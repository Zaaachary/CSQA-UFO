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

from utils import load_data, dump_data

def prompt_format(prompt_path: str, query: str, concept=''):
    with open(prompt_path) as f:
        context_string = f.read().strip('\n')
    if concept is not None:
        context_string = context_string.replace('{concept}', concept)
    if query is not None:
        context_string = context_string.replace('{question}', query)
    return context_string

# python gpt3_generate_knowledge.py --input_path /SISDC_GPFS/Home_SE/hy-suda/zfli/CODE/Project-Final/Data/Raw_data/ProtoQA/Few-shot_version/train.scraped.jsonl --output_path /SISDC_GPFS/Home_SE/hy-suda/zfli/CODE/Project-Final/Data/Constructed_data/ProtoQA/Few-shot_knowledge/train.scraped.json --prompt_path /SISDC_GPFS/Home_SE/hy-suda/zfli/CODE/Project-Final/Few-shot_learning/GPT3_fewshot/Prompts/ProtoQA/ptqa_prompt.txt --num_knowledge 2 --start 0 --end 1

@click.command()
@click.option('--input_path', type=str, default=None)
@click.option('--output_path', type=str, default=None)
@click.option('--prompt_path', type=str, default=None)
@click.option('--num_knowledge', type=int, default=2)
@click.option('--top_p', default=0.5, type=float)
@click.option('--temperature', default=1.0, type=float)
@click.option('--max_tokens', default=40, type=int)
@click.option('--start', default=None, type=int)
@click.option('--end', default=None, type=int)
@click.option('--engine', default='davinci', type=str)
@click.option('--desc/--not-desc', default=False)
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
    desc: bool
):
    assert end > start
    data = load_data(input_path, 'jsonl')
    data = data[start:end]

    with open(output_path, 'a') as fo:
        for item in tqdm(data, total=end-start):
            question = item['input_sentence']
            if 'description' not in item:
                item['description'] = []
            concepts = item['generated_result'].split(';')
            concepts = [concept.replace('.', '').strip() for concept in concepts]
            if 'parents' in concepts:
                concepts.remove('parents')
            for concept in concepts:
                context_string = prompt_format(
                    prompt_path,
                    concept=concept,
                    query=question
                )
                try:
                    knowledges = request(context_string,engine=engine,n=num_knowledge,
                        top_p=top_p,temperature=temperature,max_tokens=max_tokens)
                    generate_result = list(set(knowledges))
                    if len(generate_result) >= 1:
                        temp = f"{concept}: {generate_result[0]}"
                        item['description'].append(temp)
                except:
                    print(f'error in ')
                    exit()
            temp = json.dumps(item)
            fo.write(temp + '\n')
            fo.flush()

if __name__ == '__main__':
    main()

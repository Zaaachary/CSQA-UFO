# -*- encoding: utf-8 -*-
'''
@File    :   gpt3_fewshot.py
@Time    :   2022/12/01 15:01:58
@Author  :   Zhifeng Li
@Contact :   li_zaaachary@163.com
@Desc    :   
'''
import sys
import os
from math import ceil
import argparse
import logging
import json
from copy import deepcopy
from collections import OrderedDict

from tqdm import tqdm
import openai

logging.basicConfig(level=logging.INFO)  
logger = logging.getLogger('')
current_path = sys.path[0]
sys.path.append(os.path.join(current_path, '../tools'))

from gpt3_util import completion_request, chat_request
from data_utils import load_data, dump_data


def clean_dialog(dialog, experiment):
    pure_dialog = dialog.replace('agen:','').replace('pelanggan:', '')
    length_raw = len(pure_dialog.split())

    # formated_dialog = dialog.replace("1:", 'agen:').replace("2:", "pelanggan:")
    formated_dialog = dialog.replace('Akulaku', 'alibaba').replace('akulaku', 'alibaba')
    if 'add_dot' in experiment:
        formated_dialog = formated_dialog.replace('\n', '.\n')
    if 'AB' in experiment:
        formated_dialog = formated_dialog.replace('pelanggan', 'B').replace('agen', 'A')

    return length_raw, formated_dialog
    

def format_input(data, task_type, experiment):
    result = []
    for item in data:
        item['gpt3_input'] = []
        item_dict = {}
        dialog = item['dialog'] if 'dialog' in item else item['dialog_concat']
        length_raw, formated_dialog = clean_dialog(dialog, experiment)
        item_dict['dialog'] = formated_dialog
        item['gpt3_input'] = item_dict
        result.append(item.copy())
    return result

def load_prompt(prompt_path):
    message_list = load_data(prompt_path, 'json')
    return message_list

def format_output(task_type, item, gen_result):
    if task_type == 'summary':
        item['summary'] = gen_result[0].replace('alibaba', 'akulaku').replace('Alibaba', 'akulaku')
    else:
        raise Exception('Not Implemented.')
    
    item.pop('gpt3_input')
    return item

def main(args):
    if args.proxy:
        openai.proxy = args.proxy
    # example load
    start, end = args.start_idx, args.end_idx
    data = load_data(args.input_path, 'jsonl')
    if end != -1:
        assert start < end
        data = data[start:end]
    else:
        data = data[start:]
    data = format_input(data, args.task_type, args.experiment)
    # prompt load
    message_list = load_prompt(args.prompt_path)

    f = open(args.output_path, 'a')
    # few-shot loop
    for idx, item in enumerate(tqdm(data)):
        temp_message = deepcopy(message_list)
        for message in temp_message:
            message['content'] = message['content'].format(**item['gpt3_input'])
        if idx == 0:
            print('example:', temp_message)
        try:
            gen_result = chat_request(
                temp_message,
                engine=args.engine,
                n=args.output_num,
                top_p=args.top_p,
                temperature=args.temperature,
                frequency_penalty=args.frequency_penalty,
                max_tokens=args.max_tokens
                )
        except Exception as e:
            logger.warning(f"exception in {start} + {idx}: {temp_message}")
            logger.warning(e)
            f.close()
            exit()
        
        output_item = format_output(args.task_type, item, gen_result)
        output_str = json.dumps(output_item)
        f.write(output_str + '\n')
        f.flush()
        
    f.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    
    parser.add_argument("--task_type", type=str, choices=['summary', 'call_result', 'refuse'])
    parser.add_argument("--input_path", type=str, default=None)
    parser.add_argument("--prompt_path", type=str, default=None)
    parser.add_argument("--output_path", type=str, default=None)
    parser.add_argument("--start_idx", type=int, default=0)
    parser.add_argument("--end_idx", type=int, default=-1)
    
    parser.add_argument('--engine', default='text-davinci-003', type=str, choices=['text-davinci-003', 'gpt-3.5-turbo', 'curie', 'ada'])
    parser.add_argument("--proxy", type=str, default='', help='http://127.0.0.1:1,080')
    parser.add_argument("--output_num", type=int, default=1)
    parser.add_argument("--top_p", default=1, type=float)
    parser.add_argument('--temperature', default=1.0, type=float)
    parser.add_argument('--frequency_penalty', default=0.0, type=float)
    
    parser.add_argument("--max_tokens", default=40, type=int)
    parser.add_argument("--experiment", type=str, default='')
    
    args = parser.parse_args()
    main(args)

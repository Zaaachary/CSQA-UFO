# -*- encoding: utf-8 -*-
'''
@File    :   gpt3_fewshot.py
@Time    :   2022/12/01 15:01:58
@Author  :   Zhifeng Li
@Contact :   li_zaaachary@163.com
@Desc    :   
'''
import argparse
import logging
import json
import time
import sys
from collections import OrderedDict

from tqdm import tqdm
from transformers import GPT2Tokenizer, GPT2LMHeadModel, GPTNeoForCausalLM


sys.path.append('../../Tools')
from data_utils import load_data, dump_data


logging.basicConfig(level=logging.INFO)  
logger = logging.getLogger('')

MODEL_DICT = {
    'gpt2': (GPT2Tokenizer, GPT2LMHeadModel),
    'gpt-neo': (GPT2Tokenizer, GPTNeoForCausalLM)
}



def format_prompt(prompt: str, query: str, concept=''):
    if concept is not None:
        context_string = context_string.replace('{concept}', concept)
    if query is not None:
        context_string = context_string.replace('{question}', query)
    return context_string

def format_question(data, data_type):    
            
    data = data.strip()
    if data[-1].isalpha():
        data = data + '.'
        
    return data

def format_input(data, data_type, task_type, args):
    result = []
    for item in data:
        
        item['model_input'] = []
        item_dict = {}
        # get question
        if data_type in ['csqa2', 'unified', 'ptqa_u']:
            question = item['question']
        elif data_type in ['csqa', 'obqa', 'qasc']:
            question = item['question']['stem']
            choice_list = []
            for choice in item['question']['choices']:
                choice_str = f"{choice['label']}. {choice['text']}"
                choice_list.append(choice_str)
            choice_str = '\n'.join(choice_list)            
        elif data_type == 'siqa':
            question = item['context'] + ' ' + item['question']
            choice_list = []
            for key in ['answerA', 'answerB', 'answerC']:
                choice_list.append(item[key])
            choice_str = '\n'.join(choice_list)
            
        if data_type == 'unified':
            cur_data_type = item['data_type']
        else:
            cur_data_type = data_type
        
        question = format_question(question, cur_data_type)
        item['transformed_question'] = question
        item_dict['question'] = question
        # get key points
        if 'description' in task_type:
            keypoints = item.get("keypoints", [])
            assert len(keypoints) >= 1
            for key_point in keypoints[:args.max_description_num]:
                temp_dict = item_dict.copy()
                temp_dict['key_point'] = key_point
                item['model_input'].append(temp_dict)     
        elif 'qa' in task_type:
            if data_type in ['qasc', 'csqa', 'siqa', 'obqa']:
                item_dict['choices'] = choice_str
            if 'facts' in task_type:
                item_dict['facts'] = item['facts'][0]
            item['model_input'].append(item_dict)
        else:
            item['model_input'].append(item_dict)
        result.append(item.copy())
    return result

def load_prompt(prompt_path):
    f = open(prompt_path, 'r')
    prompt = f.read().strip('\n')
    return prompt

def format_output(task_type, data_type, item, model_output):
    if task_type == 'keypoints':
        gen_result = model_output[0][0].strip()
        if gen_result[-1] == '.':
            gen_result = gen_result[:-1]
        gen_result = [key.strip() for key in gen_result.split(';')]
    elif task_type == "description":
        keypoint_list = []
        for input_item, gen_result in zip(item['model_input'], model_output):
            keypoint = input_item['key_point']
            description = gen_result[0]
            keypoint_list.append([keypoint, description])
        gen_result = keypoint_list
    elif task_type == "facts":
        gen_result = model_output[0]
        for idx, temp in enumerate(gen_result):
            gen_result[idx] = temp.split('\n\n')[0].strip()
    
    elif task_type in ['qa','qa_facts']:
        gen_result = model_output[0][0].strip()
        if data_type == 'csqa2':
            gen_result = gen_result.replace('.','').strip()
        else:
            gen_result = gen_result.split('.')[0] 
    else:
        raise Exception('no match task_type')
    
    item.pop('model_input')
    item[task_type] = gen_result

    return item

def generate(args, context_string, model, tokenizer):
    input_ids = tokenizer.encode(context_string, return_tensors='pt')
    seq_len = len(input_ids[0])
    input_ids = input_ids.to(args.device)
    
    total_output = []
    for _ in range(args.output_num):
        output = model.generate(
            input_ids,
            max_length=seq_len + args.max_tokens,
            do_sample=True,
            num_beams=1,
            top_p=args.top_p,
            temperature=args.temperature
        )
        total_output.append(output[0])
    
    result = []
    for item in total_output:
        result.append(tokenizer.decode(item[seq_len:]))
    
    return result
    

def main(args):
    # model load
    tokenizer_class, model_class = MODEL_DICT[args.model_type]
    tokenizer = tokenizer_class.from_pretrained(args.model_path)
    model = model_class.from_pretrained(args.model_path)
    model.eval()
    model.to(args.device)
    
    # example load
    start, end = args.start_idx, args.end_idx
    data = load_data(args.input_path, 'jsonl')
    if end != -1:
        assert start < end
        data = data[start:end]
    else:
        data = data[start:]
    data = format_input(data, args.data_type, args.task_type, args)
    # prompt load
    prompt = load_prompt(args.prompt_path)
    print(prompt)
    
    f = open(args.output_path, 'a')
    # few-shot loop
    for idx, item in enumerate(tqdm(data)):
        input_list = item['model_input']
        model_output = []
        for model_input in input_list:
            context_string = prompt.format(**model_input)
            # try:
            gen_result = generate(args, context_string, model, tokenizer)
            # except:
                # logger.warning(f"exception in {start} + {idx}: {item}")
                # f.close()
                # exit()
            model_output.append(gen_result)
        output_item = format_output(args.task_type, args.data_type, item, model_output)
        output_str = json.dumps(output_item)
        f.write(output_str + '\n')
        f.flush()
        
    f.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    
    parser.add_argument("--task_type", type=str, choices=['qa', 'qa_facts', 'qa_desc', 'facts', 'description', 'keypoints'])
    parser.add_argument("--data_type", type=str, choices=['obqa', 'qasc', 'csqa', 'ptqa', 'ptqa_u', 'csqa2', 'unified', 'siqa'])
    
    parser.add_argument("--input_path", type=str, default=None)
    parser.add_argument("--prompt_path", type=str, default=None)
    parser.add_argument("--output_path", type=str, default=None)
    parser.add_argument("--start_idx", type=int, default=0)
    parser.add_argument("--end_idx", type=int, default=-1)
    parser.add_argument("--max_description_num", type=int, default=0)
    
    parser.add_argument('--model_type', type=str, default='gpt-neo')
    parser.add_argument('--model_path', type=str)
    parser.add_argument("--output_num", type=int, default=1)
    parser.add_argument("--top_p", default=1, type=float)
    parser.add_argument('--temperature', default=1.0, type=float)
    parser.add_argument("--max_tokens", default=128, type=int)
    parser.add_argument("--device", default='cuda:3')
    
    args = parser.parse_args()
    main(args)

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
from collections import OrderedDict

from tqdm import tqdm
from copy import deepcopy

from gpt3_generation import completion_request, chat_request
from utils import load_data, dump_data, STOP_WORDS


logging.basicConfig(level=logging.INFO)  
logger = logging.getLogger('')


def transform_question(origin):
    '''
    > after having kids name something that happens that interrupts a couples alone time at night

    > after having kids one thing that happens that interrupts a couples alone time at night is

    '''
    question = origin.lower()
    question = question.replace('.', '')
    question = question.replace(':', '')
    question = question.replace('?', '')
    question = question.replace('someone', 'one person')
    question = question.replace('someplace', 'one place')
    transform_dict = {
        "name something": "one thing",
        'tell me something': 'one thing',
        'name a ': 'one ',
        "name an ": "one ",
        "name": "",
        "name ": "",
        "SW tell me a ": "one ",
        "SW tell me an ": "one ",
        "SW what": "one",
        "SW give me a ": "one ",
        "SW tell me ": "",
        "which": "one",
        "what": "one",
        "how can you tell": "one way to tell",
    }
    order = ['name something', 'tell me something', 'name a ', 'name an ', 'name',
        'SW tell me a ', 'SW tell me an ', 'SW what', 'SW give me a ', 'SW tell me ',
        'which', 'what', 'how can you tell']
    transform = OrderedDict.fromkeys(order)
    transform.update(transform_dict)

    for pattern, trans in transform.items():
        if pattern.startswith('SW') and pattern[3:] in question:
            question = question.replace(pattern[3:], trans)
            question = question.strip() + ' is'
            break
        elif pattern in question:
            question = question.replace(pattern, trans)
            question = question.strip() + ' is'
            break

    question = question[0].upper() + question[1:] + ' what?'

    return question

def format_prompt(prompt: str, query: str, concept=''):
    if concept is not None:
        context_string = context_string.replace('{concept}', concept)
    if query is not None:
        context_string = context_string.replace('{question}', query)
    return context_string

def format_question(data, data_type):    
    
    data = data.strip()
    if data_type in ['ptqa', 'ptqa_u']:
        data = transform_question(data)
    elif data_type == 'csqa2':
        if data[-1] not in ['.', '?', '!']:
            data = data + '.'
            
    data = data.strip()
    if data[-1].isalpha():
        data = data + '.'
        
    return data

def clean_keywords(keywords):
    result = []
    for keyword in keywords:
        if keyword in STOP_WORDS:
            print(keyword)
            continue        

        result.append(keyword)
            
    return result
    

def format_input(data, data_type, task_type, args):
    result = []
    for item in data:
        
        item['gpt3_input'] = []
        item_dict = {}
        # get question
        if data_type == "ptqa": 
            question = item['question']['normalized'].strip().capitalize()
        elif data_type in ['csqa2', 'unified', 'ptqa_u']:
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
                item['gpt3_input'].append(temp_dict)     
        elif 'qa' in task_type:
            if data_type in ['qasc', 'csqa', 'siqa', 'obqa']:
                item_dict['choices'] = choice_str
            if 'facts' in task_type:
                item_dict['facts'] = item['facts'][0]
            item['gpt3_input'].append(item_dict)
        else:
            item['gpt3_input'].append(item_dict)
        result.append(item.copy())
    return result

def load_prompt(engine, prompt_path):
    if engine == 'gpt-3.5-turbo':
        message_list = load_data(prompt_path, 'json')
        return message_list
    else:
        f = open(prompt_path, 'r')
        prompt = f.read().strip('\n')
        return prompt

def format_output(task_type, data_type, item, gpt3_output):
    if task_type == 'keypoints':
        gen_result = gpt3_output[0][0].strip()
        if gen_result[-1] == '.':
            gen_result = gen_result[:-1]
        gen_result = [key.strip() for key in gen_result.split(';')]
    elif task_type == "description":
        keypoint_list = []
        for input_item, gen_result in zip(item['gpt3_input'], gpt3_output):
            keypoint = input_item['key_point']
            description = gen_result[0]
            keypoint_list.append([keypoint, description])
        gen_result = keypoint_list
    elif task_type == "facts":
        gen_result = gpt3_output[0]    
    
    elif task_type in ['qa','qa_facts']:
        gen_result = gpt3_output[0][0].strip()
        if data_type == 'csqa2':
            gen_result = gen_result.replace('.','').strip()
        else:
            gen_result = gen_result.split('.')[0] 
    else:
        raise Exception('no match task_type')
    
    item.pop('gpt3_input')
    item[task_type] = gen_result

    return item

def main(args):
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
    prompt = load_prompt(args.engine, args.prompt_path)
    print(prompt)
    
    f = open(args.output_path, 'a')
    # few-shot loop
    for idx, item in enumerate(tqdm(data)):
        input_list = item['gpt3_input']
        gpt3_output = []
        for gpt3_input in input_list:
            try:
                if args.engine == "gpt-3.5-turbo":
                    temp_message = deepcopy(prompt)
                    for message in temp_message:
                        message['content'] = message['content'].format(**gpt3_input)
                    gen_result = chat_request(
                        temp_message,
                        engine=args.engine,
                        n=args.output_num,
                        top_p=args.top_p,
                        temperature=args.temperature,
                        frequency_penalty=args.frequency_penalty,
                        max_tokens=args.max_tokens
                        )
                    # import pdb; pdb.set_trace()
                else:
                    context_string = prompt.format(**gpt3_input)
                    gen_result = completion_request(
                        context_string,
                        engine=args.engine,
                        n=args.output_num,
                        top_p=args.top_p,
                        stop="\n\n\n",
                        temperature=args.temperature,
                        frequency_penalty=args.frequency_penalty,
                        max_tokens=args.max_tokens
                        )
            except:
                logger.warning(f"exception in {start} + {idx}: {item}")
                f.close()
                exit()
            gpt3_output.append(gen_result)
        output_item = format_output(args.task_type, args.data_type, item, gpt3_output)
        output_str = json.dumps(output_item)
        f.write(output_str + '\n')
        f.flush()
        
    f.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    
    parser.add_argument("--proxy", type=str, default=None)
    parser.add_argument("--task_type", type=str, choices=['qa', 'qa_facts', 'qa_desc', 'facts', 'description', 'keypoints'])
    parser.add_argument("--data_type", type=str, choices=['obqa', 'qasc', 'csqa', 'ptqa', 'ptqa_u', 'csqa2', 'unified', 'siqa'])
    parser.add_argument("--input_path", type=str, default=None)
    parser.add_argument("--prompt_path", type=str, default=None)
    parser.add_argument("--output_path", type=str, default=None)
    parser.add_argument("--start_idx", type=int, default=0)
    parser.add_argument("--end_idx", type=int, default=-1)
    parser.add_argument("--max_description_num", type=int, default=0)
    
    parser.add_argument('--engine', default='davinci', type=str, choices=['davinci', 'text-curie-001', 'ada', "text-davinci-003", 'gpt-3.5-turbo'])
    parser.add_argument("--output_num", type=int, default=1)
    parser.add_argument("--top_p", default=1, type=float)
    parser.add_argument('--temperature', default=1.0, type=float)
    parser.add_argument('--frequency_penalty', default=0.0, type=float)
    
    parser.add_argument("--max_tokens", default=40, type=int)
    parser.add_argument("--slow", action="store_true")
    
    # --prompt_path /SISDC_GPFS/Home_SE/hy-suda/zfli/CODE/Project-Final/Few-shot_learning/GPT3_fewshot/Prompts/ProtoQA/ptqa_qa_v3.txt
    # --input_path /SISDC_GPFS/Home_SE/hy-suda/zfli/CODE/Project-Final/Data/Raw_data/ProtoQA/origin/test.questions.jsonl
    args_str = """
    --task_type qa_desc
    --data_type protoqa
    --prompt_path /SISDC_GPFS/Home_SE/hy-suda/zfli/CODE/Project-Final/Few-shot_learning/GPT3_fewshot/Prompts/ProtoQA/ptqa_qa_desc_v3.3.txt
    --input_path /SISDC_GPFS/Home_SE/hy-suda/zfli/CODE/Project-Final/Data/Constructed_data/ProtoQA/Few-shot_description/protoqa_v3_curie/fewshot_description_v1/dev.crowdsourced.jsonl
    --output_path /SISDC_GPFS/Home_SE/hy-suda/zfli/CODE/Project-Final/Data/Constructed_data/ProtoQA/Few-shot_QA/desc_QA/dev.v3.3.jsonl
    --start_idx 0
    --end_idx -1
    --frequency_penalty 0.0
    --engine davinci
    --output_num 1
    --max_tokens 64
    """
    # args = parser.parse_args(args_str.split())
    args = parser.parse_args()
    main(args)

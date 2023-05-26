import sys
import os
import random
import argparse
import logging
from collections import OrderedDict

sys.path.append("/SISDC_GPFS/Home_SE/hy-suda/zfli/CODE/Project-Final/Tools")
from data_io_util import load_data, dump_data

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# def append_knowledge(raw, knowledge, desc=False):
#     for o, k in zip(raw, knowledge):
#         if o['metadata']['id'] != k['idx']:
#             print(k['idx'])
#             exit()
#         if desc:
#             o['knowledge'] = '; '.join(k['description']).strip()
#         elif 'generated_result' in k:
#             o['knowledge'] = k['generated_result'].strip()
#         elif 'knowledges' in k:
#             # gpt-3 knowledge
#             try:
#                 o['knowledge'] = k['knowledges'][0].strip()
#             except:
#                 o['knowledge'] = ''
#         else:
#             raise Exception('error type')

def merge_description(args, raw, update):
    item_dict = dict()
    for item in update:
        idx = item['idx']
        concept = item['concept']
        description = item['description']
        
        temp_dict = item_dict.get(idx, OrderedDict())
        temp_dict[concept] = description
        item_dict[idx] = temp_dict

    for item in raw:
        if 'description' not in item:
            item['description'] = list()
            
        if args.data_type == 'csqa2':
            idx = item['id']
                
        if idx not in item_dict:
            continue
        update = item_dict[idx]
        
        for key, value in update.items():
            item['description'].append((key, value))
        
    return raw
    
def merge_facts(args, raw, update):
    assert len(raw) == len(update)
    
    for r, u in zip(raw, update):
        r['facts'] = u['facts']
        
    return raw
        

def main(args):
    target_list = os.listdir(args.data_path)
    try:
        os.makedirs(args.output_path)
    except:
        print('path exisit, continue? (Y/N)')
        if input().lower() != 'y':
            exit()
    
    for target in target_list:
        raw_path = os.path.join(args.data_path, target)
        if not os.path.isfile(raw_path):
            continue
        update_path = os.path.join(args.data_path_2, target)
        raw = load_data(raw_path, 'jsonl')
        update = load_data(update_path, 'jsonl')

        if args.task_type == 'desc':
            raw = merge_description(args, raw, update)
        elif args.task_type == 'facts':
            raw = merge_facts(args, raw, update)

        dump_data(raw, os.path.join(args.output_path, target), 'jsonl')
        


if __name__ == "__main__":
    random.seed(42)
    
    parser = argparse.ArgumentParser()
    
    parser.add_argument('--data_type', choices=['ptqa', 'csqa', 'csqa2'], required=True)
    parser.add_argument('--task_type', choices=['desc', 'keywords', 'facts'], required=True)
    
    parser.add_argument('--data_path', type=str, required=True, 
                        help='original data')
    parser.add_argument('--data_path_2', type=str, required=True, 
                        help='knowledge_path')
    parser.add_argument('--output_path', type=str, required=True)
    
    args_str = """
    --data_type ptqa
    --task_type facts
    --data_path /SISDC_GPFS/Home_SE/hy-suda/zfli/CODE/Project-Final/Data/Raw_data/ProtoQA/origin
    --data_path_2 /SISDC_GPFS/Home_SE/hy-suda/zfli/CODE/Project-Final/Data/Constructed_data/ProtoQA/Few-shot_facts_v2/ptqa.v2.3
    --output_path /SISDC_GPFS/Home_SE/hy-suda/zfli/CODE/Project-Final/Data/Constructed_data/ProtoQA/Few-shot_facts_v2/ptqa.v2.3.merged
    """
    args = parser.parse_args(args_str.split())
    print(args)
    main(args)
    
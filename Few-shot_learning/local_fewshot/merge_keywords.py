# -*- encoding: utf-8 -*-
'''
@File    :   merge_keywords.py
@Time    :   2022/10/30 22:21:20
@Author  :   Zhifeng Li
@Contact :   li_zaaachary@163.com
@Desc    :   
'''
import os
import random
from copy import deepcopy

from tqdm import tqdm

from data_io_util import load_data, dump_data

def clean_keyword(keywords, question=''):
    result = []
    for keyword in keywords:
        keyword = keyword.strip()
        if 'Input' in keyword:
            keyword = keyword.split('Input')[0].strip()
        # if len(keyword.split()) >= 3:
            # print(keyword)
            # continue
        if '\n' in keyword:
            keyword = keyword.split('\n')[0].strip()
        if keyword == '':
            continue
        if '_' in keyword:
            continue
        if keyword == 'A:':
            continue
        if len(keyword) ==3 :
            print(question, keywords, keyword)
        result.append(keyword)
    
    return result

def merge_data(generated_data, origin_data):
    merged_data = []
    for gen_item, ori_item in tqdm(zip(generated_data, origin_data)):
        keywords = gen_item['keywords']
        keywords = clean_keyword(keywords, gen_item['question'])
        idx = 0
        while idx < len(keywords):
            cur = keywords[idx]
            for idx_2 in range(len(keywords)-1, idx, -1):
                if cur == keywords[idx_2]:
                    keywords.pop(idx_2)
            idx += 1
            
        ori_item['keyword'] = keywords
        merged_data.append(deepcopy(ori_item))
    return merged_data

def construct_prefix_data(out_data, output_path):
    source = []
    target = []
    for oitem in out_data:
        question = oitem['question']['normalized']
        question = question[0].upper() + question[1:]
        keywords = oitem['keyword']
        # import pdb; pdb.set_trace()
        temp = []
        for item in keywords:
            item = item.split('\n')[0]
            item = item.strip()
            if item == 'A:':
                continue
            if '__' in item:
                continue
            if item == "":
                continue
            if len(item.split(' ')) > 5:
                continue
            if len(item) <= 2:
                continue
            temp.append(item)

        keywords = temp

        if len(keywords) == 0:
            continue
            
        keywords = '; '.join(keywords) + '.'
        source.append(question)
        target.append(keywords)
        
    random.seed(42)
    temp = [item for item in zip(source, target)]
    random.shuffle(temp)
    dev, train = temp[:500], temp[500:]
    
    dev_source = [item[0] for item in dev]
    dev_target = [item[1] for item in dev]
    dump_data(dev_source, os.path.join(output_path, 'dev.source'), 'plain')
    dump_data(dev_target, os.path.join(output_path, 'dev.target'), 'plain')
    train_source = [item[0] for item in train]
    train_target = [item[1] for item in train]
    dump_data(train_source, os.path.join(output_path, 'train.source'), 'plain')
    dump_data(train_target, os.path.join(output_path, 'train.target'), 'plain')
    
    


if __name__ == "__main__":
    source_root = "/SISDC_GPFS/Home_SE/hy-suda/zfli/CODE/Project-Final/Data/Raw_data/ProtoQA/origin/"
    target_root = "/SISDC_GPFS/Home_SE/hy-suda/zfli/CODE/Project-Final/Data/Constructed_data/ProtoQA/Few-shot_keywords_GPT-neo/version_8_full/"
    output_root = "/SISDC_GPFS/Home_SE/hy-suda/zfli/CODE/Project-Final/Data/Constructed_data/ProtoQA/Few-shot_keywords_GPT-neo/version_8_merge/"
    if not os.path.exists(output_root):
        os.mkdir(output_root)

    total_data = []
    for cur_data in os.listdir(target_root):
        if not cur_data.endswith('.jsonl'):
            continue
        sus_path = os.path.join(source_root, cur_data)
        tgt_path = os.path.join(target_root, cur_data)
        out_path = os.path.join(output_root, cur_data)
        sus_data = load_data(sus_path, 'jsonl')
        
        tgt_data = load_data(tgt_path, 'jsonl')

        out_data = merge_data(tgt_data, sus_data)
        
        dump_data(out_data, out_path, 'jsonl')
        total_data.extend(out_data)
    # import pdb; pdb.set_trace()
    try:
        os.mkdir(os.path.join(output_root, 'sce_tgt'))
    except:
        pass
    construct_prefix_data(total_data, os.path.join(output_root, 'sce_tgt'))
        
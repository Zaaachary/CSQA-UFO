# -*- encoding: utf-8 -*-
'''
@File    :   data_format.py
@Time    :   2022/10/28 20:27:31
@Author  :   Zhifeng Li
@Contact :   li_zaaachary@163.com
@Desc    :   

{
        "query": "A revolving door is convenient for two direction travel, but it also serves as a security measure at a what?",
        "cands": [
            "bank",
            "library",
            "department store",
            "mall",
            "new york"
        ],
        "answer": "bank"
    },
'''
import os


from utils import load_data, dump_data


def format_data(data):
    result = []
    for item in data:
        temp = dict()
        idx = item['metadata']['id']
        query = item['question']['normalized'].strip()
        query = query[0].upper() + query[1:]        
        temp['id'] = idx
        temp['query'] = query
        result.append(temp)
    
    return result


if __name__ == "__main__":
    dataset_path = "/SISDC_GPFS/Home_SE/hy-suda/zfli/CODE/Project-Final/Data/Raw_data/ProtoQA/with_keyword_v1_dpr"
    output_root = "/SISDC_GPFS/Home_SE/hy-suda/zfli/CODE/Project-Final/Data/Constructed_data/ProtoQA/Few-shot_version"
    for cur_path in os.listdir(dataset_path):
        data_path = os.path.join(dataset_path, cur_path)
        output_path = os.path.join(output_root, cur_path)
        # import pdb; pdb.set_trace()
        data = load_data(data_path, 'jsonl')
        data = format_data(data)
        dump_data(data, output_path, 'json')
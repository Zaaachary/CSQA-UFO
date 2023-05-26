# -*- encoding: utf-8 -*-
'''
@File    :   acc_compute.py
@Time    :   2023/04/16 10:41:27
@Author  :   Zhifeng Li
@Contact :   li_zaaachary@outlook.com
@Desc    :   
'''
import json
import os

TARGET = "D:\Project\CSQA-UFO\Constructed_data\QASC\gpt-3-qa"

for file_name in os.listdir(TARGET):
    with open(os.path.join(TARGET, file_name), 'r') as f:
        content = f.readlines()

    total_count = len(content)
    correct = 0
    for line in content:
        line = json.loads(line)
        if 'qa' in line:
            # if len(line['qa']) > 1:
            #     total_count -= 1
            #     continue
            if line['qa'] == line['answerKey']:
                correct += 1
        elif 'qa_facts' in line:
            # if len(line['qa_facts']) > 1:
            #     total_count -= 1
            #     continue
            if line['qa_facts'] == line['answerKey']:
                correct += 1
    print(file_name)
    print(correct, total_count, correct / total_count)


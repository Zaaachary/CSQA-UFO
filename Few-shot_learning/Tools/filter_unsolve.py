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

# TARGET = "D:\Project\CSQA-UFO\Constructed_data\QASC\gpt-3-qa\dev.chat.2.jsonl"
# OUTPUT = "D:\Project\CSQA-UFO\Constructed_data\QASC\gpt-3-qa\dev.chat.filter.2.jsonl"

# f = open(TARGET, 'r')
# content = []

# for line in f.readlines():
#     jline = json.loads(line)
#     if len(jline['qa']) > 1:
#         content.append(line)


# f = open(OUTPUT, 'w')
# for item in content:
#     f.write(item)

# Merge
TARGET_1 = "D:\Project\CSQA-UFO\Constructed_data\QASC\gpt-3-qa\dev.chat.2.jsonl"

TARGET_2 = "D:\Project\CSQA-UFO\Constructed_data\QASC\gpt-3-qa\dev.chat.jsonl"

f = open(TARGET_1, 'r')
data_1 = f.readlines()
f = open(TARGET_2, 'r')
data_2 = f.readlines()

data_dict = {}
for item in data_1:
    line = json.loads(item)
    data_dict[line['id']] = item

for idx, item in enumerate(data_2):
    json_line = json.loads(item)
    
    data_2[idx] = data_dict.get(json_line['id'], item)

f = open(TARGET_2+'1', 'w')
for line in data_2:
    f.write(line)
f.close()


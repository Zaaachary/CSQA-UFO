import os
import json
from collections import OrderedDict

def load_data(file_path, mode='plain'):
    '''
    load data from jsonl/tsf or plain
    mode: jsonl / tsf / plain
    '''
    result = []
    f = open(file_path, 'r', encoding='utf-8')

    if mode == 'json':
        result =  json.load(f, object_pairs_hook=OrderedDict)
    else:
        while True:
            line = f.readline()
            if not line:
                break
            if mode == 'jsonl':
                try:
                    jsonl_line = json.loads(line, object_pairs_hook=OrderedDict)
                except:
                    print(line)
                    raise Exception('error')
                result.append(jsonl_line)
            elif mode == 'tsf':
                line = line.strip('\n').split('\t')
                result.append(line)
            elif mode == 'plain':
                line = line.strip()
                result.append(line)
    f.close()
    return result


def dump_data(target, file_path, mode='json'):
    f = open(file_path, 'w', encoding='utf-8')
    if mode == 'json':
        json.dump(target, f, ensure_ascii=False, indent=2)
    elif mode == 'tsf':
        for line in target:
            line = list(map(str, line))
            f.write('\t'.join(line) + '\n')
    elif mode == 'jsonl':
        for line in target:
            line = json.dumps(line, ensure_ascii=False)
            f.write(line+'\n')
    elif mode == 'csv':
        for line in target:
            line = list(map(str, line))
            line = [item.replace(',',' ') for item in line]
            f.write(','.join(line) + '\n')
    elif mode == 'plain':
        for line in target:
            f.write(line + '\n')
            
    f.close()
def ensure_dir(d):
    if not os.path.exists(d):
        os.makedirs(d)


STOP_WORDS = ['i',  'me',  'my',  'myself',  'we',  'our',  'ours',  'ourselves',  'you',  "you're",  "you've",  "you'll",  "you'd",  'your',  'yours',  'yourself',  'yourselves',  'he',  'him',  'his',  'himself',  'she',  "she's",  'her',  'hers',  'herself',  'it',  "it's",  'its',  'itself',  'they',  'them',  'their',  'theirs',  'themselves',  'what',  'which',  'who',  'whom',  'this',  'that',  "that'll",  'these',  'those',  'am',  'is',  'are',  'was',  'were',  'be',  'been',  'being',  'have',  'has',  'had',  'having',  'do',  'does',  'did',  'doing',  'a',  'an',  'the',  'and',  'but',  'if',  'or',  'because',  'as',  'until',  'while',  'of',  'at',  'by',  'for',  'with',  'about',  'against',  'between',  'into',  'through',  'during',  'before',  'after',  'above',  'below',  'to',  'from',  'up',  'down',  'in',  'out',  'on',  'off',  'over',  'under',  'again',  'further',  'once',  'here',  'there',  'when',  'where',  'why',  'how',  'all',  'any',  'both',  'each',  'few',  'more',  'most',  'other',  'some',  'such',  'no',  'nor',  'not',  'only',  'own',  'same',  'so',  'than',  'too',  'very',  's',  't',  'can',  'will',  'just',  'don',  "don't",  'should',  "should've",  'd',  'll',  'm',  'o',  're',  've',  'y',  'ain',  'aren',  "aren't",  'couldn',  "couldn't",  'didn',  "didn't",  'doesn',  "doesn't",  'hadn',  "hadn't",  'hasn',  "hasn't",  'haven',  "haven't",  'isn',  "isn't",  'ma',  'mightn',  "mightn't",  'mustn',  "mustn't",  'needn',  "needn't",  'shan',  "shan't",  'shouldn',  "shouldn't",  'wasn',  "wasn't",  'weren',  "weren't",  'won',  "won't",  'wouldn',  "wouldn't", 'true', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']

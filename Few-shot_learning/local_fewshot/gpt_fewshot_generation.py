# -*- encoding: utf-8 -*-
'''
@File    :   gpt2_keyword_generation.py
@Time    :   2022/09/18 12:42:17
@Author  :   Zhifeng Li
@Contact :   li_zaaachary@163.com
@Desc    :   extract keywords from question by gpt2-fewshot learning
'''
import os
from collections import OrderedDict
from tqdm import tqdm
from transformers import GPT2LMHeadModel, GPT2Tokenizer
from transformers import GPTNeoForCausalLM


from data_io_util import load_data, dump_data


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
        # "name ": "",
        # "name another ": "another ",
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
            question = question.strip() + ' is what ? '
            break
        elif pattern in question:
            question = question.replace(pattern, trans)
            question = question.strip() + ' is what ? '
            break
    else:
        question = 'Q: ' + question +'?'

    question = question[0].upper() + question[1:]

    return question

def protoqa_question(data):
    questions = []
    for item in data:
    # for item in data[:10]:
        question = item['question']['normalized'].strip()
        question = question[0].upper() + question[1:]
        questions.append(question)
    
    return questions

def template_selection(template_type, tokenizer):
    if template_type == 'keyword':
        template_list = [
            "Extract key concepts from input.",
            "Input: Instead of walking, name a way to get around in snowy weather. Output: get around; snowy weather.",
            "Input: Name something you drink out of the bottle. Output: drink; bottle.",
            "Input: What are some things that people send by email that they used to send through the mail? Output: email; mail",
            "Input: Name a european country. Output: european country.",
            "Input: At the beach, name something that might protect you from sun. Output: beach; sun protection.",
            "Input: What could be some of the reasons you could be called to your kid's school? Output: kid's school",
            "Input: Name a sport that requires a lot of equipment. Output: sport; equipment.",
            "Input: At what age does it become embarrassing to still live with your parents? Output: embarrassing; live with parents.",
            "Input: Name a food people stir while it's cooking. Output: stir while cooking; cooking food",
            "Input: If a business woman were retiring, name something she'd be thrilled to never have to wear again. Output: business woman; retiring. ",
            "Input: {} Output: "
        ]
        template = "\n".join(template_list)
    elif template_type == 'knowledge':
        template_list = [
        # "Input: Name something that has been replaced by Google Maps and other highway and street GPS services. Knowledge: Electronic maps are the modern version of paper atlas.",
        # " Input: The fox walked from the city into the forest, name something that it is looking for.  Knowledge: Natural habitats are usually away from cities. ",
        # " Input: Name something that allow you share files with someone when you have connection with it. Knowledge: Files can be shared over the Internet. ",
        # " Input: Too many people want exotic snakes. Name something that causes the driving demand. Knowledge: Some people raise snakes as pets. ",
        # " Input: The body guard was good at his duties, name something that his employer gains. Knowledge: The job of body guards is to ensure the safety and security of the employer. ",
        # v1
        "Input: at the beach, name something that might protect you from sun. Knowledge: Protect means to prevent harm coming to; Sun sustains life but it can be the worst enemy of skin.",
        "Input: besides a waiter, name a job at a restaurant. Knowledge: restaurant is an eating establishment in which diners are served food; waiter is a male or female attendant who serves customers.",
        "Input: besides plastic surgery, name something women can do to dramatically change her appearance. Knowledge: plastic surgery is a branch of surgery concerned with improving the appearance of body through reconstructive.",
        "Input: besides a waiter, name a job at a restaurant. Knowledge: restaurant is an eating establishment in which diners are served food; waiter is a male or female attendant who serves customers.",
        "Input: besides plastic surgery, name something women can do to dramatically change her appearance. Knowledge: plastic surgery is a branch of surgery concerned with improving the appearance of body through reconstructive.",
        # "[]",
        "Input: {} Knowledge: "
        ]
        template = " ".join(template_list)
    elif template_type == 'siqa':
        template_list = [
            "Jan needed to give out jobs for an upcoming project at work. What will others want to do next? Answer: Others may get to work.",
            "Remy was an expert fisherman and was on the water with Kai. Remy baited Kai's hook. What will Remy want to do next? Answer: Remy may cast the line.",
            "Addison gave a hug to Skylar's son when they were feeling down. Why did Addison do this? Answer: Addison wants Skylar's son feel better.",
            "Kendall worked the weekend at the steakhouse and made bank on tips. Answer: Addison wants Skylar's son feel better.",
            "{} Answer: "
        ]
        template = " ".join(template_list)
    return template

def generate(questions, template, template_type, model, tokenizer, device):
    
    result = []
    for question in tqdm(questions):
            
        print(question)
        input_str = template.format(question)
        input_ids = tokenizer.encode(input_str, return_tensors = 'pt')
        seq_len = len(input_ids[0])
        input_ids = input_ids.to(device)
        output = model.generate(input_ids, max_length=seq_len + 10, num_beams=5, num_return_sequences=5, do_sample=False, top_k=20)
        # output = model.generate(input_ids, max_length=seq_len + 15, num_beams=1, num_return_sequences=2, do_sample=True, top_k=20, top_p=0.01, bad_words_ids=[[220]])
        if template_type == 'keyword':
            keywords = []
            for item in output:
                keywords.append(tokenizer.decode(item[seq_len:]))
            # keywords = keywords.strip().split(';')
            # keywords = list(set(keywords))
            temp = {"question": question, 'keywords': keywords}
        elif template_type == 'knowledge':
            knowledge = []
            for item in output:
                knowledge.append(tokenizer.decode(item[seq_len:]))
            temp = {"question": question, 'knowledge': knowledge}
        elif template_type == 'siqa':
            siqa_result = []
            for item in output:
                siqa_result.append(tokenizer.decode(item[seq_len:]))
            temp = {"question": question, 'result': siqa_result}
        
        
        result.append(temp)
        
    return result


def select_model(model_name):
    if model_name == 'gpt2':
        gpt2_path = "/SISDC_GPFS/Home_SE/hy-suda/zfli/Models/init_model/gpt2-large"
        tokenizer = GPT2Tokenizer.from_pretrained(gpt2_path)
        model = GPT2LMHeadModel.from_pretrained(gpt2_path)
    elif model_name == 'gpt-neo':
        neo_path = "/SISDC_GPFS/Home_SE/hy-suda/pre-train_model/gpt-neo-2.7B"
        tokenizer = GPT2Tokenizer.from_pretrained(neo_path)
        model = GPTNeoForCausalLM.from_pretrained(neo_path)
    return model, tokenizer

def clean_keyword(data):
    result = []
    for item in data:
        item['origin'] = item['keywords']
        keywords = ''
        for sentence in item['origin']:
            temp = sentence.split('Input:')[0].strip()
            if temp != '':
                keywords = temp
                break
        keywords = keywords.replace('.', '')
        item['keywords'] = keywords.split(';')
        result.append(item)
    return result
    

if __name__ == "__main__":
    # gpt2_path = "/SISDC_GPFS/Home_SE/hy-suda/zfli/Models/init_model/gpt2-medium"
    template_type = 'keyword'
    full_generation = True
    data_path = "/SISDC_GPFS/Home_SE/hy-suda/zfli/CODE/Project-Final/Data/Raw_data/ProtoQA/with_keyword_v1_dpr/"
    # data_path = "/SISDC_GPFS/Home_SE/hy-suda/zfli/CODE/Research/DATA/siqa/dev.jsonl"
    output_path = f"/SISDC_GPFS/Home_SE/hy-suda/zfli/CODE/Project-Final/Data/Constructed_data/ProtoQA/Few-shot_keywords_GPT-neo/"
    # output_path = "/SISDC_GPFS/Home_SE/hy-suda/zfli/CODE/Research/output_knowledge.jsonl"
    device = 'cuda:0'
    
    version = '8'
    if full_generation:
        output_path = os.path.join(output_path, f'version_{version}_full/')
    else:
        output_path = os.path.join(output_path, f'version_{version}/')
    
    if not os.path.exists(output_path):
        os.mkdir(output_path)
    
    model, tokenizer = select_model('gpt-neo')
    
    model.to(device)
    model.eval()
    
    if not full_generation:
        target = ['dev.crowdsourced.jsonl']
    else:
        target = os.listdir(data_path)


    for tgt in target:
        cur_path = os.path.join(data_path, tgt)
        data = load_data(cur_path, 'jsonl')
        questions = protoqa_question(data)
        template = template_selection(template_type=template_type, tokenizer=tokenizer)
        result = generate(questions, template, template_type, model, tokenizer, device)
        if template_type == 'keyword':
            result = clean_keyword(result)
        
        dump_data(result, os.path.join(output_path, tgt), 'jsonl')
        
    dump_data([template,], os.path.join(output_path, 'template.txt'), 'plain')
    
    
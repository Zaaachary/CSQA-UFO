import openai
from typing import List
from API_KEY import OPENAI_API_KEY
from tqdm import tqdm

openai.api_key = OPENAI_API_KEY

def completion_request(
    prompt: str,
    engine='davinci',
    max_tokens=60,
    temperature=1.0,
    top_p=1.0,
    n=1,
    stop='',
    presence_penalty=0.0,
    frequency_penalty=0.0,
    max_retry_turn=5
    ):
    # retry request (handles connection errors, timeouts, and overloaded API)
    current_turn = 0
    while True:
        try:
            response = openai.Completion.create(
                model=engine,
                prompt=prompt,
                max_tokens=max_tokens,
                temperature=temperature,
                top_p=top_p,
                n=n,
                # stop=stop if stop else None,
                presence_penalty=presence_penalty,
                frequency_penalty=frequency_penalty,
            )
            break
        except Exception as e:
            if current_turn == max_retry_turn:
                print('reach max quote.')
                exit(0)
            else:
                current_turn += 1
                tqdm.write(str(e))
                tqdm.write("Retrying...")
                import time
                time.sleep(30)
    
    generations = [gen['text'].lstrip() for gen in response['choices']]
    generations = [_ for _ in generations if _ != '']
    return generations


def chat_request(
    message_list,
    engine='',
    max_tokens=60,
    temperature=1.0,
    top_p=1.0,
    n=1,
    stop='',
    presence_penalty=0.0,
    frequency_penalty=0.0,
    max_retry_turn=5
    ):
    # retry request (handles connection errors, timeouts, and overloaded API)
    current_turn = 0
    # import pdb; pdb.set_trace()
    while True:
        try:
            response = openai.ChatCompletion.create(
                model=engine,
                messages = message_list,
                max_tokens=max_tokens,
                temperature=temperature,
                top_p=top_p,
                n=n,
                # # stop=stop if stop else None,
                presence_penalty=presence_penalty,
                frequency_penalty=frequency_penalty,
            )
            break
        except Exception as e:
            if current_turn == max_retry_turn:
                print('reach max quote.')
                exit(0)
            else:
                current_turn += 1
                tqdm.write(str(e))
                tqdm.write("Retrying...")
                import time
                time.sleep(30)
    
    generations = [gen['message']['content'] for gen in response['choices']]
    generations = [_ for _ in generations if _ != '']
    return generations


from pathlib import Path
import yaml

# Config
# CONFIG_FILE = Path('config.yml')
# OPENAI_API_KEY = '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'    # zachary
# OPENAI_API_KEY = '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'
OPENAI_API_KEY = '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'
# try:
#     with open(CONFIG_FILE) as f:
#         config = yaml.load(f, Loader=yaml.FullLoader)
#     OPENAI_API_KEY = config['openai']
# except FileNotFoundError:
#     print('No config file found. API keys will not be loaded.')

NUMERSENSE_ANSWERS = ['no', 'zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten']
DATASET_TO_QUERY_KEY = {
    'numersense': 'query',
    'CSQA': 'query',
    'CSQA2': 'query',
    'qasc': 'query',
}

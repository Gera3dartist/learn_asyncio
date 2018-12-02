import pathlib
import yaml

BASE_DIR = pathlib.Path(__file__).parent.parent
config_path = BASE_DIR / 'config' / 'polls.yaml'

PROJECT_ROOT = pathlib.Path(__file__).parent
TEMPLATES =  PROJECT_ROOT / 'templates'



def get_config(path=config_path):
	print(f'>>> {config_path}')
	with open(path) as f:
		config = yaml.load(f)
	return config




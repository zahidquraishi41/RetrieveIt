import json
import os
import sys


default_config = {
    'username': 'YOUR REDDIT USERNAME',
    'password': 'YOUR REDDIT PASSWORD',
    'client_id': 'BOT CLIENT ID',
    'client_secret': 'BOT CLIENT SECRET',
    'user_agent': 'savedscrapper by u/you',
    'unsave_after_download': False,
    'download_dir': 'downloads/'
}


def _config_path() -> str:
    pwd = os.path.dirname(sys.argv[0])
    return os.path.join(pwd, 'config.json')


def _load_config():
    with open(_config_path()) as f:
        return json.load(f)


def _reset_config():
    with open(_config_path(), 'w') as f:
        json.dump(default_config, f, indent=2)


def _validate_config(config: dict) -> bool:
    for key in default_config.keys():
        if key not in config:
            raise Exception(f'Missing "{key}" from config.json')

    for key in default_config.keys():
        if key == 'unsave_after_download':
            continue
        if not isinstance(config[key], str):
            raise Exception(f'"{key}" must be a string')
        if not config[key]:
            raise Exception(f'"{key}" cannot be empty')

    if not isinstance(config['unsave_after_download'], bool):
        raise Exception(f'"unsave_after_download" must be of boolean type')

    os.makedirs(config['download_dir'], exist_ok=True)


def get_config() -> dict | None:
    if not os.path.exists(_config_path()):
        _reset_config()
    try:
        config = _load_config()
        _validate_config(config)
        return config
    except KeyboardInterrupt:
        print(f'Error: Cancelled by user.')
        return
    except Exception as e:
        print(f'Error: {e}')
    while True:
        reset = input('Reset config.json (yes/no): ')
        if reset == 'yes':
            _reset_config()
            break
        elif reset == 'no':
            break
        else:
            print('Invalid choice\n')

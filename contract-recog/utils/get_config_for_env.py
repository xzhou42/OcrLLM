import json
import os

from utils.Log import Log


class EnvConfig:
    callback_url: str
    llm_url: str
    mysql_host: str
    mysql_user: str
    mysql_password: str
    mysql_database: str

    def __init__(self):
        self.env = os.getenv('ENVIRONMENT', 'dev').lower()
        self.init_config()
        Log.info(
            "当前 llm_url = {}, callback_url: {}, mysql_host: {}, mysql_database: {}".format(
                self.llm_url, self.callback_url, self.mysql_host, self.mysql_database))

    def init_config(self):
        config = self.get_config_for_env()
        self.callback_url = config['CALLBACK_URL']
        self.llm_url = config['LLM_URL']
        self.mysql_host = config['MYSQL_HOST']
        self.mysql_user = config['MYSQL_USER']
        self.mysql_password = config['MYSQL_PASSWORD']
        self.mysql_database = config['MYSQL_DATABASE']

    def get_config_for_env(self):
        config_file = f"config_{self.env}.json"
        with open(config_file, "r") as f:
            config = json.load(f)
        return config

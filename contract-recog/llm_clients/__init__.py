from . import llm_client
from utils.get_config_for_env import EnvConfig
env_config = EnvConfig()
client = llm_client.LlmClient(env_config.llm_url).client

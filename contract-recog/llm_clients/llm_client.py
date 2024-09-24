import openai
from openai import OpenAI

class LlmClient():
    def __init__(self, llm_url):
        self.llm_url = llm_url
        # self.client = openai.Client(base_url=self.llm_url, api_key="EMPTY")
        self.client = OpenAI(
            base_url="http://localhost:11434/v1",
            api_key='ollama',  # api_key没用，应该是随便填
        )

    def __repr__(self):
        return str(self.client)


    def chat(self,system_setting:str,query:str):
        response = self.client.chat.completions.create(
            model="qwen2",
            messages=[
                {"role": "system", "content": system_setting},
                {"role": "user", "content": query},
            ],
            temperature=0,
            max_tokens=500,
        )
        return response



if __name__ == "__main__":
    from utils.get_config_for_env import EnvConfig
    env_config = EnvConfig()
    client = LlmClient(env_config.llm_url)
    response = client.chat("你是一个商业助手","介绍一下你自己")
    print("response",response)

    # from openai import OpenAI
    #
    # client = OpenAI(
    #     base_url="http://localhost:11434/v1",
    #     api_key='ollama',  # api_key没用，应该是随便填
    # )
    # response = client.chat.completions.create(
    #     model="qwen:7b",
     #     messages=[
    #         {"role": "system", "content": "你是我的问答助手"},
    #         {"role": "user", "content": "海水里为什么有盐"},
    #     ]
    # )
    # print(response.choices[0].message.content)
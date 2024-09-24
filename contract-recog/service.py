import asyncio
import requests
from llm_clients import client
from ocr_tools import get_ocr_cnocr_local
# from ocr_tools import get_ocr_paddle, get_ocr_cnocr
from utils.prompt import COLLECTION_PROMPT
from utils.database import MySqlClient
from result_parser import extract_json_content
from utils.Log import Log
import traceback
from utils.ExceptionUtils import ChatException, OcrException, ExtractJsonException
from sql_sentences import INSERT_SQL
from datetime import datetime
import re
import time
from utils.get_config_for_env import EnvConfig

env_config = EnvConfig()

# mysql_client = MySqlClient()

# insert_result_sql = INSERT_SQL
# user = ("testing_serial","this is ocr_result","this is llm_result","this is json_result")

callback_url = env_config.callback_url


def async_to_sync(func):
    def wrapper(*args, **kwargs):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(func(*args, **kwargs))
        loop.close()
        return result

    return wrapper


def send_request_dict(url, data: object):
    response = ''
    # try:
    #     Log.info("开始回调")
    #     headers = {'accept': 'application/json', 'Content-Type': 'application/json'}
    #     # data1 = json.dumps(data.__dict__, indent=4)
    #     response = requests.post(url, headers=headers, json=data)
    #     Log.info("url: {url}, data: {data}, response: {response}".format(
    #         url=url, data=data, response=response))
    #     response.keep_alive = False
    # except Exception:
    #     Log.error("回调应用层失败：{error}".format(error=traceback.format_exc()))
    return response


def chat_task(query: str):
    """
    针对 ocr 识别结果，构建query，调用大模型得到响应。返回的只是大模型针对问题的响应内容，不包括其余的信息。
    """
    # Chat completion
    # query = prompt.format(ocr_result=ocr_result)
    try:

        # Log.info(f"尝试与LLM模型对话， question = {query}")
        response = client.chat.completions.create(
            model="qwen2",
            messages=[
                {"role": "system", "content": "你是一个信息提取助手"},
                {"role": "user", "content": query},
            ],
            temperature=0,
            max_tokens=500,
        )

        # choices是一个列表，只要第一个choice里面的message中的content
        content = response.choices[0].message.content
        # Log.info(f"大模型响应的content内容是：\n{content}")
        return content
    # 对于可能出现的异常，抛出自定义的 ChatException
    except Exception as e:
        Log.error(f"与LLM模型对话失败\n error = {e}\n info = {traceback.format_exc()}\n")
        # 向上抛出自定义的 ChatException
        raise ChatException


def extract_contract_no(text):
    pattern = r'编号:\s*([\s\S]*?)\s*请'
    match = re.search(pattern, text)
    if match:
        full_no = match.group().replace("\n", "").replace("编号:", "")
        numbers = re.findall(r'\d+', full_no)
        return "".join(numbers)
    else:
        return None


# # 示例文本
# text = "这是一段文本，编号: 12345 号 这里有一些其他的信息。"
#
# # 提取编号
# number = extract_number(text)
# print(number)  # 输出: 12345

# @async_to_sync
def process_request(file_content, serial_no: str, keys_describe: str):
    """
    处理本次请求
    """

    # files = {"file": (file.filename,file.file, file.content_type)}
    # print("files",files)
    # files = {"image": (file.filename, file_content, file.content_type)}
    # response = requests.post('http://0.0.0.0:8501/ocr', files=files)
    # print(response.json())
    json_data = ''

    try:
        start_time = time.time()

        # 对合同进行 ocr，提取文字
        # ocr_res = get_ocr_paddle(file)
        ocr_res = get_ocr_cnocr_local(file_content)
        ocr_res = ocr_res.split("本合同附件")[0]
        # print("ocr_res",ocr_res)
        contract_no = extract_contract_no(ocr_res)

        # 调用大模型，生成回答
        # print("ocr_res", ocr_res)
        query = COLLECTION_PROMPT.format(ocr_result=ocr_res,keys_describe=keys_describe)
        print("query",query)
        llm_reply = chat_task(query)
        # print("llm_reply", llm_reply)
        # 解析大模型回答，生成json格式的响应数据
        try:
            json_data = extract_json_content(llm_reply, contract_no)
        except:
            print(llm_reply)
        end_time = time.time()
        result_data = (str(serial_no), str(ocr_res), str(llm_reply), str(json_data), str(datetime.now()),
                       str(end_time - start_time))

        # if mysql_client.connection_isopen():
        #     # print("connection_isopen is open:",mysql_client.connection_isopen())
        #     mysql_client.execute_query(insert_result_sql, result_data)
        # else:
        #     mysql_client.create_connection()
        #     mysql_client.execute_query(insert_result_sql, result_data)
        # print(json_data)
        Log.info(json_data)
        response_data = {
            "code": "200",
            "msg": "",
            "serialNo": serial_no,
            "data": json_data
        }

        send_request_dict(url=callback_url, data=response_data)
        Log.info(f"流水号：{serial_no} 处理完毕，回调完毕")
        # Log.info(f"处理本次请求共用时：{round(time.time() - start_time, 2)}\n, 最终的响应内容是：\n{json_data}")
    # ocr 过程中出现异常
    except OcrException:
        Log.error(f"流水号：{serial_no}")
        send_request_dict(url=callback_url, data={"serialNo": serial_no, "code": "5001", "msg": "OCR过程出错"})
    # 和大模型对话出现异常
    except ChatException:
        Log.error(f"流水号：{serial_no}")
        send_request_dict(url=callback_url, data={"serialNo": serial_no, "code": "5001", "msg": "调用LLM过程出错"})
    # 将大模型的回复转为json时出现异常
    except ExtractJsonException:
        send_request_dict(url=callback_url, data={"serialNo": serial_no, "code": "5001", "msg": "解析JSON出错"})
        Log.error(f"流水号：{serial_no}")
    except Exception as e:
        send_request_dict(url=callback_url, data={"serialNo": serial_no, "code": "5001", "msg": "其他错误,请查看日志"})
        Log.error(f"流水号：{serial_no},{e},{traceback.format_exc()}")

    return json_data
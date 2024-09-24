from fastapi import FastAPI, UploadFile, Form
from fastapi.responses import JSONResponse
import uvicorn
from utils.Log import Log
from pydantic import BaseModel
from service import process_request
from concurrent.futures import ThreadPoolExecutor
from ocr_tools import get_ocr_cnocr_local
import socket
from utils.database import MySqlClient
from utils.get_config_for_env import EnvConfig
from urllib.parse import urlparse
from sql_sentences import SELECT_ALL
import time

class Para(BaseModel):
    serial_no: str
    tsk_id: str


app = FastAPI()
pool = ThreadPoolExecutor()
env_config = EnvConfig()
mysql_client = MySqlClient()


def extract_ip_port(url):
    parsed_url = urlparse(url)
    ip = parsed_url.hostname
    port = parsed_url.port
    return ip,port


def check_service_alive(host, port):
    try:
        # 创建一个 socket 对象
        with socket.create_connection((host, port), timeout=5):
            # print(f"服务在 {host}:{port} 上存活")
            return True
    except (socket.timeout, socket.error):
        # print(f"无法连接到 {host}:{port}，服务未存活")
        return False


@app.get("/contractrecog/checkHealth")
async def health_check():
    """
    a simple endpoint to check the health of the service
    """
    start_time = time.time()
    host, port = extract_ip_port(env_config.llm_url)
    if check_service_alive(host, port):
        try:
            select_users = SELECT_ALL
            start_query_time = time.time()
            result = mysql_client.fetch_data(select_users)
            if type(result[0]['count_all']) == int:

                end_time = time.time()
                querytotalTime = end_time - start_time
                querydbtime = end_time - start_query_time
                data = {
                        "msg": "service is ok!",
                        "content": {
                                "dbStatusMsg": "db service is ok!",
                                "dbStatus": 0,
                                "queryTotalTime": str(round(querytotalTime*1000, 2))+"ms",
                                "queryDBTime": str(round(querydbtime*1000, 2))+"ms"
                        },
                        "errorcode": 0
                        }
                return data
            else:
                raise Exception
        except:
            data = {
                "msg": "llm service is ok!",
                "content": {
                    "dbStatusMsg": "db service lost connect!",
                    "dbStatus": 1,
                    "queryTotalTime": "",
                    "queryDBTime": ""
                },
                "errorcode": 2
            }
            return data
    else:
        data = {
            "msg": "service lost connect!",
            "content": {
                "dbStatusMsg": "llm service lost connect!",
                "dbStatus": 1,
                "queryTotalTime": "",
                "queryDBTime": ""
            },
            "errorcode": 1
        }
        return data



@app.post("/ocrProcess")
async def get_info_from_ocr(file: UploadFile):
    with file.file as f:
        file_content = f.read()
        # print("file_content:", type(file_content))
        pool.submit(get_ocr_cnocr_local, file_content)
    #    return ocr_text
    return "success"


@app.post("/guarLnAnalyze")
def get_info_from_guar_demo_file(file: UploadFile, serial_no: str = Form(...), keys_describe: str = Form(...),
                                 tsk_id: str = Form(...)):
    # 开启后台任务
    # background_tasks.add_task(process_request, file, serial_no)
    with file.file as f:
        file_content = f.read()
        result = process_request(file_content, serial_no,keys_describe)
    #     pool.submit(process_request, file_content, serial_no)
    # return JSONResponse(status_code=200, content={"message": "图片接收成功，正在处理"})
    print(result)
    return result


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='contract recogization service')

    Log.set_level("info")
    parser.add_argument("--host", type=str, default="0.0.0.0")
    # parser.add_argument("--host", type=str, default="0.0.0.0")
    parser.add_argument("--port", type=int, default=7862)
    args = parser.parse_args()
    args_dict = vars(args)

    uvicorn.run(app, host=args.host, port=args.port, workers=1)

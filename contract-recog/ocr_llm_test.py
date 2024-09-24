import requests


# 定义接口的 URL
url = "http://localhost:7862/guarLnAnalyze"  # 根据实际情况替换为你的接口地址


# 定义要上传的文件和其他参数
file_path = "截图合同.png"  # 替换为实际文件路径
serial_no = "123456"  # 替换为实际的 serial_no
tsk_id = "task_001"  # 替换为实际的 tsk_id


# 打开文件
with open(file_path, "rb") as file:
    # 定义要发送的文件和数据
    files = {"file": file}
    data = {"serial_no": serial_no, "tsk_id": tsk_id}


    # 发送 POST 请求
    response = requests.post(url, files=files, data=data)


# 打印响应结果
print("Status Code:", response.status_code)
print("Response JSON:", response.json())
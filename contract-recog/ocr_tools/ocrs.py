# from paddleocr import PaddleOCR
from utils.Log import Log
import traceback
from utils.ExceptionUtils import OcrException
from fastapi import UploadFile
import requests
import cv2 as cv
import numpy as np
from cnocr import CnOcr
# CNOCR_URL = 'http://0.0.0.0:8501/ocr'

# def get_ocr_paddle(file: UploadFile):
#     """
#     对图片进行 ocr 提取
#     """
#     try:
#         file_content = file.file.read()
#         # 使用 OpenCV 打开图片
#         img = cv.imdecode(np.frombuffer(file_content, np.uint8), cv.IMREAD_COLOR)
#         ocr = PaddleOCR(use_angle_cls=False, lang="ch", use_gpu=False, show_log=False, det_db_box_thresh=0.3,
#                         use_dilation=True)
#         result = ocr.ocr(img, cls=False)
#         txts = [line[1][0] for line in result[0]]
#         all_context = "\n".join(txts)
#         return all_context
#     except Exception as e:
#         Log.error(f"paddle ocr 提取文档内容过程中，出现异常。\n error：{e}\n info = {traceback.format_exc()}\n")
#         raise OcrException


def get_ocr_cnocr_local(file_content):
    """
    使用 cnocr 进行ocr
    """
    # 使用 OpenCV 打开图片
    img = cv.imdecode(np.frombuffer(file_content, np.uint8), cv.IMREAD_COLOR)

    try:
        # 更改权重文件路径为当前项目的目录。'doc-densenet_lite_246-gru_base'
        # 启动项目时，当前路径是api.py文件所在的路径，所以要找到权重文件夹.cnocr与.cnstd，路径要加上./ocr_tools
        ocr = CnOcr(rec_model_name='doc-densenet_lite_246-gru_base', rec_root='./ocr_tools/.cnocr',
                    det_model_name='db_resnet34', det_root='./ocr_tools/.cnstd', context="cpu")
        result = ocr.ocr(img_fp=img, resized_shape=((1024, 1024)))

        all_context = '\n'.join([entry['text'] for entry in result])
        return all_context
    except Exception as e:
        Log.error(f" cnocr 提取文档内容过程中，出现异常。\n error：{e}\n info = {traceback.format_exc()}\n")
        raise OcrException


# def get_ocr_cnocr(file: UploadFile):
#     try:
#         # r = requests.post('http://0.0.0.0:8501/ocr', files={'image': (img, open(img, 'rb'), 'image/png')})
#         file_content = file.file.read()
#         files = {"image": (file.filename, file_content, file.content_type)}
#         r = requests.post(CNOCR_URL, files=files)
#         ocr_out = r.json()['results']
#         # print(ocr_out)
#         text = ''
#         for block in ocr_out:
#             text += '\n'
#             text += block['text']
#     except Exception as e:
#         Log.error(f"cnocr 提取文档内容过程中，出现异常。\n error：{e}\n info = {traceback.format_exc()}\n")
#         raise OcrException
#     return text
#
#
# def get_ocr_cnocr_str(image_path: str):
#     text = ''
#     try:
#         r = requests.post(
#             CNOCR_URL, files={'image': (image_path, open(image_path, 'rb'), 'image/png')},
#         )
#         ocr_out = r.json()['results']
#         for block in ocr_out:
#             text += '\n'
#             text += block['text']
#
#     except Exception as e:
#         Log.error(f"cnocr 提取文档内容过程中，出现异常。\n error：{e}\n info = {traceback.format_exc()}\n")
#         raise OcrException
#     finally:
#         return text


# if __name__ == "__main__":
    # from concurrent.futures import ThreadPoolExecutor, as_completed
    # import time

    # executor = ThreadPoolExecutor(max_workers=20)
    # img = '../合同样例.png'
    # start = time.time()
    # futures = [executor.submit(get_ocr_cnocr_str, img) for i in range(20)]
    # for future in as_completed(futures):
    #     result = future.result()
    #     print(result)
    #     print("===================== ")
    # print(time.time() - start)

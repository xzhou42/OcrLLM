from datetime import datetime
import traceback
from utils.ExceptionUtils import ExtractJsonException
from utils.Log import Log
import cn2an
import re
import json
def validate_and_format_date(date_str):
    """
    尝试使用指定的格式来解析日期字符串，将日期格式解析为"xxxx年xx月xx日"格式
    """
    # 指定的日期格式
    specified_format = "%Y年%m月%d日"
    output_format = "%Y%m%d"
    try:

        # 尝试按照指定格式解析日期
        parsed_date = datetime.strptime(date_str, specified_format)
        # 如果解析成功，返回格式化后的日期字符串
        ans = parsed_date.strftime(output_format)
        return ans
    # 如果解析失败，尝试看看LLM是否返回的日期格式是其他常见日期格式
    except ValueError:
        try:
            # 常见的一些日期格式
            common_formats = [
                "%Y%m%d",
                "%Y-%m-%d",  # ISO 8601格式，例如2023-08-06
                "%Y/%m/%d",  # 例如2023/08/06
                "%Y.%m.%d",  # 例如2023.08.06
                "%d-%m-%Y",  # 日-月-年，欧洲常用格式
                # 可以继续添加其他格式
            ]
            for fmt in common_formats:
                try:
                    # 尝试按照常见格式解析日期
                    parsed_date = datetime.strptime(date_str, fmt)
                    # 解析成功，转换为指定的格式
                    return parsed_date.strftime(output_format)
                except ValueError:
                    continue
            return ''
        except ValueError as e:
            # 如果所有尝试都失败了，打印错误信息
            Log.error(f"大模型给出的日期：{date_str}，无法转换为 'xxxx年xx月xx日' 格式")
            Log.error(f"转换大模型给的日期格式失败。\n error：{e}\n info = {traceback.format_exc()}\n")
            return ''


def chinese_amt_trans_bts(chinese_amt):
    try:
        small_amt = cn2an.cn2an(chinese_amt, "smart")
        small_amt = round(small_amt, 2)
        return small_amt
    except:
        # print("中文大写转阿拉伯数字失败,{error}".format(error=traceback.format_exc()))
        Log.error("中文大写转阿拉伯数字失败,{error}".format(error=traceback.format_exc()))
        return ''


def chinese_time_trans_bts(period):
    try:
        small_period = cn2an.transform(period, "cn2an")
        return small_period
    except:
        print("中文大写期限三年五年转换失败,{error}".format(error=traceback.format_exc()))
        Log.error("中文大写期限三年五年转换失败,{error}".format(error=traceback.format_exc()))
        return ''


def round_to_decimal(number, digit):
    try:
        return f"{number:.{digit}f}"
    except:
        Log.error("{number} 保留小数点后几位失败,{error}".format(number=number, error=traceback.format_exc()))
        return ''


def remove_json_comments(json_str):
    # 移除单行注释（// 开头的注释）
    json_str = re.sub(r'//.*?\n', '', json_str)
    # 移除多行注释（/* ... */）
    json_str = re.sub(r'/\*.*?\*/', '', json_str, flags=re.DOTALL)
    return json_str

def extract_json_content(data, contract_no):
    """
    将LLM的响应内容，转为 JSON 格式，并尝试对其中的日期的格式进行校验、转换。
    """

    data = remove_json_comments(data)
    try:
        content = data.split('```json')[1].split('```')[0]
    except:
        content = data

    try:
        # 字符串的 content -> 字典 dict
        json_content = json.loads(content)
        if "MAIN_CTR_NO" in json_content and json_content["MAIN_CTR_NO"] is not None:
            json_content["MAIN_CTR_NO"] = contract_no

        # 处理大模型返回的时间，格式化为 xxxx年xx月xx日
        # 合同起始时间
        if "CTR_BGN_DT" in json_content and json_content["CTR_BGN_DT"] is not None:
            json_content["CTR_BGN_DT"] = validate_and_format_date(json_content["CTR_BGN_DT"])
        # 合同结束时间
        if "CTR_MTU_DT" in json_content and json_content["CTR_MTU_DT"] is not None:
            json_content["CTR_MTU_DT"] = validate_and_format_date(json_content["CTR_MTU_DT"])
        # 利率引用时间
        if "LPR_QUO_DT" in json_content and json_content["LPR_QUO_DT"] is not None:
            json_content["LPR_QUO_DT"] = validate_and_format_date(json_content["LPR_QUO_DT"])
        # 金额大写转换以及保留两位小数
        if "BRWR_CTR_UPPER_AMT" in json_content and json_content["BRWR_CTR_UPPER_AMT"] is not None:
            json_content["BRWR_CTR_UPPER_AMT"] = json_content["BRWR_CTR_UPPER_AMT"].replace("参", "叁").replace("任", "仟")
            json_content["CTR_AMT"] = chinese_amt_trans_bts(json_content["BRWR_CTR_UPPER_AMT"])
            json_content["CTR_AMT"] = round_to_decimal(json_content["CTR_AMT"], 2)

        # 执行月利率保留7位小数
        if "EXEC_MON_IR" in json_content and json_content["EXEC_MON_IR"] is not None:
            json_content["EXEC_MON_IR"] = round_to_decimal(json_content["EXEC_MON_IR"], 7)
        # 执行年利率保留7位小数
        if "EXEC_YEAR_IR" in json_content and json_content["EXEC_YEAR_IR"] is not None:
            json_content["EXEC_YEAR_IR"] = round_to_decimal(json_content["EXEC_YEAR_IR"], 7)
        # LPR报价利率保留7位小数
        if "LPR_QUO_INTR_RAT" in json_content and json_content["LPR_QUO_INTR_RAT"] is not None:
            json_content["LPR_QUO_INTR_RAT"] = round_to_decimal(json_content["LPR_QUO_INTR_RAT"], 7)
        # 增减点数保留7位小数
        if "INCS_DECS_PNT_NUM" in json_content and json_content["INCS_DECS_PNT_NUM"] is not None:
            json_content["INCS_DECS_PNT_NUM"] = round_to_decimal(json_content["INCS_DECS_PNT_NUM"], 7)
        # 期限大写转换
        if "LPR_TRM_TYP" in json_content and json_content["LPR_TRM_TYP"] is not None:
            json_content["LPR_TRM_TYP"] = chinese_time_trans_bts(json_content["LPR_TRM_TYP"])

        return json_content
    # json 解析异常
    except json.JSONDecodeError as e:
        Log.error(f"大模型的响应内容：{data}")
        Log.error(f"将LLM响应内容解析为json格式失败，JSON 解码错误。\n error：{e}\n info = {traceback.format_exc()}\n")
        raise ExtractJsonException
    # 大模型给的日期格式异常，不能解析成"xxxx年xx月xx日"的格式
    except ValueError as e:
        raise ExtractJsonException
    # 其余可能出现的异常
    except Exception as e:
        raise ExtractJsonException

class ChatException(Exception):
    """
    自定义的 和 LLM 的对话异常
    """
    pass


class OcrException(Exception):
    """
    自定义的 ocr 异常
    """
    pass


class ExtractJsonException(Exception):
    """
    自定义的 json 相关的异常。包括将大模型的响应内容转换为json、大模型给的日期格式异常
    """
    pass

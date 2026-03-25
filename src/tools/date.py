from datetime import datetime
from langchain_community.tools import tool


def _gtime() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


@tool
def gtime() -> str:
    """
    以格式 YYYY-MM-DD HH:MM:SS 获取当前日期时间
    """
    return _gtime()


# testing
if __name__ == "__main__":
    print(_gtime())

from datetime import datetime
from util import tool


def _cur_time() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


@tool
def cur_time() -> str:
    """
    当用户要求获取当前日期时使用
    
    输入：
    {
    }
    
    输出：YYYY-MM-DD HH:MM:SS 
    """
    return _cur_time()


# testing
if __name__ == "__main__":
    print(_cur_time())

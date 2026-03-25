from langchain_community.tools import tool
import math

def _ecalc(evalable: str) -> str:
    return eval(evalable, {"__builtins__": {}}, {"math": math, **math.__dict__})


@tool
def ecalc(evalable: str) -> str:
    """
    当用户要求计算符合python规范的数学表达式时使用
    包含python内建math包的所有方法，返回数值结果
    """
    return _ecalc(evalable)


# testing
if __name__ == "__main__":
    print(_ecalc("1 + sqrt(2)"))

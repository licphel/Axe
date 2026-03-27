from util import tool
import math


def _eval_calc(evalable: str) -> str:
    return eval(evalable, {"__builtins__": {}}, {"math": math, **math.__dict__})


@tool
def eval_calc(evalable: str) -> str:
    """
    当用户要求计算符合 python 规范的数学表达式时使用
    包含 python 内建 math 包的所有方法，返回数值结果
    
    输入：
    {
      "evalable": <表达式>
    }
    
    输出：小数形式的数字，如果表达式执行失败则输出 null
    """
    try:
      result = _eval_calc(evalable)
      return result
    except:
      return "null"

# testing
if __name__ == "__main__":
    print(_eval_calc("1 + sqrt(2)"))
    print(_eval_calc("1 / log(2)"))
    print(_eval_calc("pi ** e"))

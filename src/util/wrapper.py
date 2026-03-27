import functools
import inspect

def tool(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    
    wrapper.doc = f"名称：{func.__name__}，\n文档：{func.__doc__}，\n参数：{inspect.signature(func)}"
      
    return wrapper
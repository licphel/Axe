from langchain.agents import create_agent
from langchain_deepseek import ChatDeepSeek
from langchain_community.tools.tavily_search import TavilySearchResults
from tools import *
import os

os.environ["DEEPSEEK_API_KEY"] = "sk-f4338eb0b29047cba9310ca4146d8ed9"

model = ChatDeepSeek(model="deepseek-chat")

agent = create_agent(
    model=model,
    tools=[gtime, ecalc],
    system_prompt="你是一名多才多艺的智能助手，可以调用工具帮助用户解决问题。",
)

result = agent.invoke(
    {
        "messages": [
            {"role": "user", "content": "请计算1+2+sqrt(5)+log(3)"}
        ]
    }
)

print(result["messages"][-1].content)

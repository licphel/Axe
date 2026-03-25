from langchain.agents import create_agent
from langchain_deepseek import ChatDeepSeek
from tools import *
import os

os.environ["DEEPSEEK_API_KEY"] = "sk-f4338eb0b29047cba9310ca4146d8ed9"
model = ChatDeepSeek(model="deepseek-chat")

agent = create_agent(
    model=model,
    tools=[eval_calc, cur_time, memorize, recall, forget],
    system_prompt="""
    你是一个智能助手，可以调用工具帮助用户。
    你需要自己发现一些重要信息（包括但不限于名字，地址，生日等）并存入长期记忆，用户可能不会给出明确的提示。
    """,
)

messages = []

print("智能助手已启动，输入 exit 退出\n")

while True:
    user_input = input("[user] ")
    if user_input.lower() in ["exit", "quit"]:
        break

    messages.append({"role": "user", "content": user_input})

    result = agent.invoke({"messages": messages})

    ai_response = result["messages"][-1].content
    messages.append({"role": "assistant", "content": ai_response})

    print(f"[LoMR] {ai_response}\n")

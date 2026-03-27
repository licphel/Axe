from langchain.agents import create_agent
from langchain_deepseek import ChatDeepSeek
from tools import *
from util import *
import os

os.environ["DEEPSEEK_API_KEY"] = rstr("./api_key.txt")
model = ChatDeepSeek(model="deepseek-chat")

agent = create_agent(
    model=model,
    tools=[eval_calc, cur_time, memorize, recall, forget],
    system_prompt=rstr("./prompts/sys_init.md"),
)

messages = []

print("Welcome to .AXE. Currently\n")

while True:
    user_input = input("[user] ")
    if user_input.lower() in ["exit", "quit"]:
        break

    messages.append({"role": "user", "content": user_input})

    result = agent.invoke({"messages": messages})

    ai_response = result["messages"][-1].content
    messages.append({"role": "assistant", "content": ai_response})

    print(f"[.AXE] {ai_response}\n")

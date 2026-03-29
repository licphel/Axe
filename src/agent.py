from langchain.agents import create_agent
from langchain_deepseek import ChatDeepSeek
from tools import *
from util import *
import os
import json
import re

# set envvar from local api_key.txt
os.environ["DEEPSEEK_API_KEY"] = read("./api_key.txt")

model = ChatDeepSeek(model="deepseek-chat")

tools = [eval_calc, cur_time, memorize, recall, forget]
tool_map = {}
tool_descs = ""

for v in tools:
    tool_map[v.__name__] = v
    tool_descs += v.doc

prompt_sys_init = read("prompts/react.md")
show_all = False


def debug(*args, **kwargs):
    print("\033[90m", end="")
    print(*args, **kwargs)
    print("\033[0m", end="")


def ReAct_loop(query: str) -> str:
    messages = [
        {
            "role": "system",
            "content": prompt_sys_init
            + f"\n附录：这是你可以调用的函数名-文档表：{tool_descs}",
        },
        {"role": "user", "content": query},
    ]

    # RAG
    context = recall(query)
    if context != "没有找到相关记忆":
        messages.append({"role": "system", "content": f"参考历史记忆：\n{context}\n\n"})
        if show_all:
          debug("=== RAG result: ===")
          debug(messages[-1])

    step = 0
    max_steps = 10

    while step < max_steps:
        response = model.invoke(messages).content

        if show_all:
            debug("=== model response: ===")
            debug(response)

        try:
            json_match = re.search(r"\{.*\}", str(response), re.DOTALL)
            if not json_match:
                return f"Invalid syntax：{response}"
            data = json.loads(json_match.group())
        except json.JSONDecodeError as e:
            return f"Cannot parse JSON：{e}\n src：{response}"

        if data.get("Action"):
            tool_name = data["Action"]
            tool_input = data.get("Action Input", {})

            if tool_name not in tool_map.keys():
                observation = f"Action '{tool_name}' not found"
            else:
                try:
                    result = tool_map[tool_name](**tool_input)
                    observation = str(result)
                except Exception as e:
                    observation = f"Action failed：{e}"

            messages.append({"role": "assistant", "content": str(response)})
            messages.append({"role": "system", "content": f"Observation: {observation}"})
            
            if show_all:
              debug("=== action invoked! ===")
              debug(response)
            
            step += 1
            continue

        if data.get("Final Answer"):
            return data["Final Answer"]

        return f"Output invalid：{response}"

    return "Step limit exceeded"


print("\n" + "=" * 35)
print("[!] Welcome to .AXE, currently powered by Deepseek.")
print("[!] /quit to exit.")
print("[!] /shal to show or unshow all thoughts.\n")

while True:
    user_input = input("[user] ")
    if user_input.lower() in ["/quit"]:
        break
    if user_input.lower() in ["/shal"]:
        show_all = not show_all
        continue

    print(f"[.AXE] {ReAct_loop(user_input)}\n")

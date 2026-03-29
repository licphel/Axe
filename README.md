# .AXE - 基于 ReAct 的智能体系统

一个轻量级的智能体框架，支持工具调用和长期记忆。
![alt text](perf.png)

## 功能

- **工具调用**：计算器、时间查询、记忆管理
- **长期记忆**：基于 Chroma + text2vec 的语义记忆检索
- **ReAct 循环**：模型自主决策，支持多轮对话
- **JSON 输出**：结构化输出，易于解析

## 快速开始

```bash
pip install -r requirements.txt
python agent.py
from util import tool
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core import documents
from .date import _cur_time

embeddings = HuggingFaceEmbeddings(
    model_name="shibing624/text2vec-base-chinese",
    model_kwargs={"device": "cpu"},
    encode_kwargs={"normalize_embeddings": True},
)

vectorstore = Chroma(
    collection_name="long_term_memory",
    embedding_function=embeddings,
    persist_directory="./memory",
)


def _memorize(key: str, info: str, metadata: dict | None = None):
    doc = documents.Document(
        page_content=info,
        metadata={"key": key, "timestamp": _cur_time(), **(metadata or {})},
    )
    vectorstore.add_documents([doc])
    # vectorstore.persist() <-- this is automatical


def _recall_by_key(key: str) -> str | None:
    results = vectorstore.get(where={"key": key})
    if results["documents"]:
        return results["documents"][0]
    return None


def _recall_by_similarity(query: str, topk: int = 3) -> list:
    results = vectorstore.similarity_search(query, k=topk)
    return [(doc.page_content, doc.metadata) for doc in results]


def _forget(key: str):
    results = vectorstore.get(where={"key": key})
    if results["ids"]:
        vectorstore.delete(ids=results["ids"])
        return True
    return False


@tool
def memorize(key: str, info: str) -> str:
    """
    记住一条长期记忆

    输入:
    {
      "key": <记忆的唯一标识，统一用中文>
      "info": <记忆的具体内容>
    }

    输出：是否成功
    """
    _memorize(key, info)
    return f"已记住：{key} = {info}"


@tool
def forget(key: str) -> str:
    """
    遗忘一条长期记忆

    输入:
    {
      "key": <记忆的唯一标识，统一用中文>
    }

    输出：是否成功
    """
    if _forget(key):
        return f"成功删除：{key}"
    return f"没有找到名为 {key} 的记忆"


@tool
def recall(query: str) -> str:
    """
    搜索相关记忆（模糊查询）

    输入:
    {
      "query": <记忆的模糊查询关键词，统一用中文>
    }

    输出：记忆信息（包含键值对）
    """
    results = _recall_by_similarity(query, topk=3)
    if not results:
        return "没有找到相关记忆"

    output = "找到以下相关记忆：\n"
    for content, meta in results:
        output += f"- [{meta.get('key', '未知')}] {content}\n"
    return output

from langchain_community.tools import tool
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core import documents
from .date import _cur_time

embeddings = HuggingFaceEmbeddings(
    model_name="shibing624/text2vec-base-chinese",
    model_kwargs={'device': 'cpu'},
    encode_kwargs={'normalize_embeddings': True}
)

vectorstore = Chroma(
    collection_name="long_term_memory",
    embedding_function=embeddings,
    persist_directory="./memory_db"
)

def _memorize(key: str, info: str, metadata: dict|None = None):
    doc = documents.Document(
        page_content=info,
        metadata={
            "key": key,
            "timestamp": _cur_time(),
            **(metadata or {})
        }
    )
    vectorstore.add_documents([doc])

def _recall_by_key(key: str) -> str|None:
    results = vectorstore.get(where={"key": key})
    if results['documents']:
        return results['documents'][0]
    return None

def _recall_by_similarity(query: str, topk: int = 3) -> list:
    results = vectorstore.similarity_search(query, k=topk)
    return [(doc.page_content, doc.metadata) for doc in results]

def _forget(key: str):
    results = vectorstore.get(where={"key": key})
    if results['ids']:
        vectorstore.delete(ids=results['ids'])
        return True
    return False

@tool
def memorize(key: str, info: str):
    """
    记住一条长期记忆
    参数:
        key: 记忆的唯一标识（如 "生日", "名字"）
        info: 记忆的具体内容
    """
    _memorize(key, info)
    return f"已记住：{key} = {info}"

@tool
def recall(key: str) -> str:
    """
    回忆一条长期记忆
    参数:
        key: 要回忆的记忆标识（可以是精确的key，也可以是模糊描述）
    """
    result = _recall_by_key(key)
    if result:
        return result
    
    similar = _recall_by_similarity(key, topk=1)
    if similar:
        content, meta = similar[0]
        return f"你可能想找的是「{meta.get('key', '未知')}」：{content}"
    
    return "没有找到相关记忆"

@tool
def forget(key: str):
    """
    遗忘一条长期记忆
    参数:
        key: 要遗忘的记忆标识
    """
    if _forget(key):
        return f"已遗忘：{key}"
    return f"没有找到名为 {key} 的记忆"

@tool
def search_memory(query: str) -> str:
    """
    搜索相关记忆（模糊查询）
    参数:
        query: 搜索关键词
    """
    results = _recall_by_similarity(query, topk=3)
    if not results:
        return "没有找到相关记忆"
    
    output = "找到以下相关记忆：\n"
    for content, meta in results:
        output += f"- [{meta.get('key', '未知')}] {content}\n"
    return output
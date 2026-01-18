import csv
import os
import logging
from typing import List
from typing_extensions import TypedDict

from langchain_core.documents import Document
from langchain_core.tools import tool
from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain_community.vectorstores import FAISS
from langchain.agents import create_agent
from dotenv import load_dotenv

# Import AgentCore runtime
from bedrock_agentcore.runtime import BedrockAgentCoreApp

# -------------------- Logging Setup --------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)
# -------------------------------------------------------

# Create the AgentCore app instance
app = BedrockAgentCoreApp()
_ = load_dotenv()

def load_faq_csv(path: str) -> List[Document]:
    """
    Docstring for load_faq_csv
    
    :param path: Description
    :type path: str
    :return: Description
    :rtype: List[Document]
    """
    logger.info(f"Loading FAQ CSV from path: {path}")
    docs = []
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            q = row["Question"].strip()
            a = row["Answer"].strip()
            docs.append(Document(page_content=f"Q: {q}\nA: {a}"))
    logger.info(f"Loaded {len(docs)} FAQ entries from CSV")
    return docs

docs = load_faq_csv("./data/nuts_shop_faq_real.csv")

logger.info("Creating HuggingFace embeddings")
emb = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
)

logger.info("Splitting documents into chunks")
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)
chunks = splitter.split_documents(docs)
logger.info(f"Created {len(chunks)} document chunks")

logger.info("Building FAISS vector store")
store = FAISS.from_documents(chunks, emb)
logger.info("FAISS vector store created successfully")

# -------------------- Tools --------------------
@tool
def search_faq(query: str) -> str:
    """Search the FAQ knowledge base for relevant information.
    Use this tool when the user asks questions about products, services, or policies.
    
    Args:
        query: The search query to find relevant FAQ entries
        
    Returns:
        Relevant FAQ entries that might answer the question
    """
    logger.info(f"search_faq called with query: {query}")
    results = store.similarity_search(query, k=3)
    
    if not results:
        logger.warning("No relevant FAQ entries found")
        return "No relevant FAQ entries found."
    
    context = "\n\n---\n\n".join([
        f"FAQ Entry {i+1}:\n{doc.page_content}" 
        for i, doc in enumerate(results)
    ])
    
    logger.info(f"Found {len(results)} relevant FAQ entries")
    return f"Found {len(results)} relevant FAQ entries:\n\n{context}"


@tool
def search_detailed_faq(query: str, num_results: int = 5) -> str:
    """Search the FAQ knowledge base with more results for complex queries.
    Use this when the initial search doesn't provide enough information.
    
    Args:
        query: The search query
        num_results: Number of results to retrieve (default: 5)
        
    Returns:
        More comprehensive FAQ entries
    """
    logger.info(f"search_detailed_faq called with query: {query}, num_results: {num_results}")
    results = store.similarity_search(query, k=num_results)
    
    if not results:
        logger.warning("No relevant detailed FAQ entries found")
        return "No relevant FAQ entries found."
    
    context = "\n\n---\n\n".join([
        f"FAQ Entry {i+1}:\n{doc.page_content}" 
        for i, doc in enumerate(results)
    ])
    
    logger.info(f"Found {len(results)} detailed FAQ entries")
    return f"Found {len(results)} detailed FAQ entries:\n\n{context}"


@tool
def reformulate_query(original_query: str, focus_aspect: str) -> str:
    """Reformulate the query to focus on a specific aspect.
    Use this when you need to search for a different angle of the question.
    
    Args:
        original_query: The original user question
        focus_aspect: The specific aspect to focus on (e.g., "pricing", "activation", "troubleshooting")
        
    Returns:
        A reformulated query focused on the specified aspect
    """
    logger.info(f"reformulate_query called with original_query: {original_query}, focus_aspect: {focus_aspect}")
    reformulated = f"{focus_aspect} related to {original_query}"
    results = store.similarity_search(reformulated, k=3)
    
    if not results:
        logger.warning(f"No results found for aspect: {focus_aspect}")
        return f"No results found for aspect: {focus_aspect}"
    
    context = "\n\n---\n\n".join([
        f"Entry {i+1}:\n{doc.page_content}" 
        for i, doc in enumerate(results)
    ])
    
    logger.info(f"Found {len(results)} entries for aspect: {focus_aspect}")
    return f"Results for '{focus_aspect}' aspect:\n\n{context}"


tools = [search_faq, search_detailed_faq, reformulate_query]

logger.info("Initializing ChatGroq model")
model = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0,
    api_key=os.getenv("GROQ_API_KEY")
)

system_prompt = """You are a helpful FAQ assistant with access to a knowledge base.

Your goal is to answer user questions accurately using the available tools.

Guidelines:
1. Start by using the search_faq tool to find relevant information
2. If the initial search doesn't provide enough info, use search_detailed_faq for more results
3. If the query is complex, use reformulate_query to search different aspects
4. Synthesize information from multiple tool calls if needed
5. Always provide a clear, concise answer based on the retrieved information
6. If you cannot find relevant information, clearly state that

Think step-by-step and use tools strategically to provide the best answer."""

logger.info("Creating agent with tools and system prompt")
agent = create_agent(
    model=model,
    tools=tools,
    system_prompt=system_prompt
)

# -------------------- AgentCore Entrypoint --------------------
@app.entrypoint
def agent_invocation(payload, context):
    logger.info("Received payload for agent invocation")
    logger.debug(f"Payload: {payload}")
    logger.debug(f"Context: {context}")
    
    # Extract query from payload
    query = payload.get("prompt", "No prompt found in input")
    logger.info(f"Invoking agent with query: {query}")
    
    # Invoke the graph
    result = agent.invoke({"messages": [("human", query)]})
    
    logger.info("Agent invocation complete")
    logger.debug(f"Result: {result}")
    
    # Return the answer
    return {"result": result['messages'][-1].content}


if __name__ == "__main__":
    logger.info("Starting AgentCore app")
    app.run()

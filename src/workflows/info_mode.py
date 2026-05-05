from src.retrieval.retriever import prepare_policy_texts
from src.retrieval.vector_store import create_vector_store
from src.llm.generator import generate_response
from src.utils.relevance import is_relevant

def run_info_mode(query, policies):
    if not is_relevant(query, policies):
        return "⚠️ I don’t have enough information about that. Try asking about available government schemes."

    texts = prepare_policy_texts(policies)
    db = create_vector_store(texts)

    docs = db.similarity_search(query, k=2)

    context = "\n".join([d.page_content for d in docs])

    prompt = f"""
    Answer clearly using the context below.

    {context}

    Question: {query}
    """

    return generate_response(prompt)
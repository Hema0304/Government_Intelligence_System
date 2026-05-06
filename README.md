# Policy Intelligence System

An AI-powered system for analyzing and retrieving government policies using Retrieval-Augmented Generation (RAG).  
Enables users to query policy documents and receive context-aware, accurate responses.


##  Live Demo
[Live Demo](https://governmentintelligencesystem-edud4yffz7qfkb937gd425.streamlit.app/)


## Problem Statement

Government policies are often lengthy, complex, and difficult to navigate.  
This system simplifies access by enabling users to ask natural language questions and retrieve relevant policy information instantly.


##  Features

-  Document ingestion and processing (PDFs)
-  Semantic search using embeddings
-  Context-aware question answering using LLMs
-  Faster and more relevant results than keyword-based search
-  Interactive UI built with Streamlit



##  Tech Stack

- **Language:** Python  
- **Frameworks:** LangChain  
- **Vector DB:** FAISS  
- **LLMs:** Groq API  
- **Libraries:** Hugging Face Transformers, PyPDF  
- **Frontend:** Streamlit  



##  System Architecture

1. Load policy documents (PDFs)
2. Split text into chunks
3. Generate embeddings
4. Store embeddings in FAISS vector database
5. Retrieve relevant chunks based on user query
6. Generate final response using LLM



##  Project Highlights

- Processed **50+ policy documents**
- Built modular pipeline for ingestion, retrieval, and response generation
- Improved retrieval relevance compared to keyword-based search
- Tested across diverse user queries

## Future Improvements
Add multi-language support
Improve UI/UX design
Integrate real-time policy updates
Add policy comparison and filtering features

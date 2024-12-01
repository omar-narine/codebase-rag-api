# RAG Model Dependencies/Imports
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from langchain_pinecone import PineconeVectorStore
from langchain.embeddings import OpenAIEmbeddings
from langchain_community.embeddings import HuggingFaceEmbeddings
from pinecone import Pinecone
import os
import tempfile
from github import Github, Repository
from git import Repo
from openai import OpenAI
from pathlib import Path
from langchain.schema import Document
from pinecone import Pinecone

# API Dependencies/Imports
import pickle
import numpy as np
from flask import Flask, request, Response
import json
from script.directory_removal import remove_directory_contents

app = Flask(__name__)

SUPPORTED_EXTENSIONS = ['.py', '.js', '.tsx', '.ts', '.java']
IGNORED_DIRS = ["node_modules", ".git", "dist", "__pycache__", '.next', '.vscode', 'env', 'venv']

# pinecone_index = None
# vectorstore = None
repo_url = None

# Root Endpoint to test that API is running as intended
@app.route('/')
def root():
    return Response(json.dumps({
        "status" : "OK"
    }), mimetype="application/json")


@app.route('/embed-repo/', methods=['POST'])
def embed_repo():
    '''
    This endpoint serves to create the vectors for a user provided endpoint. If the provided GitHub repo is new
    and unique, the endpoint will create the vectors for the repo and then store it on PineCone.
    '''
    global repo_url
    
    data = request.get_json()
    repo_url = data['repo_url']
    
    def clone_repo(repo_url):
        repo_name = repo_url.split("/")[-1]
        repo_path = f"./content/{repo_name}"
        Repo.clone_from(repo_url, str(repo_path))
        
        return repo_name
    
    def get_file_content(file_path, repo_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
                rel_path = os.path.relpath(file_path, repo_path)
                
                return {
                    "name": rel_path,
                    "content": content
                }
        except Exception as e:
            return Response(f"Internal Server Error:\nError reading file - {file_path}: {str(e)}", status=500)
    
    def get_main_file_content(repo_path: str):
        files_content = []
        
        try:
            for root, _, files in os.walk(repo_path):
                if any(ignored_dir in root for ignored_dir in IGNORED_DIRS):
                    continue
        
                for file in files:
                    file_path = os.path.join(root, file)
                    if os.path.splitext(file)[1] in SUPPORTED_EXTENSIONS:
                        file_content = get_file_content(file_path, repo_path)
                        if file_content:
                            files_content.append(file_content)
        
        except Exception as e:
            return Response(f"Internal Server Error:\nError reading repository - {str(e)}", status=500)    
        
        return files_content
        
    path = f"./content/{clone_repo(repo_url)}"
    # repo_dir_path = f"./content/{path}"
    file_content = get_main_file_content(path)
    
    pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
    pinecone_index = pc.Index("codebase-rag-api")
    vectorstore = PineconeVectorStore(index_name="codebase-rag-api", embedding=HuggingFaceEmbeddings())
    
    documents = []
    
    for file in file_content:
        doc = Document(
            page_content = f"{file['name'] }\n{file['content']}",
            metadata = {"source":file["name"]}
        )  
        
        documents.append(doc)
        
    vectorstore = PineconeVectorStore.from_documents(
        documents=documents,
        embedding=HuggingFaceEmbeddings(),
        index_name="codebase-rag-api",
        namespace=repo_url
    )
    
    try:
        # Remove the repository contents
        remove_directory_contents(path)
    except Exception as e:
        print(f"Error: {e}")
    
    
    return Response("Successfully cloned repo and stores its contents in PineCone", status=201)


@app.route('/query', methods=["GET"])
def process_query():
    global repo_url
    
    data = request.get_json()
    query = data.get('query')
    repo_url = data.get('repo_url', repo_url)
    
    pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
    pinecone_index = pc.Index("codebase-rag-api")    
    
    client = OpenAI(
        base_url="https://api.groq.com/openai/v1",
        api_key=os.getenv("GROQ_API_KEY")
    )
    
    def get_huggingface_embeddings(text, model_name="sentence-transformers/all-mpnet-base-v2"):
        model = SentenceTransformer(model_name)
        return model.encode(text)
    
    def perform_rag(query):
        raw_query_embedding = get_huggingface_embeddings(query)


        top_matches = pinecone_index.query(vector=raw_query_embedding.tolist(), top_k=5, include_metadata=True, namespace=repo_url)


        # Get the list of retrieved texts
        contexts = [item['metadata']['text'] for item in top_matches['matches']]


        augmented_query = "<CONTEXT>\n" + "\n\n-------\n\n".join(contexts[ : 10]) + "\n-------\n</CONTEXT>\n\n\n\nMY QUESTION:\n" + query


        # Modify the prompt below as need to improve the response quality
        system_prompt = f"""You are a Senior Software Engineer, specializing in various common language including Python, TypeScript, Java, C, Kotlin, Rust, Swift, etc.
        
        You have the task of leading a team on a new project where you are the lead engineer and as a result, you will be integrating with a lot of people from different teams and with different levels of technical knowledge. It is important to understand that because the different people you will be meeting with will have different levels of technical knowledge, that you must ensure your response will fit the level of understanding that the person asking the question has. 
        
        You should use the complexity of the question in order to determine the level of technical expertise an individual might have. For exmaple, if someone asks you "What does this project do," you can expect that they don't have a high technical background and want a high level overview of what this codebase does and how it is able to do so. If an individual asks a more complex question like "How is the JavaScript pasrser implemented," you can imagine them as being an individual on their team and should provide a more thorough response to aide in breaking down the codebase for this person. 
        
        Your follow up questions should be subtle and should not be pushy. You should assume the person's level of technical background and should avoid asking direct questions about what they know and how much they know. This will allow for you to best cater to the questions of the most people!
        
        Answer all questions that are being asked of you about the codebase, based on the code provided. CONTEXT FOR THE QUESTION WILL ALWAYS BE PROVIDED. Always consider all of the context provided when forming a response. In your response, ask follow up questions so that the person has an opportunity to confirm their understanding based on your question and/or further their understanding of the codebase. Be thorough in your responses.
        """


        llm_response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": augmented_query}
            ]
        )


        return llm_response.choices[0].message.content
    
    rag_response = perform_rag(query)
    
    json_msg = {
        "response": rag_response,
        "message": "RAG Response Successful",
        "status": 200
    }
    
    return Response(json.dumps(json_msg), status=200, mimetype='application/json')

if __name__ == '__main__':
    app.run()
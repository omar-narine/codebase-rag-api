# Codebase Retrieval API
=====================================

A robust API for retrieving codebase information and embeddings for software development and research.

## Overview
-----------

This API is designed to index and query large codebases for software development, debugging, and research purposes. It utilizes PineCone for vector store operations and OpenAI's LLM for context-aware retrieval. The API provides endpoints for:

1. Repository Indexing (Embed-repo): Indexes a given GitHub repository, retrieves code snippet embeddings, and stores them in a PineCone vector store.
2. Query Resolution (Query): Performs context-aware retrieval using a given query and a repository index, providing relevant code snippets and augmenting the query for more accurate results.

## API Endpoints
-----------------

### Embed-repo Endpoint

The embed-repo endpoint POSTs a GitHub repository URL to embed-repo, clones the repository, extracts relevant code snippets, and stores their embeddings in PineCone.

* URL: `/embed-repo/`
* Request Body: A JSON object with a single key-value pair containing the GitHub repository URL (`repo_url`).
* Response: A JSON response indicating successful repository cloning and embed-store operations.

### Query Endpoint

The query endpoint makes a GET request to retrieve code snippet information using a given query and a repository index.

* URL: `/query/`
* Request Body: A JSON object with two key-value pairs containing the OpenAI query (`query`), the repository URL or index name (`repo_url`).
* Response: A JSON response with the LLM-generated augmented query, the retrieved code snippet information, and a success message.

## Integrating with the Codebase Retrieval API
---------------------------------------------

### Repository Indexing

1. Clone the repository using the embed-repo endpoint.
2. Extract the repository information and code snippet embeddings using the query endpoint.
3. Integrate with your preferred LLM for further querying and response generation.

## Contributing
--------------

Contributions to this project are encouraged! Feel free to share your improvements, test cases, or even research ideas on our [Contributing Guidelines](Contributing-Guidelines).

## Running the API
-------------------

1. Clone this repository.
2. Import necessary dependencies: `pip install requirements.txt`
3. Set environment variables (e.g., `GROQ_API_KEY`, `PINECONE_API_KEY`, etc.).
4. Run the API: `python app.py`

Note: Before running the API, make sure to create a `.env` file with your API keys and other necessary configuration.

# License
--------

Copyright (c) [Year] [Author]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

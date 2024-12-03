# Codebase RAG API

## Project Overview

This is a server-side API that integrates with the Pinecone vector store and the OpenAI API to enable remote code reviews and provide augmentative query responses for developers working on a codebase.

## Functionality

This API has two primary endpoints:

### /embed-repo

* Clones a GitHub repository
* Processes its contents using Hugging Face embeddings
* Stores it in the Pinecone vector store for efficient similarity searches

### /query

* Takes a query as input
* Generates an augmented prompt for the query
* Sends it to the OpenAI API for a response
* Provides an informative response to assist with code reviews or answer developer questions about the codebase

## Key Features

* Codebase Processing: The API clones a GitHub repository, extracts relevant files, and processes its contents using Hugging Face embeddings.
* Pinecone Vector Store: The API uses Pinecone as a vector store to enable efficient similarity searches across the codebase.
* OpenAI Integration: The API leverages the OpenAI API to provide augmentative query responses for developers working on the codebase.
* Augmented Prompts: The API generates custom prompts for the OpenAI API based on the query, leveraging the context of the codebase.

## Technical Details

This API is built using Flask as the web framework and utilizes various libraries, including:

* Flask: For creating the web API
* Pinecone: For vector storage and similarity search
* OpenAI API: For augmentative query responses
* Hugging Face: For embeddings and input processing
* Sentence Transformers: For sentence embeddings

## Getting Started

To run this API, ensure you have the following dependencies installed:

* Flask
* Pinecone
* OpenAI API
* Hugging Face
* Sentence Transformers

You'll also need to set the environment variables PINECONE_API_KEY and GROQ_API_KEY with your respective API keys.

You can clone the repository and run the API using the following commands:

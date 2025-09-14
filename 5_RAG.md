# 5. Retrieval Augmented Generation (RAG)

RAG is a technique which is useful when we want to retrieve/ extract relevant sections of large documents to answering specific questions. 

Jupyter Notebooks:
1. [001_chunking.ipynb](./notebooks/5-rag/001_chunking.ipynb)

## Option 1: Include The Entire Doc Into The Prompt 

This is not a good approach because:
1. There's a hard limit on how much text can be fed into Claude 
2. Claude get's less effective as prompts gets longer
3. Performance degrades when there's too much information
4. Long prompt = more $$$
5. Long prompt = more time to process

## Option 2: Include Relevant Chunks Into The Prompt

In this approach we:
1. Split the document into smaller **chunks**.
   - Chunking could be based on equal portions or relevant headers/ sections or by semantic meaning or other strategies.
2. When the user asks a question, find the most relevant chunk.
3. Include the relevant chunk in the prompt to Claude.

![Option 2 RAG](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748559475%2F09_-_001_-_Introducing_Retrieval_Augmented_Generation_09.1748559475445.png)

## Benefits of RAG

- Claude only focuses on the most relevant content and tunes out irrelevant content.
- Scales to very large documents and multiple documents.
- Smaller prompts = lower costs & faster processing.

## Challenges with RAG

- Requires preprocessing steps to chunk documents.
- Needs a mechanism to find relevant chunks (retrieval).
- Retrieved chunks may not have all the necessary context.
- Some chunking approach may work better in some cases, while others may work better for other cases. 

## When To Use RAG

- While working with large documents - usually beyond what can fit into a single prompt.
- When technical implementation of chunking, search & retrieval makes sense for the application.

## Text Chunking Strategies

This is one of the **most critical** steps in the RAG pipeline. 

We can divide text based on:
1. Size: divide the text into strings of equal length 
2. Structure: divide based on document structure (like headers, paragraphs, sections) 
3. Semantic Meaning: group related sections using NLP

### Size Based Chunking

- Easiest technique. 
- Most often used in production.

#### Downsides

- Each chunk has a cutoff text
- Each chunk lacks context

#### Workaround

Add an overlap with neighboring chunks to solve the above two problems, however, this causes duplication of text.

### Structure Based Chunking

We can programmatically split chunks based on headers such as the ones in a Markdown (MD) file. This works well for MD files but in reality most documents may not be formatted in MD.

Implementation can be challenging in plain text files or inconsistently formatted documents.

### Semantic Based Chunking

Here we divide text into groups of related sentences or sections. This would require us to use NLP techniques to understand the meaning of individual sentences so that similar ones can be placed in the same group. This is computationally expensive but can retrieve more relevant chunks.

### Choosing the Right Strategy

Chunking strategy is solely based on the use case:

- **character based:** Most reliable fallback & works with any document type.
- **sentence based:** Good balance of context and meaning for the prose.
- **section based:** excellent results when you have consistent structure in documents.

## Semantic Search Using Text Embeddings

Once we have chunks of text, the next step in the RAG pipeline is to determine which chunks are related to a user query. We can't just do keyword based search, we need to understand both the meaning & context of the question and the chunks. In other words, we need to do semantic search using text embeddings.

### Text Embeddings

These are numeric representations of the meaning contained in the text. The text is converted into vectors (list of numbers ranging from -1 to 1). 

![text embeddings](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748559465%2F09_-_003_-_Text_Embeddings_05.1748559464827.png)

Each of these numbers represent a score for some quality or metric of the input. For example: 
- how "happy" the text is
- how much the text talks about "movies"
- how much the text talks about "games"
- ...

We don't know exactly what each number denotes but the above examples state the idea of how each number can tell models about what information they contain.

#### Why Embeddings Matter for RAG

Embeddings are very useful because similar texts will have similar embedding values. This way we can mathematically compare a user's question to the chunks & find semantically similar ones - even if they are not worded the same way.
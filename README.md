# Claude with AWS Bedrock

This repository contains my notes for the [Claude with Amazon Bedrock](https://anthropic.skilljar.com/claude-in-amazon-bedrock) course from Anthropic Academy.

## High Level Overview
![Architecute overview](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748557572%2F05_-_001_-_Accessing_the_API_08.1748557571907.png)

<!-- ## My Learnings

1. [Working with the Amazon AWS Bedrock API](./1_BEDROCK_API.md)
2. [Prompt Evaluations](./2_PROMPT_EVALS.md)
3. [Prompt Engineering](./3_PROMPT_ENG.md)
4. [Tool Use](./4_TOOL_USE.md)
5. [Retrieval Augmented Generation](./5_RAG.md)
6. Features of Claude
7. Model Context Protocol
8. Agents -->

### Quick Navigation

**🚀 Getting Started**
- [Setup Instructions](#setup) - Environment configuration
- [AWS Bedrock API](./1_BEDROCK_API.md) - API fundamentals

**📖 Learning Path**
- [Prompt Evaluation Methods](./2_PROMPT_EVALS.md) - Testing and validation
- [Prompt Engineering](./3_PROMPT_ENG.md) - Prompting techniques and best practices
- [Tool Implementation](./4_TOOL_USE.md) - Advanced tool use
- [RAG Techniques](./5_RAG.md) - Complete Retrieval Augmented Generation guide
- [Claude Features](./6_CLAUDE.md) - Extended Thinking, Image and PDF Support, Citations, Prompt Caching
- [Model Context Protocol](./7_MCP.md) - MCP Client, Server, Tools, Resources & Prompts
- [AI Agents](./8_AGENTS.md) - Agents, Claude Code, MCP servers, Computer Use

## Project Structure

```
claude-aws-bedrock/
├── 📚 Documentation
│   ├── 1_BEDROCK_API.md          # AWS Bedrock API usage and examples
│   ├── 2_PROMPT_EVALS.md         # Prompt evaluation techniques
│   ├── 3_PROMPT_ENG.md           # Prompt engineering strategies
│   ├── 4_TOOL_USE.md             # Tool use and function calling
│   ├── 5_RAG.md                  # Retrieval Augmented Generation
│   └── 6_CLAUDE.md               # Claude features and capabilities
│
├── 📓 Jupyter Notebooks
│   ├── 1-working-with-aws-bedrock/
│   │   ├── 001_Api_Requests.ipynb           # Basic API requests
│   │   ├── 002_System_Messages_Temperature.ipynb  # Temperature control
│   │   ├── 003_Streaming.ipynb              # Streaming responses
│   │   └── 004_Controlling_Output.ipynb     # Output control techniques
│   │
│   ├── 2-prompt-evaluations/
│   │   └── 001_Prompt_Evals.ipynb           # Prompt evaluation methods
│   │
│   ├── 3-prompt-engineering/
│   │   ├── 001_prompting.ipynb              # Prompt engineering basics
│   │   └── 002_exercise.ipynb               # Hands-on exercises
│   │
│   ├── 4-tool-use/
│   │   ├── 001_tools.ipynb                  # Tool use fundamentals
│   │   ├── 003_structured_data.ipynb        # Structured data handling
│   │   ├── 005_text_editor_tool.ipynb       # Text editor tool implementation
│   │   ├── main_file.py                     # Main application file
│   │   └── test_main_file.py                # Test file
│   │
│   ├── 5-rag/
│   │   ├── 001_chunking.ipynb               # Text chunking strategies
│   │   ├── 002_embeddings.ipynb             # Embedding generation
│   │   ├── 003_vectordb.ipynb               # Vector database setup
│   │   ├── 004_bm25.ipynb                   # BM25 retrieval
│   │   ├── 005_hybrid.ipynb                 # Hybrid search methods
│   │   ├── 006_reranking.ipynb              # Result reranking
│   │   ├── 007_contextual.ipynb             # Contextual retrieval
│   │   └── report.md                        # RAG analysis report
│   │
│   └── 6-claude-features/
│       ├── 001_thinking.ipynb               # Claude's thinking capabilities
│       └── 001_thinking_complete.ipynb      # Complete thinking example
│
├── 📊 Evaluation Data
│   └── evals/
│       ├── 2-prompt-evals/                  # Prompt evaluation datasets
│       └── 3-prompt-eng/                    # Prompt engineering datasets
│
├── 🖼️ Images
│   └── images/                              # Documentation images and diagrams
│
├── 📋 Configuration
│   ├── requirements.txt                     # Python dependencies
│   └── README.md                            # This file
```

## Setup

### AWS

1. Login to AWS Console & navigate to Bedrock.
2. Make sure that you are in the correct region (eg: US East 2) --> This is really important as the models that we will request in the next step are specific to a region.
3. Request for Model Access for the LLM (if not already granted)
4. Generate API Keys (Short term or long term) and copy it.
   This generates a new IAM User with the right role.

### Local (Python)

1. Create a virtual environment.
    ```bash
    python -m venv .venv
    ```
2. Activate the virtual environment.

    On MacOS/ Linux:
    ```bash
    source .venv/bin/activate
    ```
    On Windows:
    ```bash
    .\.venv\Scripts\activate.bat
    ```
3. Download dependencies from the `requirements.txt` file:
    ```bash
    pip install -r requirements.txt
    ```
4. Create `.env` file for the secret keys and add the API Key from step 4 in the AWS Setup. The `.env.example` is an example env file.
5. Load the environment variables before making a request to use AWS Bedrock.

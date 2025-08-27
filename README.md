# Claude with AWS Bedrock

This repository contains my notes for the [Claude with Amazon Bedrock](https://anthropic.skilljar.com/claude-in-amazon-bedrock) course from Anthropic Academy.

## High Level Overview
![Architecute overview](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748557572%2F05_-_001_-_Accessing_the_API_08.1748557571907.png)

## My Learnings

1. [Working with the Amazon AWS Bedrock API](./1_BEDROCK_API.md)
2. [Prompt Evaluations](./2_PROMPT_EVALS.md)
3. [Prompt Engineering](./3_PROMPT_ENG.md)
4. Tool Use
5. Retrieval Augmented Generation
6. Features of Claude
7. Model Context Protocol
8. Agents

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

# Claude with AWS Bedrock

This repository contains my notes for the [Claude with Amazon Bedrock](https://anthropic.skilljar.com/claude-in-amazon-bedrock) course from Anthropic Academy.

## AWS Setup

1. Login to AWS Console & navigate to Bedrock.
2. Make sure that you are in the correct region (eg: US East 2)
3. Request for Model Access for the LLM (if not already granted)
4. Generate API Keys (Short term or long term) and copy it.
   This generates a new IAM User with the right role.

## Local (Python)

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
4. Create `.env` file for the secret keys and add the API Key from step 4 in the AWS Setup
5. Load the environment variables before making a request to use AWS Bedrock.

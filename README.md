# Claude with AWS Bedrock

This repository contains my notes for the [Claude with Amazon Bedrock](https://anthropic.skilljar.com/claude-in-amazon-bedrock) course from Anthropic Academy.

## Setup

### AWS

1. Login to AWS Console & navigate to Bedrock.
2. Make sure that you are in the correct region (eg: US East 2) --> This is really important as the models that we will request in the next step are specific to the regions.
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
4. Create `.env` file for the secret keys and add the API Key from step 4 in the AWS Setup
5. Load the environment variables before making a request to use AWS Bedrock.

## Bedrock Runtime

```python
import boto3
client = boto3.client("bedrock-runtime", region_name="us-east-2")
```

Some models are not available on all regions. To solve the problem of which model is present in which region, we have inference profiles.

## Inference Profile
Automatically routes request to other regions where a specific model is hosted. If it is not in us-east-2 and present in us-west-2, then it will automatically request for it from there. Therefore, we add the inference profile id to get a specific model.

```python
# we use the inference profile ID for on-demand access to the model
model_id = "us.anthropic.claude-3-5-haiku-20241022-v1:0"
```

## Messages Structure

User Message:

```json
{
    'role': 'user', 
    'content': [{
            'text': 'What is 1+1?'
        }
    ]
}
```

AI Assistant Message:

```json
{
    'role': 'assistant', 
    'content': [{
            'text': '1+1 = 2'
        }
    ]
}

```

## Bedrock Converse API

We use the converse API to call a specific model with our user prompt & system prompt.

```python
params = {
    "modelId": model_id,
    "messages": messages,
    "system": [{
        "text": system_prompt
    }],
    "inferenceConfig": { 
        "temperature": temperature 
    }
}

response = client.converse(**params)
```

To abstract this further, we can define a method called `chat` which can perform this API call.

```python
def chat(messages, system=None, temperature=1.0):
    params = {
        "modelId": model_id,
        "messages": messages,
        "inferenceConfig": { "temperature": temperature }
    }
    if system:
        params["system"] = [{"text": system}]
    
    response = client.converse(**params)
    return response["output"]["message"]["content"][0]["text"]
```

## Multi-Turn Conversations

As Claude on AWS Bedrock does not have any memory. For continuing previous conversations, we must chain messages together in a list to give the AI context.
``` python
messages = [user_message1, assistant_message1, usermessage2, assistant_message2, ...] 
```

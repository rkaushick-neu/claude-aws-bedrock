# Claude with AWS Bedrock

This repository contains my notes for the [Claude with Amazon Bedrock](https://anthropic.skilljar.com/claude-in-amazon-bedrock) course from Anthropic Academy.

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
    "role": "user", 
    "content": [{
            "text": "What is 1+1?"
        }
    ]
}
```

AI Assistant Message:

```json
{
    "role": "assistant", 
    "content": [{
            "text": "1+1 = 2"
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
        "temperature": temperature,
        "stopSequences": stop_sequences 
    }
}

response = client.converse(**params)
```

To abstract this further, we can define a method called `chat` which can perform this API call.

```python
def chat(messages: list[dict], system: str | None = None, temperature: float = 1.0, , stop_sequences: list[str] = []) -> str:
    params = {
        "modelId": model_id,
        "messages": messages,
        "inferenceConfig": { 
            "temperature": temperature,
            "stopSequences": stop_sequences
        }
    }
    if system:
        params["system"] = [{"text": system}]
    
    response = client.converse(**params)
    return response["output"]["message"]["content"][0]["text"]
```

## Multi-Turn Conversations

As Claude on AWS Bedrock does not have any memory. For continuing previous conversations, we must chain messages together in a list to give the AI context.

``` python
messages = [user_message1, assistant_message1, user_message2, assistant_message2, ...] 
```

## Streaming

We can stream data from Bedrock using the **converse_stream** function:

```python
response = client.converse_stream(messages=messages, modelId=model_id)
```

![Streaming text as it gets generated](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748557673%2F05_-_008_-_Streaming_03.1748557673079.png)

### Response

```json
{
    "ResponseMetadata": {
        "RequestId": "4baa0075-f4ae-4eee-bb16-db1fe1c3f724", 
        "HTTPStatusCode": 200, 
        "HTTPHeaders": {
            "date": "Sat, 23 Aug 2025 15:33:59 GMT", 
            "content-type": "application/vnd.amazon.eventstream", 
            "transfer-encoding": "chunked", 
            "connection": "keep-alive", 
            "x-amzn-requestid": "4baa0075-f4ae-4eee-bb16-db1fe1c3f724"
        }, 
        "RetryAttempts": 0
    }, 
    "stream": <botocore.eventstream.EventStream object at 0x10b9a7b10>
}
```

### Steam Events

The stream event contains many event types within the response stream object:

![Stream event components](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748557673%2F05_-_008_-_Streaming_12.1748557673618.png)



#### Response Stream Event Objects

Here we get a stream object generator which we can loop through to display the message. Looping through the stream object:

```json
{"messageStart": {"role": "assistant"}}
{"contentBlockDelta": {"delta": {"text": "F"}, "contentBlockIndex": 0}}
{"contentBlockDelta": {"delta": {"text": "al"}, "contentBlockIndex": 0}}
{"contentBlockDelta": {"delta": {"text": "seData"}, "contentBlockIndex": 0}}
{"contentBlockDelta": {"delta": {"text": " is a fictional database"}, "contentBlockIndex": 0}}
// ... multiple more "contentBlockDelta"s
{"contentBlockDelta": {"delta": {"text": " systems without"}, "contentBlockIndex": 0}}
{"contentBlockDelta": {"delta": {"text": " privacy concerns."}, "contentBlockIndex": 0}}
{"contentBlockStop": {"contentBlockIndex": 0}}
{"messageStop": {"stopReason": "end_turn"}}
{"metadata": {
    "usage": {
        "inputTokens": 18, 
        "outputTokens": 54, 
        "totalTokens": 72
    }, 
    "metrics": {"latencyMs": 1822}
    }
}
```

Therefore, while looping to retrieve the content from the event, we can extract it from
```python
response["stream"]["contentBlockDelta"]["delta"]["text"]
```

## Controlling Outputs

### Message Prefilling

![Message Prefilling Code Snippet](/images/Message_prefilling_code.png)

### Stop Sequences

Force Claude to end its response immediately when it encounters a specific text.

![Stop Sequences](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748557717%2F05_-_009_-_Controlling_Model_Output_14.1748557717103.png)

### Generating Structured Code Outputs with Message Prefilling & Stop Sequences

```python
prompt = """
Generate three different sample AWS CLI commands. Each should be very short.
"""

add_user_message(messages, prompt)
add_assistant_message(messages, "Here are the three commands in a single block without any comments: \n```bash")

text = chat(messages, stop_sequences=["```"])
```

Through this technique we make sure that Claude generates only code. It would not generate any headings or other text in the beginning because of the prefilled message. As soon as the code is generated, the stop sequence causes Claude to stop generating any further explanations.

The above technique can also be used for other structured data such as:
- Code snippets (Python, JavaScript, ...)
- Bulleted lists
- CSV data
- Configuration files
- Any format where clean, copyable output matters
# 4. Tool Use

Relevant Notebooks:
- [001_tools.ipynb](./notebooks/4-tool-use/001_tools.ipynb)


LLMs do not have access to up-to-date data & have only knowledge on what they have been trained on. Tools create a bridge between Claude & external data sources.

## How Tool Use Works

1. Initial Request:  You send Claude a question along with instructions on how to get extra data.
2. Tool Request: Claude analyses the question and decides it needs specific external data.
3. Data Retrieval: The requested information is fetched from the tool.
4. Final Response: Claude uses the external data to provide a complete answer.

## Steps to Making Tools

1. Write a tool function
2. Write a JSON schema
3. Call Claude with JSON schema
4. Run tool
5. Add tool result and call Claude again

## Use Case

We want to teach Claude to set reminders:

```
Set a reminder for my doctor's appointment. It's a week from Thursday.
```

## 1. Tools Functions

1. Get the current date-time
    ```python
    def get_current_date_time(date_format="%Y-%m-%d %H:%M:%S"):
        return datetime.now().strftime(date_format)

    get_current_date_time()
    ```
2. Add duration to data-time
3. Set a reminder

## 2. JSON Schema Specifications

![JSON Schema Spec](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748558031%2F08_-_003_-_JSON_Schema_for_Tools_04.1748558031698.png)

### Purpose

1. Helps LLMs understand what arguments are required by the tool function.
2. Used for data validation across many programming contexts.

### Best Practices

- Explain what it does, when to use it & what it returns
- Aim for 3 to 4 sentences in your descriptions
- Provide detailed descriptions for parameters

JSON schema for get current date time tool:
```json
    {
        "toolSpec": {
            "name": "get_current_date_time",
            "description": "Retrieves the current date and time formatted according to the specified format string. This tool returns the system's current local date and time as a formatted string. It should be used when the user needs to know the current date, time, or both in a specific format. The tool uses Python's datetime.now() function internally, so it will reflect the server's local time zone settings. This tool does not support retrieving dates or times for different time zones or historical/future dates.",
            "inputSchema": {
                "json": {
                    "type": "object",
                    "properties": {
                        "date_format": {
                            "type": "string",
                            "description": "The format for returning the date-time as per Python strftime."
                        }
                    },
                    "required": [
                        "date_format"
                    ]
                }
            }
        } 
    }
```

## 3. Call Claude with JSON  (& Receive a ToolUse Part)

```python
params = {
        "modelId": model_id,
        "messages": messages,
        "inferenceConfig": {
            "temperature": temperature,
            "stopSequences": stop_sequences,
        },
        "toolConfig": {
            "tools": tools, 
            "toolChoice": {"auto": {}} # or { "any": {} } or { "name": "tool-name" }
        }
    }
```

### Controlling Tool Use Using 'toolChoice'
![auto, any and tool](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748558036%2F08_-_004_-_Handling_Tool_Use_Responses_02.1748558036403.png)

#### Response from Claude After Sending the JSON Spec
```json
{
    "ResponseMetadata": {
        "RequestId": "b572382e-a05d-4b7f-a72f-126e09bbab80", 
        "HTTPStatusCode": 200, 
        "HTTPHeaders": {
            "date": "Sun, 07 Sep 2025 17:11:58 GMT", 
            "content-type": "application/json", 
            "content-length": "486", 
            "connection": "keep-alive", 
            "x-amzn-requestid": "b572382e-a05d-4b7f-a72f-126e09bbab80"
        }, 
        "RetryAttempts": 0
    }, 
    "output": {
        "message": {
            "role": "assistant", 
            "content": [
                {"text": "I can help you find out the current time. Let me check that for you."}, 
                {"toolUse": {
                    "toolUseId": "tooluse_0-ZlzEmcRNaHuiNSnjVw7A", 
                    "name": "get_current_datetime", 
                    "input": {"date_format": "%H:%M:%S"}
                }}
            ]
        }
    }, 
    "stopReason": "tool_use", 
    "usage": {
        "inputTokens": 614, 
        "outputTokens": 80, 
        "totalTokens": 694, 
        "cacheReadInputTokens": 0, 
        "cacheWriteInputTokens": 0
    }, 
    "metrics": {"latencyMs": 1855}
}
```

When the response has "stopReason" as "tool_use".

### Assistant Message

1. **Text part**: That says Claude will find the information using a tool use.
2. "**toolUse" part**: Containing:
    - "toolUseId": 
    - "name": name of the tool to run - this is the name from the json schema spec (also the function)
    - "input": dictionary of the input args that Claude wants to pass inside the tool function

## 4. Run The Tool (& Second ToolResult Part)

Once we get the assistant message, we need to run the tool and the result of the tool needs to be sent back to Claude as a user message while including a **ToolResult Part**.

### Run The Tool
```python
# this is the function that goes thru each of the tools and calls the run_tool function (which in turn calls the tool method definition)
def run_tools(parts):
    tool_requests = [part for part in parts if "toolUse" in part]
    tool_result_parts = []

    for tool_request in tool_requests:
        tool_use_id = tool_request["toolUse"]["toolUseId"]
        tool_name = tool_request["toolUse"]["name"]
        tool_input = tool_request["toolUse"]["input"]

        # print(f"I need to run tool {tool_name} with args {tool_input}")

        tool_output = run_tool(tool_name, tool_input)
        print(tool_output)

run_tools(parts)
```

The above code returns:

```json
[{"toolResult": {"toolUseId": "tooluse_bbod_JYMTKawCgY4QiJbaQ",
   "content": [{"text": "09:52:39"}],
   "status": "success"}}]
```

## 5. Send Tool Result To Claude

We take the above result and add it into the messages as follows:

```json
[{"role": "user", "content": [{"text": "What time is it?"}]},
 {"role": "assistant",
  "content": [{"text": "I'll help you find out the current time. Let me check that for you."},
   {"toolUse": {"toolUseId": "tooluse_bbod_JYMTKawCgY4QiJbaQ",
     "name": "get_current_datetime",
     "input": {"date_format": "%H:%M:%S"}}}]},
 {"role": "user",
  "content": [{"toolResult": {"toolUseId": "tooluse_bbod_JYMTKawCgY4QiJbaQ",
     "content": [{"text": "09:52:39"}],
     "status": "success"}}]}]

```

**Important:** Make sure to send the JSON schema to claude again while sending the result of the tool call. Otherwise, it won't understand what the tool does.

![running the tool](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748558038%2F08_-_004_-_Handling_Tool_Use_Responses_11.1748558037792.png)

## Conversation Loop (with & without tool calls)

Whenever we receive a message from the assistant that the `stop_reason` is *tool_use*, we need to execute the tool and resend the message back to Claude. If `stop_reason` is not present, we can end the loop.

### Different Stop Reasons

1. **tool_use:** Model needs to call a tool
2. **end_turn:** Model finished generating it's assistant message
3. **max_tokens:** Model hit output token limit
4. **stop_sequence:** Model has encountered one of the user provided stop sequences
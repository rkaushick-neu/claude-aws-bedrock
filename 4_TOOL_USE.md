# 4. Tool Use

LLMs do not have access to up-to-date data & have only knowledge on what they have been trained on. Tools create a bridge between Claude & external data sources.

Relevant Notebooks:
- [001_tools.ipynb](./notebooks/4-tool-use/001_tools.ipynb)
- [003_structured_data.ipynb](./notebooks/4-tool-use/003_structured_data.ipynb)
- [005_text_editor_tool.ipynb](./notebooks/4-tool-use/005_text_editor_tool.ipynb)

## Table of Contents

- [4. Tool Use](#4-tool-use)
  - [Table of Contents](#table-of-contents)
  - [How Tool Use Works](#how-tool-use-works)
  - [Steps to Making Tools](#steps-to-making-tools)
  - [Use Case](#use-case)
  - [1. Tools Functions](#1-tools-functions)
  - [2. JSON Schema Specifications](#2-json-schema-specifications)
    - [Purpose](#purpose)
    - [Best Practices](#best-practices)
  - [3. Call Claude with JSON  (\& Receive a ToolUse Part)](#3-call-claude-with-json---receive-a-tooluse-part)
    - [Controlling Tool Use Using 'toolChoice'](#controlling-tool-use-using-toolchoice)
      - [Response from Claude After Sending the JSON Spec](#response-from-claude-after-sending-the-json-spec)
    - [Assistant Message](#assistant-message)
  - [4. Run The Tool (\& Second ToolResult Part)](#4-run-the-tool--second-toolresult-part)
    - [Run The Tools](#run-the-tools)
  - [5. Send Tool Result To Claude](#5-send-tool-result-to-claude)
  - [Conversation Loop (with \& without tool calls)](#conversation-loop-with--without-tool-calls)
    - [Different Stop Reasons](#different-stop-reasons)
  - [Batch Tool Use (For Parallel Tool Use)](#batch-tool-use-for-parallel-tool-use)
    - [Claude Sonnet 4 (Requesting Multiple Tools)](#claude-sonnet-4-requesting-multiple-tools)
    - [Claude Sonnet 3.7 (Requesting One Tool at a Time)](#claude-sonnet-37-requesting-one-tool-at-a-time)
    - [Claude Sonnet 3.7 (Again with Batch Tool)](#claude-sonnet-37-again-with-batch-tool)
  - [Structured Output With Tools](#structured-output-with-tools)
    - [Approach](#approach)
    - [Key Benefits of Using a Tool for Structured Output](#key-benefits-of-using-a-tool-for-structured-output)
  - [Flexible Tool for Structured Data Extraction](#flexible-tool-for-structured-data-extraction)
  - [Claude's Text Editor Tool](#claudes-text-editor-tool)
    - [Understanding With An Example](#understanding-with-an-example)
    - [Commands](#commands)
      - [Defining Commands](#defining-commands)
    - [Practical Application](#practical-application)

## How Tool Use Works

1. Initial Request:  You send Claude a question along with instructions on how to get extra data.
2. Tool Request: Claude analyses the question and decides it needs specific external data.
3. Data Retrieval: The requested information is fetched from the tool.
4. Tool Response: We run the requested tool and send the output to Claude. 
5. Final Response: Claude uses the tool response to provide a complete answer.

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

### Run The Tools

To run a tool we define a `run_tool` function:

```python
# runs the specific tool based on the input it requires
def run_tool(tool_name, tool_input):
    # TODO: tutorial says to hard-code but there must be a better way
    if tool_name == "get_current_datetime":
        # we use the ** in the input because it is a dictionary input
        return get_current_datetime(**tool_input)
    # multiple more elif statements if required ...
    else:
        raise Exception(f"Unknown tool name: {tool_name}")
```

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

```python
def run_conversation(messages):
    while True:
        result = chat(messages=messages, tools=[get_current_datetime_schema])

        add_assistant_message(messages, result["parts"])
        print(result["text"])

        if(result["stop_reason"] != "tool_use"):
            break

        tool_result_parts = run_tools(result["parts"])
        add_user_message(messages, tool_result_parts)

    return messages
```

### Different Stop Reasons

1. **tool_use:** Model needs to call a tool
2. **end_turn:** Model finished generating it's assistant message
3. **max_tokens:** Model hit output token limit
4. **stop_sequence:** Model has encountered one of the user provided stop sequences

## Batch Tool Use (For Parallel Tool Use)

When the user asks a question, the newer versions of Claude (like Sonnet 4) can natively request to run multiple tools. However older versions, would sequentially request each tool.

### Claude Sonnet 4 (Requesting Multiple Tools)

```json
[{"role": "user",
  "content": [{"text": "What is March 12th, 2025 + 50 days? Also, what is March 12th, 2025 + 100 days?"}]},
 {"role": "assistant",
  "content": [{"text": "I'll calculate those future dates for you by adding the specified number of days to March 12th, 2025."},
   {"toolUse": {"toolUseId": "tooluse_RdoGanMgR9a7TVW05tn99A",
     "name": "add_duration_to_datetime",
     "input": {"datetime_str": "2025-03-12",
      "duration": 50,
      "input_format": "%Y-%m-%d",
      "unit": "days"}}}]},
 {"role": "user",
  "content": [{"toolResult": {"toolUseId": "tooluse_RdoGanMgR9a7TVW05tn99A",
     "content": [{"text": "Thursday, May 01, 2025 12:00:00 AM"}],
     "status": "success"}}]},
 {"role": "assistant",
  "content": [{"toolUse": {"toolUseId": "tooluse_3fBhKHG7TcGo_MUT4DPCkQ",
     "name": "add_duration_to_datetime",
     "input": {"duration": 100,
      "unit": "days",
      "datetime_str": "2025-03-12",
      "input_format": "%Y-%m-%d"}}}]},
 {"role": "user",
  "content": [{"toolResult": {"toolUseId": "tooluse_3fBhKHG7TcGo_MUT4DPCkQ",
     "content": [{"text": "Friday, June 20, 2025 12:00:00 AM"}],
     "status": "success"}}]},
 {"role": "assistant",
  "content": [{"text": "Here are your results:\n\n- March 12th, 2025 + 50 days = Thursday, May 1st, 2025\n- March 12th, 2025 + 100 days = Friday, June 20th, 2025"}]}]
```

### Claude Sonnet 3.7 (Requesting One Tool at a Time)

```json
[{"role": "user",
  "content": [{"text": "What is March 12th, 2025 + 50 days? Also, what is March 12th, 2025 + 100 days?"}]},
 {"role": "assistant",
  "content": [{"text": "I'll calculate those future dates for you by adding the specified number of days to March 12th, 2025."},
   {"toolUse": {"toolUseId": "tooluse_RdoGanMgR9a7TVW05tn99A",
     "name": "add_duration_to_datetime",
     "input": {"datetime_str": "2025-03-12",
      "duration": 50,
      "input_format": "%Y-%m-%d",
      "unit": "days"}}}]},
 {"role": "user",
  "content": [{"toolResult": {"toolUseId": "tooluse_RdoGanMgR9a7TVW05tn99A",
     "content": [{"text": "Thursday, May 01, 2025 12:00:00 AM"}],
     "status": "success"}}]},
 {"role": "assistant",
  "content": [{"toolUse": {"toolUseId": "tooluse_3fBhKHG7TcGo_MUT4DPCkQ",
     "name": "add_duration_to_datetime",
     "input": {"duration": 100,
      "unit": "days",
      "datetime_str": "2025-03-12",
      "input_format": "%Y-%m-%d"}}}]},
 {"role": "user",
  "content": [{"toolResult": {"toolUseId": "tooluse_3fBhKHG7TcGo_MUT4DPCkQ",
     "content": [{"text": "Friday, June 20, 2025 12:00:00 AM"}],
     "status": "success"}}]},
 {"role": "assistant",
  "content": [{"text": "Here are your results:\n\n- March 12th, 2025 + 50 days = Thursday, May 1st, 2025\n- March 12th, 2025 + 100 days = Friday, June 20th, 2025"}]}]
```

If want to **FORCE Claude** to call multiple tools we can create another tool called 'Batch Tool'. In our JSON tool spec we must mention:

1. Name & description of the tool:
    ```json
    {
        "name": "batch_tool",
        "description": "Invoke multiple other tool calls simultaneously",
    }
    ```
2. Input arguments to the batch tool:
   - This will be a list of tool calls. Each tool call must have the parameters - name (of the tool to be called) & args for that tool call.
    ```json
    {
        "json": {
            "type": "object",
            "properties": {
                "invocations": {
                    "type": "array",
                    "description": "The tool calls to invoke",
                    "items": {
                        "types": "object",
                        "properties": {
                            "name": {
                                "types": "string",
                                "description": "The name of the tool to invoke",
                            },
                            "arguments": {
                                "types": "string",
                                "description": "The arguments to the tool, encoded as a JSON string",
                            },
                        },
                    },
                }
            },
        }
    }
    ```
    (Note: This is not the entire JSON spec, please refer to the `batch_tool_schema` in the [001_tools.ipynb](./notebooks/4-tool-use/001_tools.ipynb) notebook.)

Next we need to define the tool:

```python
def run_batch(tool_input):
    batch_output = []
    for invocation in tool_input["invocations"]:
        tool_name = invocation["name"]
        # arguments (as mentioned in the batch JSON spec) is a JSON encoded string
        # so we need to convert the json string to json:
        args = json.loads(invocation["arguments"])

        tool_output = run_tool(tool_name, args)
        batch_output.append({"tool_name": tool_name, "output": tool_output})
    return batch_output
```

And need to make sure that in our `run_tool` function, we call the above function:

```python
def run_tool(tool_name, tool_input):
    # TODO: tutorial says to hard-code but there must be a better way
    if tool_name == "get_current_datetime":
        # we use the ** in the input because it is a dictionary input
        return get_current_datetime(**tool_input)
    # multiple other elifs ... 
    elif tool_name == "batch_tool":
        # notice how we don't add the splat (**) because we want to pass it as a dictionary
        return run_batch(tool_input)
    else:
        raise Exception(f"Unknown tool name: {tool_name}")
```

### Claude Sonnet 3.7 (Again with Batch Tool)

Now when we run this again, we can see that Claude has correctly called the batch tools with the two tool calls in one go:

```json
[{"role": "user",
  "content": [{"text": "What is March 12th, 2025 + 50 days? Also, what is March 12th, 2025 + 100 days?"}]},
 {"role": "assistant",
  "content": [{"text": "I'll calculate the dates that are 50 and 100 days after March 12th, 2025 for you."},
   {"toolUse": {"toolUseId": "tooluse_L6ZM9CvLRoW0M-_PkCYhZw",
     "name": "batch_tool",
     "input": {
        "invocations": [
            {
                "name": "add_duration_to_datetime",
                "arguments": "{'datetime_str': '2025-03-12', 'duration': 50, 'unit': 'days', 'input_format': '%Y-%m-%d'}"
            },
            {
                "name": "add_duration_to_datetime",
                "arguments": "{'datetime_str': '2025-03-12', 'duration': 100, 'unit': 'days', 'input_format': '%Y-%m-%d'}"
            }
        ]
    }}}]},
 {"role": "user",
  "content": [
    {
        "toolResult": {
            "toolUseId": "tooluse_L6ZM9CvLRoW0M-_PkCYhZw",
            "content": [
                {"text": "[{'tool_name': 'add_duration_to_datetime', 'output': 'Thursday, May 01, 2025 12:00:00 AM'}, {'tool_name': 'add_duration_to_datetime', 'output': 'Friday, June 20, 2025 12:00:00 AM'}]"}
            ],
     "status": "success"}
     }]
 },
 {"role": "assistant",
  "content": [{"text": "Here are the results:\n\n- March 12th, 2025 + 50 days = Thursday, May 1st, 2025\n- March 12th, 2025 + 100 days = Friday, June 20th, 2025"}]}]
```

## Structured Output With Tools

Initially we used message prefill & stop sequences to generate specific outputs (like code generation). However, we can ask Claude to use tools to provide more reliable output but at the **cost of complexity**. Depending upon the scenario, we may want to use the former rather than the later because of the setup & complexities.

### Approach

1. First we define an input JSON schema & force Claude to call the tool based on specific input parameters:
    ![Input JSON Schema for the Tool](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748558131%2F08_-_010_-_Structured_Data_with_Tools_02.1748558130925.png)
2. Next, we send our question to Claude along with the JSON schema.
3. Claude responds with the mandatory tool call with the extracted JSON (from the user query). 
4. The JSON input to the tool is in the format we require, so we take the JSON and don't need to respond back to Claude.

We usually prefer this approach if we specifically need Claude to return results in a JSON format.

### Key Benefits of Using a Tool for Structured Output

- More reliable than prompt-based extraction
- Guaranteed structure matching the required schema
- No need for message prefilling or stop sequences
- Built in validation through the tool schema

(Only trade-off is that we need to write a detailed schema and handle tool responses.)

## Flexible Tool for Structured Data Extraction

Here is a flexible tool schema, `to_json`, that we can use:

```json
{
    "toolSpec": {
        "name": "to_json",
        "description": "This tool processes any JSON data and can be used for generating structured content, transforming information, or creating any JSON-based output needed for your task.",
        "inputSchema": {
            "json": {"type": "object", "additionalProperties": true}
        },
    }
}
```

Therefore instead of defining the structure in the JSON schema, we can easily define it in the prompt as follows:

```python
add_user_message(messages, 
f"""
Analyze the article below and extract key data. Then call the to_json tool.

<article_text>
{result['text']}
</article_text>

When you call to_json, pass in the following structure:
{{
        "title": str # title of the article,
        "author": str # author of the article,
        "topics": List[str] # List of topics mentioned in the article,
        "num_topics": int # Number of topics mentioned
}}
""",)
```

Now when we can call Claude to force it to use the `to_json` tool and it will provide us with the required json format.

## Claude's Text Editor Tool

The text editor tool is directly built-into Claude.

This gives Claude the ability to:
- View file or directory contents
- View specific range of lines in a file
- Replace text in a file
- Create new files
- Insert text at specific lines in a file
- Undo recent edits to files


Only the json schema is built in, we must provide the implementation of the actual tool.

![Need to define only the function](./images/TextEditorToolRequirement.png)

### Understanding With An Example

Consider we want to read the contents of a file. Here is what the message exchange between Claude will look like:

![diagrammatic flow of what happened](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748558133%2F08_-_012_-_The_Text_Editor_Tool_12.1748558133215.png)

As we can see in Claude's tool use part, it sent:
```json
{
    "command": "view",
    "path": "./main_file.py"
}
```

### Commands

There are 5 commands which the text editor tool might send as a response to our application:

1. **"view":** View/ read the contents of a file or directory
2. **"str_replace":** Replace a specific string in a file with a new string
3. **"create":** Create a file with somme initial content
4. **"insert":** Insert text at a specific line number in a file
5. **"undo_edit":** Undo the last edit made to a file

We need to write out code for each of these specific cases.

#### Defining Commands

For each of the above commands, we must define a concrete function in the `TextEditorTool` class, and in our `run_tool` function, we must call the respective function as follows:

```python
text_editor_tool = TextEditorTool()

def run_tool(tool_name, tool_input):
    if tool_name == "str_replace_editor":
        command = tool_input.get("command", "")
        if command == "view":
            path = tool_input.get("path", "")
            view_range = tool_input.get("view_range", None)
            return text_editor_tool.view(path, view_range)
        elif command == "str_replace":
            path = tool_input.get("path", "")
            old_str = tool_input.get("old_str", "")
            new_str = tool_input.get("new_str", "")
            return text_editor_tool.str_replace(path, old_str, new_str)
        elif command == "create":
            # ...
        elif command == "insert":
            # ...
        elif command == "undo_edit":
            # ...
        else:
            raise Exception(f"Unknown text editor command: {command}")
    else:
        raise Exception(f"Unknown tool name: {tool_name}")
```

### Practical Application

The Text Editor Tool essentially turns Claude into a code assistant that can:

- Read existing code and provide analysis
- Create new files and functions
- Modify existing code
- Set up test files
- Refactor code across multiple files

The `calculate_pi` method in the [main_file.py](./notebooks/4-tool-use/main_file.py) & the [test_main_file.py](./notebooks/4-tool-use/test_main_file.py) has been generated by Claude.
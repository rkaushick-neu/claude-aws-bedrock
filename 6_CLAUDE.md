# 6. Claude Features

Jupyter Notebooks:
- [001_thinking.ipynb](./notebooks/6-claude-features/001_thinking.ipynb): Getting Claude to think before responding.
- [002_images.ipynb](./notebooks/6-claude-features/002_images.ipynb): Sending images through the API.
- [003_pdf.ipynb](./notebooks/6-claude-features/003_pdf.ipynb): Sending PDF documents through the API.

## Extended Thinking

Thinking allows Claude to reason with itself before generating it's response to the user. This can be used for complex problems that require a logical step by step approach to solve the problem.

Thinking can help Claude be **more intelligent** on harder problems, but it's **more expensive and causes more latency**.

```python
params = {
        "modelId": model_id,
        "messages": messages,
        # ... many other params ...
        "additionalModelRequestFields": {
            # ...
            "thinking": {
                "type": "enabled",
                "budget_tokens": 1024 # 1024 is the minimum number of tokens allowed for thinking
            }
        }
    }
response = client.converse(**params)
```

The response from Claude when thinking is enabled:

```json
[
    {
        'reasoningContent': {
            'reasoningText': {
                'text': 'I need to write a concise one-paragraph guide to recursion in computer science. I should:\n1. Define what recursion is clearly\n2. Explain the key components (base case and recursive case)\n3. Mention why it's useful\n4. Perhaps include a simple conceptual example\n5. Keep it to one cohesive paragraph\n\nI'll aim to make it accessible but informative, avoiding overly technical language while still being precise.',
                'signature': 'ErcBCkgIBxABGAIiQF3W5Yo2bMElMnzxHOqEdN32U0dWi9f4PAqGKx1Zm5bT4e+UH3eGoBQj...'
            }
        }
    },
    {
        'text': '# A Guide to Recursion\n\nRecursion is a powerful programming concept where a function solves a problem by calling itself with simpler versions of the original problem, continuing this process until reaching a "base case" that can be solved directly without further recursion ...'
    }
]

```

### When To Use Thinking?

When our evals are not performing well, we can decide to use extended thinking. The `thinking_budget` is dependant upon the complexity of each problem. For moderate complexity, we can begin with a thinking budget of 1024 tokens, but if it is more complex, we can increase it as per the use case.

When we decide to use extended thinking we receive the following two parts in Claude's response:
1. **Reasoning Content**: Claude's internal thinking process.
2. **Text**: Final response answering user's message.

We can also include Claude's previous thinking part if we want to ask a follow up question.

> [!NOTE]
> The most important takeaway about extended thinking is that the decision to use it must be data-driven. Only once we run evaluations and optimize prompts, we can consider 'extended thinking' if we still need a higher boost in accuracy for complex tasks.

### Thinking Signature

Each thinking part comes with a signature. This is because developers shouldn't change the thinking part as it could lead to safety issues. The signature makes sure that the thinking part is not tampered with. 

![Claude's thinking signature](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748559588%2F10_-_001_-_Extended_Thinking_04.1748559588322.png)

### Redacted Thinking Content

Sometimes Claude's thinking may get flagged by internal safety systems. If this happens, we would receive a `redactedContent` part instead of the thinking text.

![Redacted thinking](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748559589%2F10_-_001_-_Extended_Thinking_06.1748559588844.png)


Redacted Response:

```json
[
    {
        'reasoningContent': {
            'redactedContent': 'EoUGCkgIBxABGAIqQKbnB9k1Sul5rvhN+DuWUV6izV/LYzMnIrdmjw8LYSSdeIQfUmPDm93tHMQdP5kBAaKwWcEEnuoWAt61...'
        }
    },
    {
        'text': 'I notice that your message contains what appears to be an attempt to manipulate my internal processing with some kind of "magic string" or trigger. I can\'t respond to commands that try to alter how my systems work.\n\nIf you have a genuine question or topic you\'d like to discuss, I\'d be happy to help you with that instead. Please feel free to share what you\'re actually interested in talking about, and I\'ll do my best to assist you.'
    }
]
```

## Image Support

### Image Limitations

![Image handling & limitations](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748559593%2F10_-_002_-_Image_Support_01.1748559593554.png)

### Prompting Techniques

We must use the same prompting techniques even when working with Claude such as by:
- giving clear instructions or steps to follow
- 1-shot or multi-shot prompting

![Step by step instructions with images](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748559595%2F10_-_002_-_Image_Support_05.1748559595686.png)

## PDF Support

PDF documents can be sent through the API (similar to images). 

First we need to read the PDF file in bytes:

```python
with open("./earth.pdf", "rb") as f:
    file_bytes = f.read()
```

Finally before sending the request to Claude, we would add the document into the user message as follows:

```python
add_user_message(
    messages,
    [
        {   
            "document": {
                "format": "pdf", 
                "name": "earth", # name of the doc without the extension
                "source": {"bytes": file_bytes},
            }
        },
        {"text": prompt},
    ],
)
```

### Claude's PDF Capabilities

- Extract & summarize key information
- Answer specific questions about document content
- Analyze document structure & formatting
- Process multi-page documents efficiently
- Work with PDFs containing text & images


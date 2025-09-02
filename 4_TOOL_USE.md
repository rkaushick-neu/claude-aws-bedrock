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

### Tools We Need

1. Get the current date-time
2. Add duration to data-time
3. Set a reminder


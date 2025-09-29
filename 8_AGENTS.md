# 8. Agents

## Claude Code

Capabilities:
- search, read, edit files
- access to terminal to run commands
- web search access
- support for MCP (built in MCP client)

Claude code can do more than just write code:

![claude code's abilities](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748559793%2F12_-_003_-_Claude_Code_in_Action_01.1748559793800.png)

### Installing Claude Code

1. Install NodeJS at
    ```
    nodejs.org/en/download
    ```
2. Install Claude Code from terminal:
   ```bash
    npm install -g @anthropic-ai/claude-code
    ```
3. Configure Claude Code to use Bedrock
   ```bash
   export ANTHROPIC_MODEL='us.anthropic.claude-3-7-sonnet-20250219-v1:0'
   export ANTHROPIC_SMALL_FAST_MODEL='us.anthropic.claude-3-5-haiku-20241022-v1:0'
   export CLAUDE_CODE_USE_BEDROCK=1
   export AWS_ACCESS_KEY_ID='<your-aws-access-key>'
   export AWS_SECRET_ACCESS_KEY='<your-aws-secret-access-key>'
   ```
4. Run it on the terminal by just running the command:
    ```bash
    claude
    ```

#### Project To Work With Claude Code

The [claude-code-agent-project/app_starter](./claude-code-agent-project/app_starter/) is a sample project to get started using Claude Code.

### /init

This should be the first command in to get Claude Code to understand our repository. The `/init` command get's Claude to:
- scan the codebase
- understand project structure
- understand the dependencies
- understand coding style/ patterns

It stores all of this in a **CLAUDE.md** file. Subsequent calls to Claude Code uses this file as context to answer questions or make changes.

We can also include special directions with `/init` (optionally):
```
/init Include detailed notes on defining MCP tools from the README file
```

There can be multiple **CLAUDE.md** files for different scopes:
- **Project scope:** added into git & shared between engineers
- **Local scope:** not added in git, developer specific notes to Claude
- **User scope:** (not added in git), used across all the projects for a user

### Other commands
- `/login`: Login to Claude Code (if you are signing into a paid Claude subscription/ using API)
- `/status`: Check the details of where Claude is running (like if it is using Bedrock, AWS region, Model, ...)
- `/clear`: Clears the conversation and the context history for new fresh requests
- `/exit`: Exit from the Claude 
- and many more ...

### Claude Code Workflows:

Claude works best when we provide it the right context, ask it to plan out it's approach and then finally ask it to implement the plan:
![Workflows](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748559794%2F12_-_003_-_Claude_Code_in_Action_11.1748559794657.png)

Another good practice is to ask Claude to follow **Test Driven Development (TDD)** wherein, we would ask Claude to think about the test cases first, implement test cases and then only later implement the code that passes the tests.
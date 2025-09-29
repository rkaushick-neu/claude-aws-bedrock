# 7. Model Context Protocol (MCP)

MCP is a communication layer that provides Claude (and now other LLMs like ChatGPT) context and tools without the need of to author tool integrations ourselves. Instead, MCP shifts the burden of defining integrations to outside 3rd party services though specialized MCP servers.

## MCP Architecture

![MCP Architecture](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748559635%2F11_-_001_-_Introducing_MCP_01.1748559635516.png)

## Problem That MCP Solves

If we want to provide tools to our LLM for interfacing with GitHub, we would need to author a whole lot of different tools for different functionality. This is tedious to develop, test and very hard to maintain.

![Tools required to interface with GitHub](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748559636%2F11_-_001_-_Introducing_MCP_05.1748559636704.png)

However, instead of writing all the tools ourselves, we can connect to the official GitHub MCP server & directly use those defined tools. This shifts the burden of development, testing and maintenance from the developers to the 3rd party providers.

## Common Questions

![FAQs](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748559638%2F11_-_001_-_Introducing_MCP_12.1748559637997.png)

> [!IMPORTANT]
> MCP ≠ Tool Use.
> MCP & tool use go hand in hand. MCP allows us to use tool functions already defined by others in dedicated MCP servers.


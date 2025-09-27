# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Document Tools package that provides various document-related tools for converting and processing document formats. The tools are exposed through an MCP (Model Control Protocol) server interface for seamless integration with AI assistants.

## Code Architecture

- `main.py`: Entry point that initializes and runs the MCP server
- `tools/`: Directory containing the tool implementations:
  - `document.py`: Tools for document conversion and processing
  - `math.py`: Sample mathematical tools
- `tests/`: Directory containing test files and fixtures

The project uses the MCP framework to define and expose tools as API endpoints. Each tool is a Python function registered with the MCP server using the `mcp.tool()` decorator.

## Development Commands

### Setup

```bash
# Create a virtual environment and activate it
uv venv
source .venv/bin/activate

# Install the package in development mode
uv pip install -e .
```

### Running the Server

```bash
# Start the MCP server
uv run main.py
```

### Testing

```bash
# Run all tests
uv run pytest

# Run a specific test file
uv run pytest tests/test_document.py

# Run a specific test function
uv run pytest tests/test_document.py::TestBinaryDocumentToMarkdown::test_binary_document_to_markdown_with_docx
```

## Tool Definition Guidelines

When defining new tools for the MCP server:

1. **Tool Registration**: Tools are registered with the MCP server using the decorator pattern:
   ```python
   mcp.tool()(my_function)
   ```

2. **Tool Documentation**: Tool descriptions should:
   - Begin with a one-line summary
   - Provide detailed explanation of functionality
   - Explain when to use (and not use) the tool
   - Include usage examples with expected input/output

3. **Parameter Definitions**: Use `Field` from pydantic for parameter descriptions:
   ```python
   from pydantic import Field

   def my_tool(
       param1: str = Field(description="Detailed description of this parameter"),
       param2: int = Field(description="Explain what this parameter does")
   ) -> ReturnType:
       """Comprehensive docstring here"""
       # Implementation
   ```

4. **Example Tool Structure**:
   ```python
   def tool_name(
       param1: type = Field(description="Parameter description"),
       param2: type = Field(description="Parameter description")
   ) -> return_type:
       """One-line summary of the tool's purpose.

       Detailed explanation of functionality and behavior.

       When to use:
       - Scenario 1
       - Scenario 2

       Examples:
       >>> tool_name(value1, value2)
       expected_output
       """
       # Implementation
   ```

5. **Tool Registration in main.py**:
   ```python
   from mcp.server.fastmcp import FastMCP
   from tools.your_module import your_tool

   mcp = FastMCP("docs")
   mcp.tool()(your_tool)
   ```

## Best Practices

1. Always write comprehensive docstrings for tools following the example in `math.py`
2. Include appropriate test cases in the tests directory for new tools
3. Tools should have clearly defined input parameters and return types
4. Use the `Field` class from pydantic to provide detailed parameter descriptions
5. Always apply appropriate types to funciton args
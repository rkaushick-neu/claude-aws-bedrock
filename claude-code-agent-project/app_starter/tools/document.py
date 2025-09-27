from markitdown import MarkItDown, StreamInfo
from io import BytesIO
import os
from typing import Optional
from pydantic import Field


def binary_document_to_markdown(binary_data: bytes, file_type: str) -> str:
    """Converts binary document data to markdown-formatted text."""
    md = MarkItDown()
    file_obj = BytesIO(binary_data)
    stream_info = StreamInfo(extension=file_type)
    result = md.convert(file_obj, stream_info=stream_info)
    return result.text_content


def document_path_to_markdown(
    file_path: str = Field(description="Path to the PDF or DOCX document to convert"),
    file_type: Optional[str] = Field(None, description="Optional file type override (pdf or docx). If not provided, will be determined from file extension")
) -> str:
    """Convert a PDF or DOCX document to markdown format.

    This tool takes a file path to a document, reads it, and converts its contents
    to markdown format. Supports PDF and DOCX file formats.

    When to use:
    - When you need to extract text content from PDF or DOCX documents
    - When you need to process document content in a markdown-compatible format

    Examples:
    >>> document_path_to_markdown("path/to/document.pdf")
    "# Document Title\n\nDocument content in markdown format..."
    >>> document_path_to_markdown("path/to/document.docx")
    "# Document Title\n\nDocument content in markdown format..."
    """
    # Validate that file exists
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    # Determine file type if not provided
    # Handle both None and Field object cases
    if hasattr(file_type, 'default'):
        # If it's a Field object, extract the default value
        ft = file_type.default
    else:
        # Otherwise use the provided value
        ft = file_type

    if ft is None:
        # Extract extension from the file path
        ft = os.path.splitext(file_path)[1].lower().lstrip('.')

    # Validate file type
    if ft not in ['pdf', 'docx']:
        raise ValueError(f"Unsupported file type: {ft}. Supported types are 'pdf' and 'docx'.")

    # Read binary data from file
    try:
        with open(file_path, 'rb') as f:
            binary_data = f.read()
    except Exception as e:
        raise IOError(f"Error reading file: {str(e)}")

    # Convert using existing function
    return binary_document_to_markdown(binary_data, ft)

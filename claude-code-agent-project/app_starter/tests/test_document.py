import os
import pytest
from tools.document import binary_document_to_markdown, document_path_to_markdown


class TestBinaryDocumentToMarkdown:
    # Define fixture paths
    FIXTURES_DIR = os.path.join(os.path.dirname(__file__), "fixtures")
    DOCX_FIXTURE = os.path.join(FIXTURES_DIR, "mcp_docs.docx")
    PDF_FIXTURE = os.path.join(FIXTURES_DIR, "mcp_docs.pdf")

    def test_fixture_files_exist(self):
        """Verify test fixtures exist."""
        assert os.path.exists(self.DOCX_FIXTURE), (
            f"DOCX fixture not found at {self.DOCX_FIXTURE}"
        )
        assert os.path.exists(self.PDF_FIXTURE), (
            f"PDF fixture not found at {self.PDF_FIXTURE}"
        )

    def test_binary_document_to_markdown_with_docx(self):
        """Test converting a DOCX document to markdown."""
        # Read binary content from the fixture
        with open(self.DOCX_FIXTURE, "rb") as f:
            docx_data = f.read()

        # Call function
        result = binary_document_to_markdown(docx_data, "docx")

        # Basic assertions to check the conversion was successful
        assert isinstance(result, str)
        assert len(result) > 0
        # Check for typical markdown formatting - this will depend on your actual test file
        assert "#" in result or "-" in result or "*" in result

    def test_binary_document_to_markdown_with_pdf(self):
        """Test converting a PDF document to markdown."""
        # Read binary content from the fixture
        with open(self.PDF_FIXTURE, "rb") as f:
            pdf_data = f.read()

        # Call function
        result = binary_document_to_markdown(pdf_data, "pdf")

        # Basic assertions to check the conversion was successful
        assert isinstance(result, str)
        assert len(result) > 0
        # Check for typical markdown formatting - this will depend on your actual test file
        assert "#" in result or "-" in result or "*" in result


class TestDocumentPathToMarkdown:
    # Define fixture paths
    FIXTURES_DIR = os.path.join(os.path.dirname(__file__), "fixtures")
    DOCX_FIXTURE = os.path.join(FIXTURES_DIR, "mcp_docs.docx")
    PDF_FIXTURE = os.path.join(FIXTURES_DIR, "mcp_docs.pdf")
    NONEXISTENT_FILE = os.path.join(FIXTURES_DIR, "nonexistent.pdf")
    INVALID_TYPE_FILE = os.path.join(FIXTURES_DIR, "mcp_docs.txt")

    def test_fixture_files_exist(self):
        """Verify test fixtures exist."""
        assert os.path.exists(self.DOCX_FIXTURE), (
            f"DOCX fixture not found at {self.DOCX_FIXTURE}"
        )
        assert os.path.exists(self.PDF_FIXTURE), (
            f"PDF fixture not found at {self.PDF_FIXTURE}"
        )

    def test_document_path_to_markdown_with_pdf(self):
        """Test converting a PDF file path to markdown."""
        # Call function
        result = document_path_to_markdown(self.PDF_FIXTURE)

        # Basic assertions to check the conversion was successful
        assert isinstance(result, str)
        assert len(result) > 0
        # Check for typical markdown formatting
        assert "#" in result or "-" in result or "*" in result

    def test_document_path_to_markdown_with_docx(self):
        """Test converting a DOCX file path to markdown."""
        # Call function
        result = document_path_to_markdown(self.DOCX_FIXTURE)

        # Basic assertions to check the conversion was successful
        assert isinstance(result, str)
        assert len(result) > 0
        # Check for typical markdown formatting
        assert "#" in result or "-" in result or "*" in result

    def test_document_path_to_markdown_with_explicit_type(self):
        """Test with explicit file_type override."""
        # Call function with explicit file type
        result = document_path_to_markdown(self.PDF_FIXTURE, file_type="pdf")

        # Basic assertions to check the conversion was successful
        assert isinstance(result, str)
        assert len(result) > 0

    def test_document_path_to_markdown_file_not_found(self):
        """Test with non-existent file path."""
        # Should raise FileNotFoundError
        with pytest.raises(FileNotFoundError):
            document_path_to_markdown(self.NONEXISTENT_FILE)

    def test_document_path_to_markdown_invalid_type(self):
        """Test with unsupported file type."""
        # Create a temporary text file for testing
        with open(self.INVALID_TYPE_FILE, "w") as f:
            f.write("This is a test file.")

        try:
            # Should raise ValueError for unsupported file type
            with pytest.raises(ValueError):
                document_path_to_markdown(self.INVALID_TYPE_FILE)
        finally:
            # Clean up the temporary file
            if os.path.exists(self.INVALID_TYPE_FILE):
                os.remove(self.INVALID_TYPE_FILE)
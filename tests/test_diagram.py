import pytest
from agent_arena.diagram import extract_mermaid_code


class TestExtractMermaidCode:
    def test_extracts_from_code_block(self):
        text = """Here is the diagram:

```mermaid
flowchart TD
    A[User] --> B[API]
    B --> C[(Database)]
```

Done."""
        result = extract_mermaid_code(text)
        assert result.startswith("flowchart TD")
        assert "A[User]" in result

    def test_raw_flowchart(self):
        text = "flowchart TD\n    A --> B"
        result = extract_mermaid_code(text)
        assert result == text

    def test_raw_graph(self):
        text = "graph LR\n    A --> B"
        result = extract_mermaid_code(text)
        assert result == text

    def test_strips_whitespace(self):
        text = "  flowchart TD\n    A --> B  "
        result = extract_mermaid_code(text)
        assert result == "flowchart TD\n    A --> B"

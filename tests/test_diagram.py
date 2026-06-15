from agent_arena.diagram import extract_d2_code


class TestExtractD2Code:
    def test_extracts_from_d2_code_block(self):
        text = """Sure, here is the D2:

```d2
direction: right
user: User {shape: person}
user -> api
```

Done."""
        result = extract_d2_code(text)
        assert result.startswith("direction: right")
        assert "user -> api" in result

    def test_falls_back_to_mermaid_block_if_llm_misbehaves(self):
        text = "```mermaid\nflowchart TD\n  A --> B\n```"
        result = extract_d2_code(text)
        assert "A --> B" in result

    def test_strips_whitespace(self):
        text = "  direction: right\n  a -> b  "
        result = extract_d2_code(text)
        assert result.startswith("direction: right")

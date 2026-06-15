from agent_arena.specialists import (
    SpecialistReport, SpecialistFinding,
    render_specialist_block_for_final, render_specialist_section_for_report,
)


def _sample():
    return [
        SpecialistReport(
            agent="security",
            overall_concern="Secrets stored as plain env vars across the 3 proposals.",
            findings=[
                SpecialistFinding(
                    severity="high", topic="Plain-text secrets",
                    applies_to=["azure", "aws", "gcp"],
                    issue="OpenAI keys mounted as env vars",
                    recommendation="Use Key Vault / Secrets Manager / Secret Manager",
                ),
            ],
        ),
        SpecialistReport(agent="finops", overall_concern="No 3-year TCO", findings=[]),
    ]


def test_block_for_final_contains_severity_and_recommendation():
    block = render_specialist_block_for_final(_sample())
    assert "SECURITY" in block
    assert "[HIGH]" in block
    assert "Key Vault" in block


def test_report_section_renders_icons_and_scope():
    md = render_specialist_section_for_report(_sample())
    assert "🛡️ Seguridad" in md
    assert "🔴" in md
    assert "AZURE/AWS/GCP" in md
    assert "Sin hallazgos materiales." in md  # finops has no findings


def test_empty_inputs_produce_empty_outputs():
    assert render_specialist_block_for_final([]) == ""
    assert render_specialist_section_for_report([]) == ""

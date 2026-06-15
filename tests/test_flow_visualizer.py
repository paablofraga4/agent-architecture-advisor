from agent_arena.flow_visualizer import FlowState, PIPELINE_NODES


def test_initial_state_all_pending():
    s = FlowState()
    assert all(v == "pending" for v in s.nodes.values())
    assert len(s.nodes) == len(PIPELINE_NODES)


def test_event_transitions():
    s = FlowState()
    assert s.apply_event("planner_started") is True
    assert s.nodes["planner"] == "running"
    assert s.apply_event("planner_finished") is True
    assert s.nodes["planner"] == "done"
    # Idempotent
    assert s.apply_event("planner_finished") is False


def test_error_marks_running_nodes_error():
    s = FlowState()
    s.apply_event("azure_agent_started")
    s.apply_event("aws_agent_started")
    s.apply_event("error")
    assert s.nodes["azure"] == "error"
    assert s.nodes["aws"] == "error"
    assert s.nodes["planner"] == "pending"


def test_render_contains_mermaid_and_class_assignments():
    s = FlowState()
    s.apply_event("planner_started")
    s.apply_event("retrieval_finished")
    msg = s.render_message()
    assert "```mermaid" in msg
    assert "flowchart LR" in msg
    assert "class planner running" in msg
    assert "class retrieval done" in msg

from app.brain import BrainManager, BrainConfig, BrainTask, BrainEvent, BrainState


def test_brain_manager_orchestrates_import_and_search():
    manager = BrainManager()
    task = BrainTask(task_id="import-1", kind="import", payload={"path": "docs"})
    manager.enqueue(task)
    manager.process_pending()

    assert manager.state.last_event is not None
    assert manager.state.tasks_completed >= 1


def test_brain_state_and_events_work():
    state = BrainState()
    event = BrainEvent(name="indexed", payload={"count": 3})
    state.apply(event)

    assert state.last_event.name == "indexed"
    assert state.session_id


def test_brain_config_defaults():
    config = BrainConfig()
    assert config.namespace == "ai-librarian"

"""
Unit Test Suite for Task Scheduler Module
Governing Authority: Governing Officer Tarwater
"""

import pytest
from task_scheduler import TaskScheduler


def test_scheduler_initialization():
    scheduler = TaskScheduler()
    assert scheduler.tasks == []


def test_add_valid_task():
    scheduler = TaskScheduler()
    task = scheduler.add_task("Deploy Governance Engine", priority=5)
    
    assert task["id"] == 1
    assert task["name"] == "Deploy Governance Engine"
    assert task["priority"] == 5
    assert task["status"] == "PENDING"
    assert len(scheduler.tasks) == 1


def test_add_invalid_task_raises_error():
    scheduler = TaskScheduler()
    with pytest.raises(ValueError):
        scheduler.add_task("")
    with pytest.raises(ValueError):
        scheduler.add_task(None) # type: ignore


def test_process_tasks():
    scheduler = TaskScheduler()
    scheduler.add_task("Low Priority Task", priority=1)
    scheduler.add_task("High Priority Task", priority=10)

    processed = scheduler.process_tasks()
    
    assert len(processed) == 2
    # High priority should process first
    assert processed[0]["name"] == "High Priority Task"
    assert processed[0]["status"] == "COMPLETED"
    assert processed[1]["name"] == "Low Priority Task"

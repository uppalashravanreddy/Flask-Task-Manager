import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from forms import PRIORITY_RANK, PRIORITY_CHOICES


class FakeTask:
    def __init__(self, title, priority):
        self.title = title
        self.priority = priority


def test_priority_rank_high_sorts_first():
    tasks = [
        FakeTask('Task A', 'Low'),
        FakeTask('Task B', 'High'),
        FakeTask('Task C', 'Medium'),
    ]
    result = sorted(tasks, key=lambda t: PRIORITY_RANK.get(t.priority, 2))
    assert result[0].title == 'Task B'
    assert result[1].title == 'Task C'
    assert result[2].title == 'Task A'


def test_priority_rank_medium_sorts_between_high_and_low():
    tasks = [
        FakeTask('Low Task', 'Low'),
        FakeTask('Medium Task', 'Medium'),
        FakeTask('High Task', 'High'),
    ]
    result = sorted(tasks, key=lambda t: PRIORITY_RANK.get(t.priority, 2))
    assert result[0].priority == 'High'
    assert result[1].priority == 'Medium'
    assert result[2].priority == 'Low'


def test_unknown_priority_defaults_to_medium_position():
    tasks = [
        FakeTask('Unknown', 'Critical'),
        FakeTask('High Task', 'High'),
        FakeTask('Low Task', 'Low'),
    ]
    result = sorted(tasks, key=lambda t: PRIORITY_RANK.get(t.priority, 2))
    assert result[0].title == 'High Task'
    assert result[1].title == 'Unknown'
    assert result[2].title == 'Low Task'


def test_priority_choices_contain_all_three_values():
    values = [choice[0] for choice in PRIORITY_CHOICES]
    assert 'High' in values
    assert 'Medium' in values
    assert 'Low' in values


def test_priority_choices_has_no_extra_values():
    assert len(PRIORITY_CHOICES) == 3


def test_priority_rank_keys_match_choices():
    choice_values = {choice[0] for choice in PRIORITY_CHOICES}
    rank_keys = set(PRIORITY_RANK.keys())
    assert choice_values == rank_keys

import pytest
from src.app import activities
import copy

@pytest.fixture(autouse=True)
def reset_activities():
    # Save a deep copy of the original activities
    original = copy.deepcopy(activities)
    yield
    # Restore the original activities after each test
    activities.clear()
    activities.update(copy.deepcopy(original))

import pytest
from src.swarm_sim.intent import SurveyIntent, validate_intent

def test_valid_intent():
    validate_intent(SurveyIntent())

def test_rejects_non_survey():
    with pytest.raises(ValueError):
        validate_intent(SurveyIntent(objective="ATTACK"))

def test_rejects_bad_coverage():
    with pytest.raises(ValueError):
        validate_intent(SurveyIntent(required_coverage=1.5))

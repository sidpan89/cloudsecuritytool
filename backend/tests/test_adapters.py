import json
from adapters.prowler import ProwlerAdapter
from adapters.trivy import TrivyAdapter
from adapters.checkov import CheckovAdapter
from adapters.falco import FalcoAdapter


def load_fixture(path: str):
    with open(path) as f:
        return json.load(f)


def test_prowler_adapter():
    payload = load_fixture('fixtures/prowler/sample.json')
    adapter = ProwlerAdapter()
    parsed = adapter.parse(payload)
    assert len(parsed) == 1
    norm = adapter.normalize(parsed[0])
    assert norm['tool'] == 'prowler'


def test_trivy_adapter():
    payload = load_fixture('fixtures/trivy/sample.json')
    adapter = TrivyAdapter()
    parsed = adapter.parse(payload)
    assert parsed[0]['Target'] == 'demo-image:latest'
    norm = adapter.normalize(parsed[0])
    assert norm['severity'] == 'medium'


def test_checkov_adapter():
    payload = load_fixture('fixtures/checkov/sample.json')
    adapter = CheckovAdapter()
    parsed = adapter.parse(payload)
    assert parsed[0]['check_id'] == 'CKV_AWS_1'
    norm = adapter.normalize(parsed[0])
    assert norm['category'] == 'iac'


def test_falco_adapter():
    payload = load_fixture('fixtures/falco/sample.json')
    adapter = FalcoAdapter()
    parsed = adapter.parse(payload)
    assert len(parsed) == 1
    norm = adapter.normalize(parsed[0])
    assert norm['event_type'] == 'process'

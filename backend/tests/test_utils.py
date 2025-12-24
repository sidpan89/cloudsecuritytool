from backend.app.services.utils import normalize_resource_id


def test_normalize_aws_arn():
    arn = 'arn:aws:s3:::demo-bucket'
    assert normalize_resource_id(arn) == arn


def test_normalize_gcp():
    rid = '//cloudresourcemanager.googleapis.com/projects/demo'
    assert normalize_resource_id(rid) == rid


def test_normalize_default():
    rid = ' Custom Resource '
    assert normalize_resource_id(rid) == 'customresource'

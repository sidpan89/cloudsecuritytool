import re

def normalize_resource_id(identifier: str) -> str:
    if identifier.startswith('arn:'):
        return identifier
    if identifier.startswith('k8s://'):
        return identifier
    if identifier.startswith('iac://'):
        return identifier
    if identifier.startswith('//cloudresourcemanager.googleapis.com'):
        return identifier
    if identifier.startswith('/') and '/providers/' in identifier:
        return identifier
    if identifier.startswith('docker://'):
        return identifier
    # Default: compress whitespace and lowercase
    normalized = re.sub(r'\s+', '', identifier).lower()
    return normalized

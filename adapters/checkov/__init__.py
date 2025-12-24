from adapters.base import Adapter


class CheckovAdapter(Adapter):
    tool = 'checkov'

    def parse(self, payload: dict) -> list[dict]:
        return payload.get('results', {}).get('failed_checks', [])

    def normalize(self, record: dict) -> dict:
        return {
            'tool': self.tool,
            'title': record.get('check_name'),
            'severity': str(record.get('severity', '')).lower(),
            'service': 'iac',
            'canonical_resource_id': f"iac://repo/{record.get('file_path')}#{record.get('resource')}",
            'category': 'iac'
        }

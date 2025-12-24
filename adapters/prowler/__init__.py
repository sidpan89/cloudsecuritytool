from adapters.base import Adapter


class ProwlerAdapter(Adapter):
    tool = 'prowler'

    def parse(self, payload: dict) -> list[dict]:
        return payload.get('Findings', [])

    def normalize(self, record: dict) -> dict:
        return {
            'tool': self.tool,
            'title': record.get('Title'),
            'severity': record.get('Severity', '').lower(),
            'service': record.get('Service'),
            'canonical_resource_id': record.get('ResourceId'),
            'category': record.get('Category'),
        }

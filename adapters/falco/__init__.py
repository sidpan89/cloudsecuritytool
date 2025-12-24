from adapters.base import Adapter


class FalcoAdapter(Adapter):
    tool = 'falco'

    def parse(self, payload: dict) -> list[dict]:
        return [payload]

    def normalize(self, record: dict) -> dict:
        return {
            'tool': self.tool,
            'severity': record.get('severity', 'info'),
            'message': record.get('message', ''),
            'event_type': record.get('event_type', 'runtime'),
            'canonical_resource_id': record.get('resource'),
        }

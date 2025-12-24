from adapters.base import Adapter


class TrivyAdapter(Adapter):
    tool = 'trivy'

    def parse(self, payload: dict) -> list[dict]:
        records = []
        for result in payload.get('Results', []):
            for vuln in result.get('Vulnerabilities', []) or []:
                entry = vuln.copy()
                entry['Target'] = result.get('Target')
                records.append(entry)
        return records

    def normalize(self, record: dict) -> dict:
        return {
            'tool': self.tool,
            'title': record.get('Title') or record.get('VulnerabilityID'),
            'severity': str(record.get('Severity', '')).lower(),
            'service': 'container',
            'canonical_resource_id': f"docker://{record.get('Target')}",
            'category': 'cwpp'
        }

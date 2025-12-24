from adapters.prowler import ProwlerAdapter
from adapters.trivy import TrivyAdapter
from adapters.checkov import CheckovAdapter
from adapters.falco import FalcoAdapter

ADAPTERS = {
    'prowler': ProwlerAdapter(),
    'trivy': TrivyAdapter(),
    'checkov': CheckovAdapter(),
    'falco': FalcoAdapter(),
}

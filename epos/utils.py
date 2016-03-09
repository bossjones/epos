import requests
from toolz import curry
from functools import wraps


@curry
def http_endpoint(host, resource, method=requests.get, **params):
    endpoint = 'http://{host}/{resource}'.format(host=host,
                                                 resource=resource.lstrip('/'))
    # headers = {'Content-Type': 'application/json'}

    @wraps(method)
    def wrapper(payload={}, **params):
        url = endpoint.format(**params)
        response = method(url, json=payload, allow_redirects=True)
        response.raise_for_status()
        return response.json() if not response.status_code == 204 else response

    return wrapper

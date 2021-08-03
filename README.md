# jelastic-client

A Jelastic API python library.

# Installation

```bash
pip3 install jelastic-client --extra-index-url https://__token__:<your_personal_token>@gitlab.hidora.com/api/v4/projects/185/packages/pypi/simple
```

The gitlab access token needs to have `read_api` scope.

# Usage

```python
import jelastic_client

api_url = "https://[hoster-api-host]/1.0/"
api_token = "your-private-access-token"

factory = jelastic_client.JelasticClientFactory(api_url, api_token)
jps_client = factory.create_jps_client()
jps_client.install()
```
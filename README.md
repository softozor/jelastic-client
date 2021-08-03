# jelastic-client

A Jelastic API python library.

# Installation

```bash
pip3 install jelastic-client --no-deps --index-url https://<personal_access_token_name>:<personal_access_token>@gitlab.hidora.com/api/v4/projects/185/packages/pypi/simple
```

The gitlab access token needs to have `read_api` scope.

# Usage

```python
import jelastic_client

jelastic_client.settings.api_url = "https://[hoster-api-host]/1.0/"
jelastic_client.settings.api_token = "your-private-access-token"

jps_client = jelastic_client.JpsClient()
jps_client.install()
```
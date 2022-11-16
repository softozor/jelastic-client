[![Build Status](https://jelasticozor-teamcity.sh1.hidora.com/app/rest/builds/buildType:(id:SharedLibraries_JelasticClient_Integration)/statusIcon)](https://jelasticozor-teamcity.sh1.hidora.com/viewType.html?buildTypeId=SharedLibraries_JelasticClient_Integration&guest=1)


# jelastic-client

A Jelastic API python library.

# Installation

```bash
pip3 install jelastic-client
```

# Usage

At the root of this repository, you can run

```python
import jelastic_client

api_url = "https://[hoster-api-host]/1.0/"
api_token = "your-private-access-token"

factory = jelastic_client.JelasticClientFactory(api_url, api_token)
jps_client = factory.create_jps_client()
env_name = "my-jelastic-client-test"
jps_client.install_from_file("./test/data/valid_manifest.jps", env_name)
control_client = factory.create_control_client()
env_info = control_client.get_env_info(env_name)
assert env_info.is_running() is True
```

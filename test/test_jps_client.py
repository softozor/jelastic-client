from jelastic_client import JpsClient


def test_something(jps_client: JpsClient):
    jps_client.install()
    assert True is True

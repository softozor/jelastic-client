import random
import string

from jelastic_client import ControlClient


def get_manifest_data(success_text):
    if not success_text:
        return {}

    manifest_data = {}
    for key_value in success_text.split("<br />\n"):
        split_item = key_value.split(":")
        key = split_item[0]
        value = split_item[1]
        # to make it more flexible we could use re.sub
        # and try to extract code contained within optional
        # html tags
        key = key.replace("<strong>", "")
        key = key.replace("</strong>", "")
        manifest_data[key] = value.strip()

    return manifest_data


def create_random_env_name(commit_sha: str, worker_id: str) -> str:
    env_id = "".join(random.choice(string.digits) for _ in range(7))
    return "-".join([commit_sha, worker_id, env_id])


def get_new_random_env_name(
    control_client: ControlClient, commit_sha: str, worker_id: str
) -> str:
    env_name = create_random_env_name(commit_sha, worker_id)
    while control_client.get_env_info(env_name).exists():
        env_name = create_random_env_name(commit_sha, worker_id)
    return env_name

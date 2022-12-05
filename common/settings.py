import os
from typing import List, Union

# Utils functions
ARRAY_ENV_SEPARATOR = os.getenv("ARRAY_ENV_SEPARATOR", " ")


def get_array_env(env_name: str) -> Union[str, List[str]]:
    env_value: Union[str, List[str]] = os.getenv(env_name, [])
    if isinstance(env_value, str):
        return env_value.split(ARRAY_ENV_SEPARATOR)
    return env_value

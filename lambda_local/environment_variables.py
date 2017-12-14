import json
import os


def set_environment_variables(json_file_path):
    """
    Read and set environment variables from a flat json file.

    Bear in mind that env vars set this way and later on read using
    `os.getenv` function will be strings since after all env vars are just
    that - plain strings.

    Json file example:
    ```
    {
        "FOO": "bar",
        "BAZ": true
    }
    ```

    :param json_file_path: path to flat json file
    :type json_file_path: str
    """
    if json_file_path:
        with open(json_file_path) as json_file:
            env_vars = json.loads(json_file.read())

            for env_name, env_value in env_vars.items():
                os.environ[str(env_name)] = str(env_value)

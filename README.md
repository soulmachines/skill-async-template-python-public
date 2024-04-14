# Async skill api python server example

[![GitHub license](https://img.shields.io/badge/license-Apache%202.0-blue)](./LICENSE)
[![Python Version](https://img.shields.io/badge/python-v3.9-blue)](https://www.python.org/)
[![FastAPI Version](https://img.shields.io/badge/fastAPI-v0.110.1-blue)](https://pypi.org/project/fastapi/)

This is an example implementation of a Skill using the Skills Async API.

The Skills Async API provides a way for developers to create more advanced conversation interactions with your Digital People, by allowing you to send and receive messages asynchronously.

This provides more flexibility than the REST-based skill API when you want to go beyond simple request-response interactions. Example applications can be streaming multiple messages in the same turn, or allowing the skill to send messages to the user proactively.

## Development environment setup

```sh
python -m venv .venv
source .venv/bin/activate

python -m pip install --upgrade pip
pip install -r requirements.txt
```

Once you are happy with the code in dev phase, you can freeze requirements for deployment, to do so you can run the following script:

```sh
./scripts/freeze_requirements.sh
```

### Testing your skill

The example server (implemented using FastAPI) can be launched with:

```sh
./scripts/run_app.py [ARGS]
# To see supported arguments run:
./scripts/run_app.py --help
```

- You can try making modifications and adding your custom code for handling the various API requests and messages in `src/api/handlers`.
- You can debug the app in vscode using the `app` debug configuration.

## Serve for use with Studio

Localtunnel may be used to generate a public web address for your locally-running Skill, allowing DDNA Studio to connect to your Skill from a live Digital Person.

Generate a URL with a personalized subdomain using the following command, and then use this URL to configure the endpoints in your Skill Definition.

```sh
npx localtunnel --port 5000 --subdomain your-unique-id
```

## Licensing

This repository is licensed under the Apache License, Version 2.0. See [LICENSE](./LICENSE) for the full license text.

## Issues

For any issues, please reach out to one of our Customer Success team members.

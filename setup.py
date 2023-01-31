from setuptools import setup

# Metadata goes in setup.cfg. These are here for GitHub's dependency graph.
setup(
    name="statesman-slack",
    install_requires=[
        "flask<3.0",
        "flask-dotenv",
        "flask-executor",
        "flask-inputs",
        "flask-limiter[redis]",
        "flask-redis",
        "flask-script",
        "flask-session",
        "jsonschema",
        "pika",
        "python-dotenv",
        "pyyaml",
        "redis",
        "requests",
        "sentry-sdk[flask]",
        "slacker",
        "uwsgi",
    ],
    extras_require={},
)

from setuptools import setup

# Metadata goes in setup.cfg. These are here for GitHub's dependency graph.
setup(
    name="statesman-slack",
    install_requires=[
        "flask",
        "flask-dotenv",
        "flask-session",
        "pyyaml",
        "uwsgi",
        "sentry-sdk[flask]==1.9.8",
        "python-dotenv",
        "flask-inputs",
        "jsonschema",
        "flask-redis",
        "slacker",
        "flask-script",
        "redis",
    ],
    extras_require={},
)

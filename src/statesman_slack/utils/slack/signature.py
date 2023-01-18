__author__ = "Paul Schifferer <paul@schifferers.net>"
"""
slack.py
- Slack utilities
"""


from flask import current_app
import subprocess, shlex
import json
import hmac, hashlib
import os
import logging
from slacker import Slacker
import requests
from statesman_slack import constants
from statesman_slack.common.exceptions import SignatureException


def verify_signature(signature:str, timestamp:str, request_body:str):
    current_app.logger.debug("signature: %s", signature)

    current_app.logger.debug("request_body: %s", request_body)
    our_sig = f'{constants.SLACK_SIGNATURE_VERSION}:{timestamp}:{request_body}'
    current_app.logger.debug("our_sig: %s", our_sig)

    key = os.environ[constants.SLACK_SIGNING_SECRET_ENV]
    current_app.logger.debug("key: %s", key)
    digest = hmac.new(key.encode('utf-8'),
                      our_sig.encode('utf-8'),
                      hashlib.sha256).hexdigest()
    current_app.logger.debug("digest: %s", digest)

    if f'{constants.SLACK_SIGNATURE_VERSION}={digest}' != signature:
        raise SignatureException('Signature failed validation')

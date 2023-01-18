__author__ = "Paul Schifferer <paul@schifferers.net>"
"""
action.py
- Action API
"""


import logging
from datetime import datetime
from flask import session, jsonify, request, current_app, Blueprint
from werkzeug.exceptions import Forbidden, BadRequest, NotFound
from statesman_slack import constants
from statesman_slack.controllers.interact import handle_action_request
from statesman_slack.models import constants as model_constants
from statesman_slack.blueprints.api import user_required, requires_auth
from statesman_slack.blueprints.api.exceptions import error_response
from statesman_slack.common.exceptions import SignatureException
from statesman_slack.utils.limiter import limiter


blueprint = Blueprint("interact", __name__, url_prefix="/interact")


@blueprint.route("/", methods=["POST"])
@limiter.limit("10/second")
def handle_interaction():
    current_app.logger.debug("POST /interact/: %s", request)

    try:
        # handle_ssl_check(request)
        return handle_action_request(request)
    except:
        current_app.logger.exception("Exception while processing interaction")
        response = {"response_type": "ephemeral", "text": "Sorry, that didn't work. Please try again."}

        return response, 200

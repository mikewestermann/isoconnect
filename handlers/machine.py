from flask import render_template, request, redirect, url_for, Blueprint

from models.settings import db
from models.card import Card
from models.user import User
from models.machine import Machine

from utils.redis_helper import create_csrf_token, validate_csrf

#Dieser Handler soll für die DB live Abfrage über einen getaktetene Worker erfolgen 

#machine_handlers = Blueprint("machine", __name__)

#@machine_handlers.route("/card/<card_id>/create-comment", methods=["POST"])
#def comment_create(topic_id):
    
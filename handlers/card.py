import hashlib
import uuid
import os
from flask import Flask, render_template, request, redirect, url_for, make_response, Blueprint


from models.card import Card
from models.user import User
from models.settings import db
from models.machine import Machine

from handlers.auth import auth_handlers

from utils.redis_helper import create_csrf_token, validate_csrf



card_handlers = Blueprint("card", __name__)

@card_handlers.route("/")
def index():
    # check if user is authenticated based on session_token
    session_token = request.cookies.get("session_token")
    user = db.query(User).filter_by(session_token=session_token).first()

    return render_template("card/index.html", user=user)

@card_handlers.route("/dashboard")
def dashboard():
    # check if user is authenticated based on session_token
    session_token = request.cookies.get("session_token")
    user = db.query(User).filter_by(session_token=session_token).first()

    # get cards
    cards = db.query(Card).filter_by(author=user).all()

    # statische Daten
    machines = db.query(Machine).all() #Verbindung zwischen machine und card db herstellen

    # worker für db live verbindung 
    # START test background tasks (TODO: delete this code later)
    #if os.getenv('REDIS_URL'):
     #   from tasks import get_random_num
      #  get_random_num()
    # END test background tasks

    return render_template("card/dashboard.html", user=user, cards=cards, machines=machines)


@card_handlers.route("/card_create", methods=["GET", "POST"])
def card_create():    
    # get current user (author)
    session_token = request.cookies.get("session_token")
    user = db.query(User).filter_by(session_token=session_token).first()
    


    # only logged in users can create a topic
    if not user:
        return redirect(url_for('auth.login'))

    if request.method == "GET":
        csrf_token = create_csrf_token(user.email_adresse)

        return render_template("card/card_create.html", user=user, csrf_token=csrf_token)

    elif request.method == "POST":
        csrf = request.form.get("csrf")

        print("CSRF-Email_adresse: "+ csrf)

        if validate_csrf(csrf, user.email_adresse):

            name = request.form.get("name")
            baujahr = request.form.get("baujahr")
            maschinennummer = request.form.get("maschinennummer")
            standort = request.form.get("standort")
                    
            # create a Card object
            card = Card.create( name=name, baujahr=baujahr, maschinennummer=maschinennummer, standort=standort, author=user)

            return redirect(url_for('card.dashboard'))
        else:
            return "CSRF token is not valid"


@card_handlers.route("/card/<card_id>", methods=["GET"])
def card_details(card_id):
    card = db.query(Card).get(int(card_id))  # get card from db by ID

    # get current user (author)
    session_token = request.cookies.get("session_token")
    user = db.query(User).filter_by(session_token=session_token).first()

    machine = db.query(Machine).filter_by(name=name).all() #Verbindung zwischen machine und card db herstellen


    return render_template("card/card_details.html", card=card, user=user, csrf_token=create_csrf_token(user.email_adresse), machine=machine)


@card_handlers.route("/card/<card_id>/edit", methods=["GET", "POST"])
def card_edit(card_id):
    card = db.query(Card).get(int(card_id))  # get card from db by ID

    if request.method == "GET":
        return render_template("card/card_edit.html", card=card)

    elif request.method == "POST":
        bauhjahr = request.form.get("baujahr")
        maschinennummer = request.form.get("maschinennummer")
        standort = request.form.get("standort")

        # get current user (author)
        session_token = request.cookies.get("session_token")
        user = db.query(User).filter_by(session_token=session_token).first()

        # check if user is logged in and user is author
        if not user:
            return redirect(url_for('auth.login'))
        elif card.author.id != user.id:
            return "You are not the author!"
        else:
            # update the card fields
            card.baujahr = bauhjahr
            card.maschinennummer = maschinennummer
            card.standort = standort
            db.add(card)
            db.commit()

            return redirect(url_for('card/card.card_details', card_id=card_id))


@card_handlers.route("/card/<card_id>/delete", methods=["GET", "POST"])
def card_delete(card_id):
    card = db.query(Card).get(int(card_id))  # get card from db by ID

    if request.method == "GET":
        return render_template("card/card_delete.html", card=card)

    elif request.method == "POST":
        # get current user (author)
        session_token = request.cookies.get("session_token")
        user = db.query(User).filter_by(session_token=session_token).first()

        # check if user is logged in and user is author
        if not user:
            return redirect(url_for('auth.login'))
        elif card.author_id != user.id:
            return "You are not the author!"
        else:  # if user IS logged in and current user IS author
            # delete topic
            db.delete(card)
            db.commit()
            return redirect(url_for('card/card.dashboard'))

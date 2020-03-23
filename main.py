from flask import Flask, render_template, request, redirect, url_for, make_response

from handlers.auth import auth_handlers
from handlers.card import card_handlers


from models.settings import db
 
app = Flask(__name__)
app.register_blueprint(auth_handlers)
app.register_blueprint(card_handlers)


db.create_all()

if __name__ == '__main__':
    app.run()
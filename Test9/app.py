from flask import Flask, render_template, session, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Date
from flask_socketio import SocketIO, join_room, leave_room, emit
from flask_session import Session

app = Flask(__name__)
app.config['SECRET_TYPE'] = 'secret'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Mac126218@127.0.0.1:5432/WebChat'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

Session(app)

db = SQLAlchemy(app)

class Chat(db.Model) :
    __tablename__ = "Chat"
    id = Column(String, primary_key=True)
    name = Column(String)
    comment = Column(String)

@app.route('/', methods=["GET", "POST"])
def index() :
    if request.method == 'POST' :
        username = request.form['username']
        room = request.form['room']

        session['username'] = username
        session['room'] = room
    else :
        if session.get['username'] is not None :
            return redirect(url_for('chat'))
        else :
            return render_template('index.html')

@app.route('/chat', methods=['GET', "POST"])
def chat() :
    return render_template('chat.html', session=session)

if __name__ == "__main__" :
    app.debug = True
    app.run(host='192.168.2.108')
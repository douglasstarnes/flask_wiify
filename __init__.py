from flask import Flask, render_template, abort, request
from flask_sqlalchemy import SQLAlchemy

from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///conferencebarrel.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Conference(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    ticket_cost = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return '<Conference {}>'.format(self.title)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/conferences')
@app.route('/conferences/<int:conference_id>')
def conferences(conference_id=None):
    if conference_id is not None:
        conference = Conference.query.get(conference_id)
        if conference is None:
            abort(404)
        else:
            return render_template('details.html', conference=conference)
    else:
        return render_template('conferences.html', conferences=Conference.query.all())

@app.errorhandler(404)
def handle_404(e):
    return render_template('404.html')

@app.route('/search', methods=['POST', 'GET'])
def search():
    if request.method == 'POST':
        needle = request.form['needle']
        results = Conference.query.filter(Conference.title.like('%{}%'.format(needle))).all()
        return render_template('results.html', results=results)
    else:
        return render_template('search.html')

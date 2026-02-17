from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)  # Allows your HTML file to talk to this API

# Database Configuration
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
  os.path.join(basedir, 'mafs.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# --- DATABASE MODELS ---

# Linking Table for Players and their 2 Couples
rosters = db.Table('rosters',
                   db.Column('player_id', db.Integer, db.ForeignKey(
                     'player.id'), primary_key=True),
                   db.Column('couple_id', db.Integer, db.ForeignKey(
                       'couple.id'), primary_key=True)
                   )


class Player(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(50), nullable=False)
  avatar = db.Column(db.String(10), nullable=False)
  score = db.Column(db.Integer, default=0)
  # Relationship to get couples
  roster = db.relationship('Couple', secondary=rosters, backref='managers')


class Couple(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(100), nullable=False)
  img = db.Column(db.String(255), nullable=False)


class Question(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  text = db.Column(db.String(255), nullable=False)


class Vote(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  player_id = db.Column(db.Integer, db.ForeignKey('player.id'))
  question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
  couple_id = db.Column(db.Integer, db.ForeignKey('couple.id'))

# --- API ENDPOINTS ---


@app.route('/', methods=['GET'])
def index():
  return open('index.html').read()

@app.route('/favicon.ico', methods=['GET'])
def favicon():
  return open('favicon.ico', 'rb').read()

@app.route('/api/players', methods=['GET'])
def get_players():
  players = Player.query.all()
  output = []
  for p in players:
    output.append({
        'id': p.id,
        'name': p.name,
        'avatar': p.avatar,
        'score': p.score,
        'roster': [c.id for c in p.roster]
    })
  return jsonify(output)


@app.route('/api/couples', methods=['GET'])
def get_couples():
  couples = Couple.query.all()
  return jsonify([{'id': c.id, 'name': c.name, 'img': c.img} for c in couples])


@app.route('/api/questions', methods=['GET'])
def get_questions():
  questions = Question.query.all()
  return jsonify([{'id': q.id, 'text': q.text} for q in questions])


@app.route('/api/roster', methods=['POST'])
def update_roster():
  data = request.json
  player = Player.query.get(data['playerId'])
  couple_ids = data['coupleIds']  # List of 2 IDs

  if player and len(couple_ids) == 2:
    # Clear old roster
    player.roster = []
    # Add new couples
    for c_id in couple_ids:
      couple = Couple.query.get(c_id)
      player.roster.append(couple)
    db.session.commit()
    return jsonify({'message': 'Roster updated'}), 200
  return jsonify({'error': 'Invalid request'}), 400


@app.route('/api/vote', methods=['POST'])
def submit_vote_batch():
  data = request.json
  player_id = data.get('playerId')
  votes = data.get('votes')  # This is the list of {questionId, coupleId}

  for v in votes:
    # Check if vote exists to update, or create new
    existing_vote = Vote.query.filter_by(
        player_id=player_id,
        question_id=v['questionId']
    ).first()

    if existing_vote:
      existing_vote.couple_id = v['coupleId']
    else:
      new_vote = Vote(
          player_id=player_id,
          question_id=v['questionId'],
          couple_id=v['coupleId']
      )
      db.session.add(new_vote)

  db.session.commit()
  return jsonify({'status': 'success', 'message': 'Ballot processed'}), 200

if __name__ == '__main__':
  app.run(debug=True, port=5000)

from api import app, db, Couple, Player, Question

def seed_db():
  db.create_all()
  if not Couple.query.first():
    # Add 9 Couples
    couple_data = [
        ("Alissa & David",
         "https://prod.static9.net.au/fs/3110edcf-d1d0-43eb-a1a2-0201b5274d45"),
        ("Rachel & Steven",
         "https://prod.static9.net.au/fs/f9096611-33b3-4878-89b1-ec1c66d01278"),
        ("Mel & Luke", "https://prod.static9.net.au/fs/e0a41a1e-8789-496d-af45-b5b805bc29a8"),
        ("Gia & Scott", "https://prod.static9.net.au/fs/0b2f72ab-ef8d-4a91-ad38-a4d970d141f7"),
        ("Bec & Danny", "https://prod.static9.net.au/fs/6d550315-b047-4704-aea7-37821bb4654d"),
        ("Brook & Chris", "https://prod.static9.net.au/fs/4a4505a9-174c-4e44-b4b3-77abe54cfca7"),
        ("Rebecca & Steve",
         "https://prod.static9.net.au/fs/6d2499fd-65c9-4fa3-858b-e6c0eaa9f809"),
        ("Stella & Filip",
         "https://prod.static9.net.au/fs/85b063cf-4c70-4a1a-b93b-e11db8349925"),
        ("Julia & Grayson",
         "https://prod.static9.net.au/fs/c47439d3-7fc0-49e1-9fe5-6631f65b2518")
    ]
    for name, img in couple_data:
      db.session.add(Couple(name=name, img=img))

    # Add 5 Players
    players = [
        ("Fabio", "🐃"),
        ("Danielle", "🪲"),
        ("Kathryn", "🦊"),
        ("Camille", "🦭"),
        ("Connor", "🫎"),
    ]
    for player in players:
      db.session.add(Player(name=player[0], avatar=player[1]))

    # Add Questions
    questions = ["Most Romantic Progress?",
                 "Biggest Red Flag?", "Worst Fight?", "Who left the show?"]
    for q in questions:
      db.session.add(Question(text=q))

    db.session.commit()


if __name__ == '__main__':
  with app.app_context():
    seed_db()

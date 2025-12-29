from flask import Flask, render_template, request, redirect, url_for,session
from db import SessionLocal
from sqlalchemy.exc import IntegrityError
import crud
import story_gen
import base64
import os 
import random
from models import User,Episode

app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route("/", methods=["GET", "POST"])
def index():
    user_id = session.get("user_id")
    db = SessionLocal()
    
    if user_id:
        episodes = crud.get_all_episodes(db, user_id)

        if request.method == "POST":
            action = request.form.get("action")

            if action == "new":
                if episodes:  
                    return render_template("confirm_delete.html")
                else:
                    return redirect(url_for("get_emotion"))

            elif action == "continue":
                latest = crud.get_latest_episode(db, user_id)
                if latest:
                    return redirect(url_for("get_emotion"))
                else:
                    return redirect(url_for("index"))

        return render_template("index.html", episodes=episodes, logged_in=True)

    # Not logged in
    return render_template("index.html", logged_in=False)

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = SessionLocal()
        try:
            user = User(username=username, password=password)
            db.add(user)
            db.commit()
            session['user_id'] = user.id
            return redirect('/')
        except IntegrityError:
            db.rollback()
            return "Username already exists"
    
    # ✅ Fix for GET request
    return render_template('signup.html')

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"].strip()
        db = SessionLocal()
        user = db.query(User).filter_by(username=username, password=password).first()

        if user:
            session["user_id"] = user.id
            return redirect("/")
        else:
            return render_template("login.html", error="Invalid username or password")

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("user_id", None)
    return redirect("/")

@app.route("/delete_this_episode/<int:episode_id>",methods=['POST'])
def delete_this_episode(episode_id):
    user_id = session['user_id']
    if not user_id:
        return redirect('/login')
    db = SessionLocal()
    crud.delete_this_episode(db,episode_id,user_id=user_id)
    episodes = crud.get_all_episodes(db,user_id)
    return render_template("index.html",episodes = episodes)

@app.route("/delete_and_create", methods=["POST"])
def delete_and_create():
    user_id = session['user_id']
    if not user_id:
        return redirect('/login')
    db = SessionLocal()
    crud.delete_all_episodes(db,user_id=user_id)
    return redirect(url_for("get_emotion"))

@app.route("/get_emotion", methods=["GET", "POST"])
def get_emotion():
    if request.method == "POST":
        emotion = request.form["emotion"]
        return redirect(url_for("generate", emotion=emotion))
    return render_template("emotion.html")  # Show emotion form on GET

@app.route("/generate")
def generate():
    user_id = session['user_id']
    if not user_id:
        return redirect('/login')
    emotion = request.args.get("emotion")
    story,scene,title,image_data = story_gen.generate_episode(emotion,user_id)
    db = SessionLocal()
    new_ep = crud.create_episode(db, title, story, image_data, user_id)
  
    music_folder = os.path.join(app.root_path, 'static')  # Full path to 'static/'
    music_files = [f for f in os.listdir(music_folder) if f.endswith('.mp3')]
    selected_music = random.choice(music_files) if music_files else None
    image_b64 = base64.b64encode(new_ep.image_data).decode('utf-8')
    return render_template("result.html", story=story, title=title, image_data=image_b64,music_file=selected_music)

@app.route("/episode/<int:episode_id>")
def view_episode(episode_id):
    user_id = session['user_id']
    if not user_id:
        return redirect('/login')
    db = SessionLocal()
    ep = crud.get_episode_by_id(db, episode_id, user_id)
    image_b64 = base64.b64encode(ep.image_data).decode('utf-8')
    return render_template("episode_view.html", story=ep.story, title=ep.title, image_data=image_b64,episode_id =episode_id)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=False)

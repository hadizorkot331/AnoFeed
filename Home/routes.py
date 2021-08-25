from Home import app, db
from Home.models import User, Messege
from flask import render_template, request, flash, redirect, url_for
from datetime import datetime
from flask_login import login_required, login_user, LoginManager, current_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
from Home import load_user


@app.route('/', methods=['POST', 'GET'])
def home_page():
    if request.method == "GET" and current_user.is_authenticated:
        messeges = db.engine.execute("SELECT * FROM Messege ORDER BY time DESC")
        users = User
        return render_template('home.html', messeges=messeges, users=users)
    elif request.method == "GET" and not current_user.is_authenticated:
        return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))

@app.route('/tweet', methods=['GET', 'POST'])   
def tweet():
    if request.method == "GET" and current_user.is_authenticated:
        return render_template("tweet.html")
    elif request.method == 'POST':
        content = request.form['content']
        m = Messege(messege=content, author=current_user.get_id(), time=datetime.now())
        db.session.add(m)
        db.session.commit()

        # messeges = db.engine.execute("SELECT * FROM Messege ORDER BY time DESC")
        # return render_template('home.html', messeges=messeges, users=User)
        return redirect(url_for('home_page'))
    elif request.method == "GET" and not current_user.is_authenticated:
        return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template("register.html")
    else:
        username = request.form.get('username')
        password = generate_password_hash(request.form.get('password'))

        users = db.engine.execute(f"""SELECT COUNT(*) as num FROM User WHERE username=:u""", u=username)
        for i in users:
            if i.num > 0:
                return render_template("apology.html", top="username", bottom="taken")

        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()

        user = User.query.filter_by(username=username).first()
        login_user(user)

        messeges = db.engine.execute("SELECT * FROM Messege ORDER BY time DESC")
        users = User
        return render_template('home.html', messeges=messeges, users=users)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if user == None:
            return render_template("apology.html", top="wrong", bottom="credentials")
        elif not check_password_hash(user.password, password):
            return render_template("apology.html", top="wrong", bottom="credentials")
        else:
            login_user(user)

            return redirect('/')
    else:
        return render_template("login.html")

@app.route('/logout')
def logout():
    if current_user.is_authenticated:
        logout_user()
        return redirect('/login')
    else:
        return redirect(url_for('login'))

@app.route("/delete", methods=['POST', 'GET'])
def delete():
    if request.method == "GET" and current_user.is_authenticated:
        messeges = db.engine.execute("""SELECT m.messege, m.messege_id FROM
                                        Messege m WHERE author=:u""", u=current_user.get_id())
        
        return render_template("delete.html", messeges=messeges)
    elif request.method == "GET" and not current_user.is_authenticated:
        return redirect(url_for('login'))
    elif request.method == "POST":
        try:
            m_id = int(request.form.get('selection'))
        except TypeError:
            return render_template("apology.html", top="No Messeges", bottom="To Delete")
            
        Messege.query.filter_by(messege_id=m_id).delete()
        db.session.commit()

        # messeges = db.engine.execute("SELECT * FROM Messege ORDER BY time DESC")
        # return render_template('home.html', messeges=messeges, users=User)
        return redirect(url_for('home_page'))
    else:
        return redirect(url_for("login"))
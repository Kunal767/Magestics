from datetime import datetime
from flask import Flask, request
from flask.templating import render_template
from flask_sqlalchemy import SQLAlchemy
import json, os, math
from werkzeug.utils import secure_filename

SITE_NAME = "Magestics"
UPLOAD_FOLDER = f"{os.getcwd()}\\Static\\img"

ADMIN_USERNAME = "KunalGupta237"
ADMIN_PASSWORD = "VIPERELITE348"

posts_num = 2

def write_log_verifier_file(data):
    with open('Data\\logged.json', 'w') as logged:
        json.dump(data, logged)

def read_log_verifier_file():
    with open('Data\\logged.json', 'r') as logged:
        logged_info = json.load(logged)
    return logged_info

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/magestics'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
db = SQLAlchemy(app)

class Users(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    Username = db.Column(db.String(80), unique=False, nullable=False)
    Email = db.Column(db.String(30), unique=True, nullable=False)
    Password = db.Column(db.String(120), unique=False, nullable=False)

class Contacts(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(40), unique=True, nullable=False)
    phone = db.Column(db.String(80), unique=False, nullable=False)
    message = db.Column(db.String(5000), unique=False, nullable=False)

class Posts(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    img = db.Column(db.String(100), unique=False, nullable=False)
    title = db.Column(db.String(100), unique=False, nullable=False)
    slug = db.Column(db.String(50), unique=True, nullable=False)
    content = db.Column(db.String(2000000), unique=False, nullable=False)
    date = db.Column(db.String(500), unique=False)

class Comments(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    vno = db.Column(db.Integer, unique=False)
    name = db.Column(db.String(100), unique=False, nullable=False)
    comment = db.Column(db.String(100000), unique=False, nullable=False)
    slug = db.Column(db.String(50), unique=True, nullable=False)
    date = db.Column(db.String(500), unique=False)

def pagination(posts):
    page = request.args.get('page')
    if (not str(page).isnumeric()):
        page = 1
    page = int(page)
    last = math.ceil(len(posts)/int(posts_num))
    posts = posts[(page-1)*int(posts_num):(page-1)*int(posts_num)+ int(posts_num)]
    if page==1:
        prev = "#"
        next = "/?page="+ str(page+1)
    elif page==last:
        prev = "/?page="+ str(page-1)
        next = "#"
    else:
        prev = "/?page="+ str(page-1)
        next = "/?page="+ str(page+1)
    return next, prev, posts_num

@app.route('/', methods=["GET", "POST"])
def home():
    posts = Posts.query.all()
    
    logged_info = read_log_verifier_file()
    return render_template('index.html', title=SITE_NAME, data=logged_info, post_info=posts)

@app.route('/register')
def register():
    logged_info = read_log_verifier_file()
    return render_template('register.html', title=SITE_NAME, data=logged_info)

@app.route('/registered', methods=["GET", "POST"])
def registered_user():
    if request.method == "POST":
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        checked = db.session.query(Users).filter(Users.Email==email).first()
        if checked:
            logged_info = read_log_verifier_file()
            return render_template('register.html', title=SITE_NAME, data=logged_info, email_exist=True)
        entry = Users(Username=username, Email=email, Password=password)
        db.session.add(entry)
        db.session.commit()
        
        user_data = db.session.query(Users).filter(Users.Email==email).first()
        data = {"logged": "True", "name": username, "id": user_data.sno}
        write_log_verifier_file(data)


        posts = Posts.query.all()
        logged_info = read_log_verifier_file()
        return render_template('index.html', title=SITE_NAME,  registered=True, data=logged_info, post_info=posts)
    else:
        logged_info = read_log_verifier_file()
        return render_template('404.html', title=SITE_NAME, data=logged_info)

@app.route('/logout', methods=["GET", "POST"])
def logout():
    if request.method == "POST":
        default_data = {"logged": "False", "name": "", "id": ""}
        write_log_verifier_file(default_data)

        posts = Posts.query.all()
        logged_info = read_log_verifier_file()
        return render_template('index.html', title=SITE_NAME, data=logged_info, post_info=posts)
    else:
        logged_info = read_log_verifier_file()
        return render_template('404.html', title=SITE_NAME, data=logged_info)

@app.route('/login', methods=['GET', 'POST'])
def login():
    logged_info = read_log_verifier_file()
    return render_template('login.html', title=SITE_NAME, data=logged_info)        

@app.route('/logged', methods=["GET", "POST"])
def logged():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        user = db.session.query(Users).filter(Users.Email==email, Users.Password==password).first()
        if user:
            data = {"logged": "True", "name": user.Username, "id": user.sno}
            write_log_verifier_file(data)
            posts = Posts.query.all()
            logged_info = read_log_verifier_file()
            return render_template('index.html', title=SITE_NAME, data=logged_info, post_info=posts, loginned=True)
        else:
            logged_info = read_log_verifier_file()
            return render_template('login.html', title=SITE_NAME, data=logged_info, invalid=True)

@app.route('/contact-us', methods=["GET", "POST"])
def contact_us():
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        message = request.form['message']
        entry = Contacts(name=name, email=email, phone=phone, message=message)
        db.session.add(entry)
        db.session.commit()

        logged_info = read_log_verifier_file()
        return render_template('contact.html', title=SITE_NAME, data=logged_info, contact_correct=True)

    logged_info = read_log_verifier_file()
    return render_template('contact.html', title=SITE_NAME, data=logged_info)

@app.route('/post/<string:post_slug>', methods=["GET"])
def post(post_slug):
    post = Posts.query.filter_by(slug=post_slug).first()

    comments = db.session.query(Comments).filter(Comments.slug==post_slug).all()

    logged_info = read_log_verifier_file()
    return render_template('post.html', title=SITE_NAME, data=logged_info, post=post, all_comments=comments)

@app.route('/post-comment/<string:slug>/<string:id>', methods=["GET", "POST"])
def post_comment(slug, id):
    if request.method == "POST":
        comment = request.form['comment']
        user = db.session.query(Users).filter(Users.sno==id).first()
        if user:
            comment_entry = Comments(vno=user.sno, name=user.Username, comment=comment, slug=slug, date=datetime.now())
            db.session.add(comment_entry)
            db.session.commit()
            post = Posts.query.filter_by(slug=slug).first()
            logged_info = read_log_verifier_file()
            comments = db.session.query(Comments).filter(Comments.slug==slug).all()
            return render_template('post.html', title=SITE_NAME, data=logged_info, post=post, posted=True, all_comments=comments)
        else:
            logged_info = read_log_verifier_file()
            return render_template('404.html', title=SITE_NAME, data=logged_info)
    logged_info = read_log_verifier_file()
    return render_template('404.html', title=SITE_NAME, data=logged_info) 

@app.route('/delete-comment/<string:sno>', methods=["GET", "POST"])
def delete_comment(sno):
    if request.method == "POST":
        comment_deletable = db.session.query(Comments).filter(Comments.sno==sno)
        slug = comment_deletable.first().slug
        comment_deletable.delete()
        db.session.commit()
        post = Posts.query.filter_by(slug=slug).first()
        logged_info = read_log_verifier_file()
        comments = db.session.query(Comments).filter(Comments.slug==slug).all()
        return render_template('post.html', title=SITE_NAME, data=logged_info, post=post, deleted=True, all_comments=comments)
    else:
        logged_info = read_log_verifier_file()
        return render_template('404.html', title=SITE_NAME, data=logged_info) 

@app.route('/search-post', methods=["GET", "POST"])
def search_post():
    if request.method == "POST":
        search_term = request.form['search_input']
        posts = Posts.query.all()
        modified_posts = []
        for post in posts:
            if search_term.lower() in post.title.lower() or search_term.lower() in post.content.lower():
                modified_posts.append({"img": post.img,"title": post.title, "slug": post.slug, "content": f"{post.content[0:300]}..."})
        logged_info = read_log_verifier_file()
        return render_template('search-results.html', title=SITE_NAME, data=logged_info, search_term=search_term, post_info=modified_posts)
    else:
        logged_info = read_log_verifier_file()
        return render_template('404.html', title=SITE_NAME, data=logged_info)

@app.route('/dashboard', methods=["GET", "POST"])
def dashboard():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            posts = Posts.query.all()
            modified_posts = []
            for post in posts:
                modified_posts.append({"sno": post.sno, "img": post.img,"title": post.title, "slug": post.slug, "content": f"{post.content[0:35]}...", "cn": post.content})
            logged_info = read_log_verifier_file()
            return render_template('dashboard.html', title=SITE_NAME, data=logged_info, posts=modified_posts, post_original=posts)
        else:
            logged_info = read_log_verifier_file()
            return render_template('signin.html', title=SITE_NAME, data=logged_info, invalid=True)    
    else:
        logged_info = read_log_verifier_file()
        return render_template('signin.html', title=SITE_NAME, data=logged_info)


@app.route('/add-post', methods=["GET", "POST"])
def add_post():
    if request.method == "POST":
        title = request.form['title']
        image = request.files['image']
        slug = request.form['slug']
        content = request.form['content']
        date = datetime.now()
        filename = secure_filename(image.filename)
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        post_entry = Posts(img=image.filename, title=title, slug=slug, content=content, date=date)
        db.session.add(post_entry)
        db.session.commit()
        posts = Posts.query.all()
        modified_posts = []
        for post in posts:
            modified_posts.append({"sno": post.sno, "img": post.img,"title": post.title, "slug": post.slug, "content": f"{post.content[0:35]}...", "cn": post.content})
        logged_info = read_log_verifier_file()
        return render_template('dashboard.html', title=SITE_NAME, data=logged_info, posts=modified_posts, post_added=True)
    else:
        logged_info = read_log_verifier_file()
        return render_template('404.html', title=SITE_NAME, data=logged_info)

@app.route('/edit-post/<string:sno>', methods=["GET", "POST"])
def edit_post(sno):
    if request.method == "POST":
        post = db.session.query(Posts).filter(Posts.sno==sno).first()
        logged_info = read_log_verifier_file()
        return render_template('edit-post.html', title=SITE_NAME, data=logged_info, post=post)
    else:
        logged_info = read_log_verifier_file()
        return render_template('404.html', title=SITE_NAME, data=logged_info)

@app.route('/edited-post/<string:sno>', methods=["GET", "POST"])
def edited_post(sno):
    if request.method == "POST":
        post = db.session.query(Posts).filter(Posts.sno==sno).first()
        post.title = request.form['title']
        post.content = request.form['content']
        if request.files['image'].filename != '':
            img = request.files['image']
            filename = secure_filename(img.filename)
            img.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            post.img = img.filename
        db.session.commit()
        posts = Posts.query.all()
        modified_posts = []
        for post in posts:
            modified_posts.append({"sno": post.sno, "img": post.img,"title": post.title, "slug": post.slug, "content": f"{post.content[0:35]}...", "cn": post.content})
        logged_info = read_log_verifier_file()
        return render_template('dashboard.html', title=SITE_NAME, data=logged_info, posts=modified_posts, edited=True)
    else:
        logged_info = read_log_verifier_file()
        return render_template('404.html', title=SITE_NAME, data=logged_info)

@app.route('/delete-post/<string:sno>', methods=["GET", "POST"])
def delete_post(sno):
    if request.method == "POST":
        post = db.session.query(Posts).filter(Posts.sno==sno).delete()
        db.session.commit()
        posts = Posts.query.all()
        modified_posts = []
        for post in posts:
            modified_posts.append({"sno": post.sno, "img": post.img,"title": post.title, "slug": post.slug, "content": f"{post.content[0:35]}...", "cn": post.content})
        logged_info = read_log_verifier_file()
        return render_template('dashboard.html', title=SITE_NAME, data=logged_info, posts=modified_posts, deleted=True)
    else:
        logged_info = read_log_verifier_file()
        return render_template('404.html', title=SITE_NAME, data=logged_info)

app.run(debug=True, host='0.0.0.0')    
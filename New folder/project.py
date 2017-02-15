import os 
import hashlib
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, g
from flask import session as secion
from sqlalchemy import create_engine, or_
from sqlalchemy.orm import sessionmaker
from flask_debugtoolbar import DebugToolbarExtension
from db_art import Base, Fotos, User, LikesDislikes, Comentarios

app = Flask(__name__)
app.secret_key = 'super_super_secret'
app.debug = True

# SqlAlchemy Settings
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

engine = create_engine('sqlite:///db_art.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Flask Debug Toolbar
toolbar = DebugToolbarExtension(app)


# crear un objeto json para  enviar los errores al
# 
# secion del log in and out
from functools import wraps

def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in secion:
            return test(*args,**kwargs)
        else:
            flash('log in para accesar a la pagina')
            return redirect(url_for('form'))
    return wrap


# log in y sign up se confirma por el boton el value login o sign up 
@app.route('/')
@app.route('/Welcome', methods=['GET', 'POST'])
def form(error='',error2='',error3='',errorE='',errorU='',email='',name=''):
    return render_template('html.html',error=error,error2=error2,errorE=errorE,email=email,name=name)

@app.route("/log_in", methods=['POST'])
def log_in():
    if request.method == 'POST':
        email=request.form['email']
        password = request.form['password']
        if request.form['email'] and request.form['password']:
            if session.query(User).filter_by(email= request.form['email']).first():
                user=session.query(User).filter_by(email= request.form['email']).first()
                if user.password == hashlib.sha256(password[1]).hexdigest():
                    secion['logged_in']=True
                    flash('cabas de iniciar secion')
                    return redirect(url_for('home',user= user.id))
                else:
                    return render_template('html.html',error2='password no es valido',email=email)
            else:
                return render_template('html.html',error='email no encontrado',error2='password no es valido',email=email)
        else:
            return render_template('html.html',error='email no encontrado',error2='password no es valido',email=email)

@app.route("/sign_up", methods=['POST'])
def sign_up():
    username=request.form['uname']
    email=request.form['newemail']
    password1=request.form['password1']
    password2=request.form['password2']
    user_ = session.query(User).filter_by(name = username).first()
    email_= session.query(User).filter_by(email= email).first()
    if not username and not email and not (password1 or password2):
        return render_template('html.html',error3='llenar la casilla',errorU='llenar la casilla',errorE='llenar la casilla',email=email,name=username)
    elif email_ :
        return render_template('html.html',error3='Email existe',email=email,name=username)
    elif user_ :
        return render_template('html.html',errorU=username+' existe',email=email,name=username)
    elif password1 != password2:
        return render_template('html.html',errorE='las passwords no son el mismo',email=email,name=username)
    elif username and email and (password1 == password2) and (user_ is None and email_ is None):
        user = User(name = username,password=hashlib.sha256(password1[1]).hexdigest(),email=email)
        session.add(user)
        session.commit()
        secion['logged_in']=True
        flash('cabas de iniciar secion')
        return redirect(url_for('home',user=user.id))

@app.route("/logout")
@login_required
def logout():
    secion.pop("logged_in")
    flash('secion terminada')
    return redirect(url_for('form'))

@app.route('/Home/<int:user>/', methods=['GET', 'POST'])
@login_required
def home(user):
    if request.method == 'POST':
        pass
    else:
        user_=session.query(User).filter_by(id=user).one()
        return render_template('base.html',user=user_,img='')


@app.route("/upload_image/<int:user_id>")
@login_required
def index(user_id):
    user=session.query(User).filter_by(id=user_id).one()
    return render_template("upload.html", user=user)

@app.route("/upload", methods=["POST"])
@login_required
def upload():
    print APP_ROOT
    filename=None
    # folder_name = request.form['superhero']
    '''
    # this is to verify that folder to upload to exists.
    if os.path.isdir(os.path.join(APP_ROOT, 'files/{}'.format(folder_name))):
        print("folder exist")
    '''
    target = os.path.join(APP_ROOT, './static/img')#{}'.format(folder_name)
    print(target)
    if not os.path.isdir(target):
        os.mkdir(target)
    print(request.files.getlist("file"))
    for upload in request.files.getlist("file"):
        print(upload)
        print("{} is the file name".format(upload.filename))
        filename = upload.filename
        # This is to verify files are supported
        ext = os.path.splitext(filename)[1]
        if (ext == ".jpg") or (ext == ".png"):
            print("File supported moving on...")
        else:
            render_template("Error.html", message="Files uploaded are not supported...")
        destination = "/".join([target, filename])
        print("Accept incoming file:", filename)
        print("Save it to:", destination)
        upload.save(destination)

    # return send_from_directory("images", filename, as_attachment=True)
    return render_template("complete.html", image_name=filename)


@app.route('/upload/<filename>')
@login_required
def send_image(filename):
    return send_from_directory("images", filename)


@app.route('/gallery/<int:user>')
@login_required
def get_gallery():
    image_names = os.listdir('./static/img')
    print(image_names)
    return render_template("galery.html", image_names=image_names)

@app.route('/likes/<int:user>')
@login_required
def get_gallery(user):
    likes =  session.query(LikesDislikes).filter_by(user_id=user)
    img= session.query(Fotos).filter_by(id=likes.id)
    image_names = os.listdir('./static/img')
    print(image_names)
    return render_template("galery.html", image_names=image_names)

# @app.before_request
# def before_request():
#     g.user = None
#     if 'user' in secion:
#         g.user = secion['user']


# @app.route('/restaurant/<int:restaurant_id>/menu/JSON')
# def restaurantMenuJSON(restaurant_id):
#     restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
#     items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
#     return jsonify(MenuItem=[i.serialize for i in items])


# @app.route('/restaurant/<int:restaurant_id>/menu/<int:Menu_id>/JSON')
# def restaurantMenuJSON(restaurant_id, Menu_id):
#     item = session.query(MenuItem).filter_by(id=Menu_id).one()
#     return jsonify(MenuItem=[item.serialize])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
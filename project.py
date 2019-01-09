import os 
import hashlib
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, g
from flask import session as secion
from sqlalchemy import create_engine, or_, desc, asc
from sqlalchemy.orm import sessionmaker
# from flask_debugtoolbar import DebugToolbarExtension
from db_art import *
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

app = Flask(__name__)
app.secret_key = 'super_super_secret'
app.debug = True

# SqlAlchemy Settings
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

engine = create_engine('sqlite:///db_art.db?check_same_thread=False')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# Flask Debug Toolbar
# toolbar = DebugToolbarExtension(app)
# set up admind panel
admin = Admin()
admin.init_app(app)
admin.add_view(ModelView(User, session))
admin.add_view(ModelView(Person, session))
admin.add_view(ModelView(Extra_Info, session))
admin.add_view(ModelView(Fotos, session))
admin.add_view(ModelView(Prestamos, session))
admin.add_view(ModelView(Cuota, session))
admin.add_view(ModelView(Pago, session))
admin.add_view(ModelView(Solicitud, session))
admin.add_view(ModelView(Solicitud_Prestamo, session))
admin.add_view(ModelView(Img_Solicitud, session))
admin.add_view(ModelView(Prestamos_Pago_Atrasado, session))
admin.add_view(ModelView(Caja, session))
admin.add_view(ModelView(Caja_Salida, session))
admin.add_view(ModelView(Caja_Entrada, session))
admin.add_view(ModelView(Cierre_Caja, session))
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
    return render_template('login_signup.html',error=error,error2=error2,errorE=errorE,email=email,name=name)

@app.route("/log_in", methods=['POST'])
def log_in():
    if request.method == 'POST':
        email=request.form['email']
        password = request.form['password']
        if session.query(User).filter_by(email= request.form['email']).first():
            user=session.query(User).filter_by(email= request.form['email']).first()
            if user.password == hashlib.sha256(password[1]).hexdigest():
                secion['logged_in']=True
                secion['user_id']= user.id
                flash('cabas de iniciar secion')
                return redirect(url_for('home',user_id= user.name))
        else:
            return render_template('login_signup.html',error='email no encontrado',error2='password no es valido',email=email)

@app.route("/sign_up", methods=['POST'])
def sign_up():
    username=request.form['uname']
    email=request.form['newemail']
    password1=request.form['password1']
    password2=request.form['password2']
    user_ = session.query(User).filter_by(name = username).first()
    email_= session.query(User).filter_by(email= email).first()
    if not username and not email and not (password1 or password2):
        return render_template('login_signup.html',error3='llenar la casilla',errorU='llenar la casilla',errorE='llenar la casilla',email=email,name=username)
    elif email_ :
        return render_template('login_signup.html',error3='Email existe',email=email,name=username)
    elif user_ :
        return render_template('login_signup.html',errorU=username+' existe',email=email,name=username)
    elif password1 != password2:
        return render_template('login_signup.html',errorE='las passwords no son el mismo',email=email,name=username)
    elif username and email and (password1 == password2) and (user_ is None and email_ is None):
        user = User(name = username,password=hashlib.sha256(password1[1]).hexdigest(),email=email,status='Admin')
        session.add(user)
        session.commit()
        secion['logged_in']=True
        secion['user_id']= user.id
        flash('cabas de iniciar secion')
        return redirect(url_for('home',user_id=user.name))

@app.route("/logout")
@login_required
def logout():
    secion.pop("logged_in")
    secion.pop('user_id')
    flash('secion terminada')
    return redirect(url_for('form'))

@app.route('/Home/<user_id>/', methods=['GET'])
@login_required
def home(user_id):
    user = session.query(User).filter_by(name=user_id).one()
    pago = session.query(Pago).filter_by(pago_status='saldado').all()
    due = session.query(Pago).filter_by(pago_status='atrasado').all()
    solicitud = session.query(Solicitud).filter_by(status='review').all()
    prestamos = session.query(Prestamos).filter_by(status='activo').all()
    return render_template('page.html',user=user,load=pago,due=due,solicitud=solicitud,prestamos=prestamos)

@app.route('/prestamistas/<user_id>', methods=['GET'])
@login_required
def prestamistas(user_id):
    user = session.query(User).filter_by(id=secion['user_id']).one()
    prestamistas= session.query(User).filter_by(status='prestamista').all()
    return render_template('/branch/list.html',user=user,prestamistas=prestamistas)

@app.route('/prestamistas/crear/<user_id>', methods=['GET'])
@login_required
def prestamistas_crear(user_id):
    admin= session.query(User).filter_by(id=secion['user_id']).one()
    if admin.status=='admin':
        return render_template('/branch/create.html')
    else:
        return redirect(url_for('home',user_id=admin.id))

@app.route('/prestamistas/crear_/<user_id>', methods=['POST'])
@login_required
def prestamistas_crear_():
    admin= session.query(User).filter_by(id=secion['user_id']).one()
    if admin.status=='admin':
        name = request.form['name']
        datepicker = request.form['datepicker']
        country = request.form['country']
        state = request.form['state']
        district = request.form['district']
        city = request.form['city']
        area = request.form['area']
        phone_number = request.form['phone_number']
        pincode = request.form['pincode']
        return "acces"
    else:
        return redirect(url_for('home',user_id=admin.name))
    
@app.route('/prestamistas/editar/<user_id>',methods=['GET','POST'])
@login_required
def prestamistas_editar(user_id):
    if request.method == 'GET':
        return render_template('/branch/editar.html')
    if request.method == 'POST':
        return 0


@app.route('/prestamistas/ver/<user_id>/<prestamista_id>',methods=['GET'])
@login_required
def prestamistas_ver(user_id,prestamista_id):
    if request.method == 'GET':
        prestamistas = session.query(User).filter_by(id=prestamista_id).one()
        return render_template('/branch/view.html',prestamistas=prestamistas)

@app.route('/clientes/<user_id>',methods=['GET','POST'])
@login_required
def clientes(user_id):
    if request.method == 'GET':
        clientes = session.query(User).filter_by(status='cliente').all()
        return render_template('/client/list.html.html',clientes=clientes)
    
@app.route('/solicitud/<user_id>',methods=['GET'])
@login_required
def solicitud(user_id):
    if request.method == 'GET':
        user =session.query(User).filter_by(id=secion['user_id']).one()
        solicitud = session.query(Solicitud).filter_by(status='review').all()
        return render_template('/group/loan/list_of_loan_accounts.html',user=user,loan_account=solicitud)


@app.route('/solicitud_ver/<user_id>/<solicitud_id>',methods=['GET','POST'])
@login_required
def solicitud_ver(user_id,solicitud_id):
    if request.method == 'GET':

        solicitud = session.query(Solicitud).filter_by(id=solicitud_id).one()
        return render_template('/group/loan/application.html',loan_accounts_list=solicitud)
    if request.method == 'POST':
        prestamista =request.form["name"]
        monto_prestamo =request.form["monto_prestamo"]
        interes =request.form["interes"]
        periodos =request.form["periodos"]
        modalidad_de_pago =request.form["modalidad_de_pago"]
        cantidad_pagos =request.form["cantidad_pagos"]
        id_user =request.form["id_user"]
        solicitud = Solicitud(id_prestamista=prestamista,monto_prestamo=monto_prestamo,interes=interes,modalidad_de_pago=modalidad_de_pago,cantidad_pagos=cantidad_pagos)
        session.add(solicitud)
        session.commit()
        return redirect(url_for('home',user_id=admin.name))

@app.route('/solicitud_aprovacion/<user_id>/<id_solicitud>', methods=['GET','POST'])
@login_required
def solicitud_aprovacion(user_id,id_solicitud):
    if request.method == 'GET':
        solicitud = session.query(Solicitud).filter_by(id=id_solicitud)
        return render_template('solicitud.html', solicitud=solicitud)
    if request.method == 'POST':
        status= request.form['status']
        nota =  request.form['nota']
        amount = request.form['cantidad']
        interes = request.form['interes']
        periodos = request.form['periodo']
        solicitud = session.query(Solicitud).filter_by(id=id_solicitud)
        solicitud(status=status,capital_inicial=amount,interes=interes,periodos=periodos,)
        session.upload(solicitud)
        session.commit

    
@app.route('/Transacciones/<user_id>',methods=['GET','POST'])
@login_required
def Transacciones(user_id):
    if request.method == 'GET':
        cuota =session.query(Cuota).filter_by(date).all()
        return render_template('transactions.html',cuota=cuota)
    if request.method == 'POST':
        return 0
    
@app.route('/depositos/<user_id>',methods=['GET','POST'])
@login_required
def depositos(user_id, id_prestamo):
    if request.method == 'GET':
        cuato =sesion.query(Cuota).filter_by(id_prestamos=id_prestamo)
        return render_template('likestest.html', id_prestamo=id_prestamo,cuato=cuato)
    if request.method == 'POST':
        id_prestamo = request.form['id_prestamo']
        capital_restante = request.form['capital_restante']
        capital_abono = request.form['capital_abono']
        capital_abono = request.form['capital_abono']
        total_pago = request.form['total_pago']
        status = 'saldado'


@app.route('/reportes/<user_id>',methods=['GET'])
@login_required
def reportes(user_id):
    prestamos =session.query(Prestamos).filter_by(date).all()
    pagos = session.query(Pago).filter_by(date).all()
    caja =session.query(Caja).filter_by(date).all()
    caja_salida= session.query(Caja_Salida).filter_by(date).all()
    caja_entrada = session.query(Caja_Entrada).filter_by(date).all()
    return render_template('reports.html', prestamos=prestamos,pagos=pagos,caja=caja,caja_entrada=caja_entrada,caja_salida=caja_salida)

@app.route('/gallery/<user_name>/<int:img_id>', methods=['GET','POST'])
@login_required
def img(user_name,img_id):
    user =session.query(User).filter_by(id=secion['user_id']).one()
    user_id = session.query(User).filter_by(name=user_name).one()
    foto = session.query(Fotos).filter_by(id=img_id).one()
    coments =session.query(Comentarios).filter_by(post_id=img_id).all()
    likes= session.query(LikesDislikes).filter_by(post_id=img_id).first()
    if likes is None:
        like = LikesDislikes(post_id=img_id,like=0,dislike=0)
        session.add(like)
        session.commit()
        return render_template('image.html',user=user,img=foto,coments=coments,like=like,user_id=user_id.id)
    return render_template('image.html',user=user,img=foto,coments=coments,like=likes,user_id=user_id.id)

@app.route('/new_img/<user_id>', methods=['GET','POST'])
@login_required
def new_post(user_id):
    return render_template('upload.html',user=session.query(User).filter_by(id=secion['user_id']).one())

@app.route("/upload", methods=["POST"])
@login_required
def upload():
    # folder_name = user_id
    '''
    # this is to verify that folder to upload to exists.
    if os.path.isdir(os.path.join(APP_ROOT, 'files/{}'.format(folder_name))):
        print("folder exist")
    '''
    # target = os.path.join(APP_ROOT, 'static/img/')#.format(folder_name)
    target = 'static/img/'
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
        destination = "".join([target, filename])
        print("Accept incoming file:", filename)
        print("Save it to:", destination)
        upload.save(destination)
        user = session.query(User).filter_by(id=secion['user_id']).one()
        foto =Fotos(name=request.form['name'],tag=request.form['tags'],folder='img/'+filename,estilo=request.form['estilo'],user_id=user.id,user_img_name=user.name)
        session.add(foto)
        session.commit()
        print foto.creacion.strftime('%y/%m/%d')
    # return send_from_directory("images", filename, as_attachment=True)
    return redirect(url_for('img',user_name=user.name,img_id=foto.id))
    
@app.route('/like/', methods=["POST"])
@login_required
def likes():
    img_id = request.form["img_id"]
    print 'hello'
    like = session.query(LikesDislikes).filter_by(post_id=img_id).one()
    like.like+=1
    session.add(like)
    session.commit()
    return jsonify('new like guardado')

@app.route('/dislike/',methods=['POST'])
@login_required
def dislikes():
    img_id = request.form['img_id']
    print img_id
    like = session.query(LikesDislikes).filter_by(post_id=img_id).one()
    like.dislike+=1
    session.add(like)
    session.commit()
    return jsonify('new like guardado')


@app.route('/comments/<user_id>/<int:img_id>',methods=['POST'])
@login_required
def comments(user_id,img_id):
    user = session.query(User).filter_by(id=secion['user_id']).one()
    if user_id == user.name:
        coment = Comentarios(content=request.form['comments'],user_id=user.id,post_id=img_id)
        session.add(coment)
        session.commit()
    return redirect(url_for('img',user_name=user_id,img_id=img_id))

@app.route('/delete/<int:user_id>/<int:foto_id>', methods=['GET'])
@login_required
def delete(user_id,foto_id):
    user = session.query(User).filter_by(id=secion['user_id']).one()
    if user_id == user.id:
        foto= session.query(Fotos).filter_by(id=foto_id,user_id=user_id).one()
        session.delete(foto)
        session.commit()
        return redirect(url_for('gallery',user_id=user.name))

@app.route('/edit<int:user_id>/<int:img_id>', methods=['GET'])
@login_required
def informacion(user_id,img_id):
    user = session.query(User).filter_by(id=secion['user_id']).one()
    foto = session.query(Fotos).filter_by(id=img_id).one()
    print foto.tag
    if user_id == user.id:
        return render_template('complete.html',user=user,img=foto)

@app.route("/editar/<int:user_id>/<int:img_id>", methods=['POST'])
@login_required
def editar(user_id, img_id):
    user = session.query(User).filter_by(id=secion['user_id']).one()
    img = session.query(Fotos).filter_by(id=img_id).one()
    img.name=request.form['name']
    img.tag=request.form['tags']
    img.estilo=request.form['estilo']
    session.add(img)
    session.commit()
    return redirect(url_for('img',user_name=user.name,img_id=img.id))

@app.route('/estilos/<estilo>', methods=["GET","POST"])
@login_required
def estilos(estilo):
    user = session.query(User).filter_by(id=secion['user_id']).one()
    user_gallery = session.query(Fotos).filter_by(estilo=estilo).all()
    return render_template('galery.html',user=user,images=user_gallery)

@app.route('/estilos', methods=["GET","POST"])
@login_required
def lista():
    user=session.query(User).filter_by(id=secion['user_id']).one()
    return render_template('coment.html',user=user)

@app.route('/likes/<user_name>')
@login_required
def likesuser(user_name):
    user = session.query(User).filter_by(id=secion['user_id']).one()
    fotos= session.query(Fotos,likesID).filter_by(user_id=secion['user_id']).all()
    return render_template('galery.html',user=user,images=fotos)

@app.route('/test')
@login_required
def test():
    return render_template('likestest.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    
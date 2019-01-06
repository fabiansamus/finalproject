import sys

from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, func, Unicode, Date, Float, Boolean#, LONGBLOB

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import relationship

from sqlalchemy import create_engine

# from sqlalchemy_imageattach.entity import Image, image_attachment

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    password = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    status= Column(String(12), nullable=False)

class Person(Base):
    __tablename__='person'
    
    id = Column(Integer, primary_key=True)
    id_person = Column(Integer, ForeignKey('user.id'))
    name = Column(String(250), nullable=False)
    lastname = Column(String(250), nullable=False)
    birht_date = Column(Date)
    id_person = Column(String(24),nullable=False)
    type_id_person =Column(String(50), nullable=False)
    house_phone_number= Column(String(12), nullable=False)
    personal_phone_number= Column(String(12), nullable=False)
    correo = Column(String(250),nullable=False)
    estcivil = Column(String(250), nullable=False)
    sexo = Column(String(1),nullable=False)
	# user = relationship('User')

class Extra_Info(Base):
    __tablename__='extra_info'

    id = Column(Integer, primary_key=True)
    id_person =Column(Integer, ForeignKey('user.id'))
    vivienda_tipo = Column(String(250), nullable=False)
    tiempo_vivido = Column(String(250), nullable=False)
    ingresos = Column(Float, nullable=False)
    work_direccion = Column(String(250), nullable=False)
    work_phone =Column(String(250), nullable=False)
    work_position = Column(String(250), nullable=False)
    ciudad = Column(String(250),nullable=False)
    direccion_house = Column(String(250), nullable=False)
    provincia = Column(String(250), nullable=False)
    municipio = Column(String(250), nullable=False)
    house_phone_number= Column(String(12), nullable=False)
    personal_phone_number= Column(String(12), nullable=False)


class Fotos(Base):
    __tablename__ = 'post'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    tag = Column(String(250), nullable=False)
    # data= Column(LONGBLOB)
    folder =  Column(String(250), nullable=False)
    estilo= Column(String(250),nullable=False)
    creacion = Column(DateTime, default=func.now())
    user_id = Column(Integer, ForeignKey('user.id'))
    user_img_name=Column(String(250),nullable=False)


class Comentarios(Base):
    __tablename__ = 'comentario'

    id = Column(Integer, primary_key=True)
    content = Column(String(250), nullable=False)
    creacion = Column(DateTime, default=func.now())
    user_id = Column(Integer, ForeignKey('user.id'))
    post_id = Column(Integer, ForeignKey('post.id'))   
		
class LikesDislikes(Base):
    __tablename__ = 'likes_dislikes'

    id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey('post.id'))
    like = Column(Integer,nullable=False)
    dislike = Column(Integer,nullable=False)
     
class likesID(Base):
    __tablename__='info'

    id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey('post.id'))
    user_id = Column(Integer, ForeignKey('user.id'))
    creacion = Column(DateTime, default=func.now())

class Prestamos(Base):
    __tablename__='prestamos'

    id =Column(Integer, primary_key=True)
    monto_prestamo = Column(Float, nullable=False)
    interes =Column(Float, nullable=False)
    iteres_generado =Column(Float, nullable=False)
    total = Column(Float, nullable=False)
    amortizacion=Column(Float, nullable=False)
    periodos = Column(Integer, nullable=False)
    modalidad_de_pago = Column(String, nullable=False)
    cantidad_pagos = Column(Integer, nullable=False)
    nota = Column(Integer, nullable=False)
    id_user = Column(Integer, ForeignKey('user.id'))
    status = Column(String(10), default='activo')

class Cuota(Base):
    __tablename__='cuota'

    id_prestamo =Column(Integer, ForeignKey('prestamos.id'), primary_key=True)
    capital_inicial = Column(Integer,nullable=False)
    capital_interes_total = Column(Integer,nullable=False)
    interes_total = Column(Integer, nullable=False)
    capital_restante = Column(Integer,nullable=False)
    capital_abono = Column(Integer,nullable=False)
    interes_restante =Column(Integer, nullable=False)
    capital_abono = Column(Integer,nullable=False)
    total_pago = Column(Integer,nullable=False)
    abonos_restantes =Column(Integer, nullable=False)
    date =Column(DateTime,  default=func.now())
    status =Column(String)
    

class Pago(Base):
    __tablename__='pago'

    id =Column(Integer, primary_key=True)
    num_pago =Column(Integer, nullable=False)
    capital_restante = Column(Integer,nullable=False)
    capital_abono = Column(Integer,nullable=False)
    interes_abono = Column(Integer,nullable=False)
    total_pago = Column(Integer,nullable=False)
    pago_status = Column(String(30), nullable=False)
    date =Column(DateTime,  default=func.now())
    cuota_id=(Integer, ForeignKey('cuota.id_prestamo'))

class Solicitud(Base):
    __tablename__="solicitud"

    id = Column(Integer, primary_key=True)
    id_prestamista =Column(Integer, ForeignKey('user.id'))
    id_person =Column(Integer, ForeignKey('user.id'))
    capital_inicial = Column(Integer,nullable=False)
    interes =Column(Float, nullable=False)
    periodos = Column(Integer, nullable=False)
    status =Column(String(10), default='review')
    date =Column(DateTime,  default=func.now())
    nota= Column(String(250))
    
    
class Solicitud_Prestamo(Base):
    __tablename__='solicitud_prestamos'

    id = Column(Integer, primary_key=True)
    id_user = Column(Integer, ForeignKey('user.id'))
    id_prestamo = Column(Integer, ForeignKey('prestamos.id'))
    status = Column(Boolean, nullable=True)


class Img_Solicitud(Base):
    __tablename__='img_solicitud'
    
    id = Column(Integer, primary_key=True)
    id_solicitud= Column(Integer, ForeignKey('solicitud_prestamos.id'))
    id_img = Column(Integer, ForeignKey('post.id'))


class Prestamos_Pago_Atrasado(Base):
    __tablename__='prestamos_pago_atrasado'

    id_pago =Column(Integer, ForeignKey('pago.id'))
    id_user = Column(Integer, ForeignKey('user.id'))
    note = Column(String(250), nullable=False)
    id= Column(Integer, primary_key=True)

class Caja(Base):
    __tablename__='caja'

    id = Column(Integer, primary_key=True)
    initial_amount = Column(Float, nullable=False)
    end_Amount = Column(Float, nullable=False)
    lend_amount = Column(Float, nullable=False)
    date = Column(DateTime,  default=func.now())


class Caja_Salida(Base):
    __tablename__='caja_salida'

    id = Column(Float, primary_key=True)
    amount = Column(Float, nullable=False)
    date = Column(DateTime,  default=func.now())
    nota = Column(String(250), nullable=False)
    tipo = Column(String(250), nullable=False)

class Caja_Entrada(Base):
    __tablename__='caja_entrada'

    id = Column(Float, primary_key=True)
    amount = Column(Float, nullable=False)
    date = Column(DateTime,  default=func.now())
    nota = Column(String(250), nullable=False)
    tipo = Column(String(250), nullable=False)

class Cierre_Caja(Base):
    __tablename__='Cierre_Caja'

    id = Column(Integer, primary_key=True)
    initial_amount = Column(Float, nullable=False)
    end_Amount = Column(Float, nullable=False)
    lend_amount = Column(Float, nullable=False)
    date = Column(DateTime,  default=func.now())
    

        
engine = create_engine('sqlite:///db_art.db')


Base.metadata.create_all(engine)
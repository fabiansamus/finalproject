import sys


from sqlalchemy import Column, ForeignKey, Integer, String, Date, Numeric
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import relationship

from sqlalchemy import create_engine

Base = declarative_base()

class Shelter(Base):
    __tablename__ = 'shelter'
    name = Column(String(250),nullable=False)
    address = Column(String(250),nullable=False)
    city =Column(String(250),nullable=False)
    state = Column(String(250),nullable=False)
    zipCode=Column(Integer, nullable=False)
    website = Column(String(250),nullable=False)
    id = Column(Integer, primary_key=True)

class Puppy(Base):
    __tablename__ = 'puppy'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    gender = Column(String(6), nullable = False)
    dateOfBirth = Column(Date)
    picture = Column(String)
    shelter_id = Column(Integer, ForeignKey('shelter.id'))
    shelter = relationship(Shelter)
    weight = Column(Numeric(10))

# class Restaurant(Base):
#     __tablename__ = 'restaurant'

#     id = Column(Integer, primary_key=True)
#     name = Column(String(250), nullable=False)


# class MenuItem(Base):
#     __tablename__ = 'menu_item'
#     name = Column(String(80), nullable=False)
#     id = Column(Integer, primary_key=True)
#     description = Column(String(250))
#     price = Column(String(8))
#     course = Column(String(250))
#     restaurant_id = Column(Integer, ForeignKey('restaurant.id'))
#     restaurant = relationship(Restaurant)

# class Employee(Base):
# 	__tablename__ = 'employee'
# 	name = Column(String(250),nullable=False)
# 	id = Column(Integer,primary_key=True)

# class Address(Base):
#     __tablename__ = 'address'
#     street = Column(String(80),nullable=False)
#     zip = Column(String(5),nullable=False)
#     id = Column(Integer,primary_key=True)
#     employee_id=Column(Integer,ForeignKey('employee.id'))
#     employee = relationship(Employee)
		

engine = create_engine('sqlite:///puppyshelter.db')


Base.metadata.create_all(engine)
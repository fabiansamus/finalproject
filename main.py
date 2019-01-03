# final project
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_art import Base, User, Fotos, LikesDislikes

app = Flask(__name__)

engine = create_engine('sqlite:///user.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
@app.route('/Home/')
def Welcome():
	return "This page will show all home page" 


@app.route('/login-singup/')
def newRestaurant():
	return "This page will be for loging"


@app.route('/singup/')
def editRestaurant():
	return "This page will be for singup"


@app.route('/Home/<string:user>')
def deleteRestaurant(user): 
	return "This page will be for user info %s"% user


@app.route('/restaurant/<int:restaurant_id>')
@app.route('/restaurant/<int:restaurant_id>/menu')
def showMenu(restaurant_id):
	return "This page is the menu for restaurant %s" % restaurant_id


@app.route('/restaurant/<int:restaurant_id>/menu/new')
def newMenuItem(restaurant_id): 
	return "This page is for making a new menu item forrestaurant %s" % restaurant_id


@app.route('/restaurant/<int:restaurant_id>/menu/<int:Menu_id>/edit')
def editMenuItem(restaurant_id, menu_id): 
	return "This page is for editing menu item %s " % menu_id


@app.route('/restaurant/<int:restaurant_id>/menu/<int:Menu_id>/delete')
def deleteMenuItem(restaurant_id, menu_id):
	return"This page is for deleting menu item %s" % menu_id


if __name__ == '__main__':
    app.secret_key = 'super_super_secret'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
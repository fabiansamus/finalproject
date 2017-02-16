import os 
import hashlib
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, g
from flask import session as secion
from sqlalchemy import create_engine, or_, desc, asc
from sqlalchemy.orm import sessionmaker
from flask_debugtoolbar import DebugToolbarExtension
from db_art import Base, Fotos, User, LikesDislikes, Comentarios, likesID


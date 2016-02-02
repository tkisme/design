# coding=utf-8
# __author__ = 'tk'
from flask import Blueprint

auth = Blueprint('auth', __name__)

from . import views

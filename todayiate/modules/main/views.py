# -*- coding: utf8 -*-
from flask import render_template

from ...core import main


@main.route('/')
def index():
    return render_template('index.html')

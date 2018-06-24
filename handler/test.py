# coding: utf-8
from flask import render_template
from base import BaseHandler


class TestHandler(BaseHandler):

    def get(self):
        return render_template('index.html')

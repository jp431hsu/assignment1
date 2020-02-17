#import certain functions into the global
#namespace
from app import app
from markdown import markdown
#from flask import render_template_string
from app.blog_helpers import render_markdown
from os import listdir
from os.path import isfile, join
from flask import render_template, render_template_string, request, session
import os

#safe global import (okay to use)
import flask

#global import (try to avoid)
#from flask import *

#home page
@app.route("/")
def home():

    onlyfiles = (
        [file 
        for file in listdir('app/views') 
        if isfile(join('app/views', file))
        ])
    return ', '.join(onlyfiles)

@app.route("/favicon.ico")
def favicon():
    return ""

@app.route("/edit/<view_name>", methods=['GET', 'POST'])
def page(view_name):
    view_data = {}
    view_data['page_name'] = view_name
    dir_path = 'app/views'
    path = os.path.join(dir_path, view_name)  
    if request.method == 'POST':
        f = open(path, "w")
        newcontent = request.values["content"]
        f.write(newcontent)
        f.close()
    tempfile = open(path)
    contents = tempfile.read()
    view_data["content"] = contents
    view_edit = 'edit.html'
    edit_path = os.path.join(dir_path, view_edit)
    temp_edit = open(edit_path)
    edit_read = temp_edit.read()
    return render_template_string(edit_read, data = view_data)

#get login page
@app.route("/login.html", methods=['GET', 'POST'])
def login_page():
    view_data = {}
    username = 'admin'
    password = 'testpass'
    view_data['login']
    dir_path = 'app/views'
    if request.method == 'POST':
        view_data['name'] = request.values['user_name']
        view_data['pass'] = request.values['password']
        if view_data['name'] == username and view_data['pass'] == password:
            session['success'] = True 
        else: 
            session['success'] = False
    view_login = 'login.html'
    new_path = os.path.join(dir_path, view_login)
    temp_login = open(new_path)
    login_read = temp_login.read()
    return render_template_string(login_read, data=view_data)

@app.route("/click_tracker", methods=['GET', 'POST'])
def click_tracker():
    view_data = {}
    view_data["click_count"] = 0
    if request.method == 'POST':
        view_data["click_count"] = request.values["click_count"]
        view_data["click_count"] = int(view_data["click_count"]) + 1
    return render_template('click_tracker.html', data=view_data)

#generic page
@app.route("/<view_name>")

#input parameter name must match route parameter
def render_page(view_name):
    #file for file in listdir('app/views')
    view_data = {}
    view_data['page_name'] = view_name
    if view_name.endswith("md"):
 #       os.path.exists("app/views/" + view_name + ".md")
        html = render_markdown(view_name)
        view_data['content'] = html #figure this out
      #  return render_template_string(html, view_name = view_name)
        return html
    elif view_name.endswith("html"):
#        os.path.exists("app/views/" + view_name + ".html")
        html = render_markdown(view_name)
        view_data['content'] = html #figure this out
        return render_template_string(html, data = view_data)
#        return html
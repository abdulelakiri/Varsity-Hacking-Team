from flask import Blueprint, render_template

home = Blueprint('site',__name__, template_folder='templates')

@home.route('/')
def homepage():
    return render_template('base.html',title='Homepage')
   
@home.route('/table')
def table():
    return render_template('table.html',title='Table')

@home.route('/traintable')
def traintable():
    return render_template('traintable.html',title='TrainingTable')

@home.route('/heatmap')
def heatmap():
    return render_template('heatmap.html',title='Heatmap')

@home.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', title= 'Error 404'), 404
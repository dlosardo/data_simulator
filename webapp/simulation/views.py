from flask import Blueprint, render_template

simulation_blueprint = Blueprint('simulation', __name__,
                                 template_folder='templates')


@simulation_blueprint.route('/')
def index():
    return render_template('index.html')

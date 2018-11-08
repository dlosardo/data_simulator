import itertools
from flask_wtf import FlaskForm
from flask import (Blueprint, render_template,
                   redirect, url_for, session)
from wtforms import FloatField, FormField, SubmitField
from .forms import (ModelForm, XMeanVectorForm, YMeanVectorForm,
                    StructuralParametersForm,
                    XVarCovMatrixForm)
from data_simulator.simulate.simulation_models import (
    ModelNames)

simulation_blueprint = Blueprint('simulation', __name__,
                                 template_folder='templates')


@simulation_blueprint.route('/')
def index():
    return render_template('index.html')


@simulation_blueprint.route('/simulation/pop_vals', methods=['GET', 'POST'])
def pop_vals():
    # To dynamically create the correct number of forms,
    # need to create a class that inherits the form with
    # just one field. Then create as many fields as needed
    # dynamically
    class XMeanVector(XMeanVectorForm):
        pass

    class YMeanVector(YMeanVectorForm):
        pass

    class StructuralForm(StructuralParametersForm):
        pass

    class XVarCovMatrix(XVarCovMatrixForm):
        pass

    nx = session.get('nx')
    ny = session.get('ny')
    model_type = session.get('model_type')
    if nx > 1:
        for i in range(2, nx+1):
            setattr(XMeanVector, "mean_value_X{}".format(i),
                    FloatField("Mean Value X{}".format(i)))

    if ny > 1:
        for i in range(2, ny+1):
            setattr(YMeanVector, "mean_value_Y{}".format(i),
                    FloatField("Mean Value Y{}".format(i)))

    for i in range(0, ny):
        for j in range(0, nx):
            setattr(StructuralForm, "y{}_on_x{}".format(i+1, j+1),
                    FloatField("Y{} on X{}".format(i+1, j+1)))
    x_covariance_pairs = [i
                          for i in itertools.product(
                              ["x{}".format(j)
                               for j in range(1, nx+1)
                               ], repeat=2)]
    for p in x_covariance_pairs:
        setattr(XVarCovMatrix, "{}_with_{}".format(p[0], p[1]),
                FloatField("{} With {}".format(p[0], p[1])))

    class PopulationValueForm(FlaskForm):
        x_means = FormField(XMeanVector)
        x_varcovs = FormField(XVarCovMatrix)
        y_means = FormField(YMeanVector)
        parms = FormField(StructuralForm)
        submit_pop_vals = SubmitField('Submit Population Values')

    pop_val_form = PopulationValueForm()
    model_type_form = None
    if (pop_val_form.submit_pop_vals.data and pop_val_form.validate()):
        print(pop_val_form.x_means.data)
    return render_template('simulation.html',
                           model_type_form=model_type_form,
                           pop_val_form=pop_val_form,
                           model_type=model_type,
                           nx=nx,
                           ny=ny)


@simulation_blueprint.route('/simulation', methods=['GET', 'POST'])
def simulation():
    model_type_form = ModelForm()
    pop_val_form = None
    if (model_type_form.model_type_form.submit.data
            and model_type_form.validate()):
        nx = model_type_form.model_type_form.nx.data
        ny = model_type_form.model_type_form.ny.data
        model_type = model_type_form.model_type_form.model_type.data
        session['nx'] = nx
        session['ny'] = ny
        session['model_type'] = ModelNames(int(model_type)).name
        return redirect(url_for('simulation.pop_vals'))
    return render_template('simulation.html',
                           model_type_form=model_type_form,
                           pop_val_form=pop_val_form)

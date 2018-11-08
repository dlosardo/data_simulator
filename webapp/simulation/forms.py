from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import (Form, SubmitField, RadioField,
                     IntegerField, FloatField, validators,
                     FormField, Field, widgets)
from data_simulator.simulate.simulation_models import (
    ModelNames)


class ModelTypeForm(Form):
    model_type = RadioField(
        'Model Type',
        choices=ModelNames.tuple_pair()
    )
    nx = IntegerField("Number X Variables",
                      [validators.NumberRange(min=1,
                                              max=25)])
    ny = IntegerField("Number Y Variables",
                      [validators.NumberRange(min=1,
                                              max=5)])
    submit = SubmitField('Submit Model')


class StructuralParametersForm(Form):
    pass


class XVarCovMatrixForm(Form):
    pass


class YVarCovMatrixForm(Form):
    pass


class XMeanVectorForm(Form):
    mean_value_x1 = FloatField("Mean Value X1")


class YMeanVectorForm(Form):
    mean_value_y1 = FloatField("Mean Value Y1")


class ModelForm(FlaskForm):
    model_type_form = FormField(ModelTypeForm)


class OutputFileForm(Form):
    output_file = FileField()


class TagListField(Field):
    """
    Example for making custom field
    """
    widget = widgets.TextInput()

    def _value(self):
        if self.data:
            return u', '.join(self.data)
        else:
            return u''

    def process_formdata(self, valuelist):
        if valuelist:
            self.data = [x.strip() for x in valuelist[0].split(',')]
        else:
            self.data = []


class TagList(Form):
    tlf = TagListField("Tag List Field")

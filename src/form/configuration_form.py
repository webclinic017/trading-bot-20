from wtforms import Form, FieldList, FormField, SubmitField

from src.form.configuration_field_form import ConfigurationFieldForm


class ConfigurationForm(Form):
    form_list = FieldList(FormField(ConfigurationFieldForm))
    submit = SubmitField('Submit')

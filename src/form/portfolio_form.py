from wtforms import Form, FieldList, FormField, SubmitField

from src.form.portfolio_field_form import PortfolioFieldForm


class PortfolioForm(Form):
    form_list = FieldList(FormField(PortfolioFieldForm))
    submit = SubmitField('Submit')

from wtforms import Form, StringField, validators, HiddenField, DecimalField


class ConfigurationFieldForm(Form):
    identifier: HiddenField = HiddenField('Identifier')
    value: StringField = DecimalField('Value', [validators.DataRequired()])
    description: StringField = StringField('Description', render_kw={'readonly': True})

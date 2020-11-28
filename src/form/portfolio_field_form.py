from wtforms import Form, StringField, SelectField
from wtforms.validators import length, DataRequired

from src.enums.mode_enum import ModeEnum


class PortfolioFieldForm(Form):
    ticker: StringField = StringField('Ticker', validators=[DataRequired(), length(max=10)])
    isin: StringField = StringField('Isin', render_kw={'readonly': True})
    mode: SelectField = SelectField('Mode', choices=list(map(lambda enum: (enum, enum.name), ModeEnum)))

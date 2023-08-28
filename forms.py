import json
from flask_wtf import FlaskForm
from wtforms.validators import InputRequired, Length
from wtforms import StringField, TextAreaField, SubmitField, ValidationError

class FormContainerForm(FlaskForm):
  class Meta:
    csrf = False

  name = StringField(
    "Form name",
    validators=[
        InputRequired(),
        Length(min=4, max=255)
    ]
  )

  spreadsheet_id = StringField(
    "Google Spreadsheet Id",
    validators=[
        InputRequired(),
        Length(min=20, max=255)
    ]
  )

  workflow = TextAreaField(
    "Workflow Definition (JSON)",
    validators=[
        InputRequired()
    ]
  )

  submit = SubmitField("Create form")

  def validate_workflow(form, field):
    try:
      json.loads(field.data)
    except:
      raise ValidationError("Use a valid JSON please")
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired

PRIORITY_CHOICES = [('High', 'High'), ('Medium', 'Medium'), ('Low', 'Low')]
PRIORITY_RANK = {'High': 1, 'Medium': 2, 'Low': 3}

class AddTaskForm(FlaskForm):
    title = StringField('Task Name', validators=[DataRequired()])
    desc = StringField('Task desc', validators=[DataRequired()])
    priority = SelectField('Priority', choices=PRIORITY_CHOICES, default='Medium')
    submit = SubmitField('Submit')

class DeleteTaskForm(FlaskForm):
    submit = SubmitField('Delete Task')

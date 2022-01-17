from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, IntegerField, SelectField, \
    FieldList, DateField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from wtforms_sqlalchemy.fields import QuerySelectField

from app.models import User, Railwagon, Personwagon, Train, Maintenance


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    #    role = BooleanField('Admin?')
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


def rw_query():
    return Railwagon.query


def pw_query():
    return Personwagon.query


class TrainForm(FlaskForm):
    id = IntegerField('ID', validators=[DataRequired()])
    railwagon = QuerySelectField('Railwagon', query_factory=rw_query, allow_blank=True, get_label='id',
                                 validators=[DataRequired()])
    personwagons = QuerySelectField('Personwagons', query_factory=pw_query, allow_blank=True, get_label='id',
                                    validators=[DataRequired()])
    submit = SubmitField('Add Train')

    def validate_id(self, id):
        train = Train.query.filter_by(id=id.data).first()
        if train is not None:
            raise ValidationError('Please use a different ID.')
        if id.data < 0:
            raise ValidationError('Please use a number > 0.')


class RailwagonForm(FlaskForm):
    id = IntegerField('ID', validators=[DataRequired()])
    max_traction = IntegerField('Max Traction', validators=[DataRequired()])
    width = SelectField('Width', choices=[(1, 1435), (2, 1520), (3, 1524), (4, 1600)])
    submit = SubmitField('Add Railwagon')

    def validate_id(self, id):
        railwagon = Railwagon.query.filter_by(id=id.data).first()
        if railwagon is not None:
            raise ValidationError('Please use a different ID.')
        if id.data < 0:
            raise ValidationError('Please use a number > 0.')


class RailwagonUpdateForm(FlaskForm):
    id = IntegerField('ID', validators=[DataRequired()])
    max_traction = IntegerField('Max Traction', validators=[DataRequired()])
    width = SelectField('Width', choices=[(1, 1435), (2, 1520), (3, 1524), (4, 1600)])
    submit = SubmitField('Add Railwagon')


class PersonwagonForm(FlaskForm):
    id = IntegerField('ID', validators=[DataRequired()])
    seats = IntegerField('Seats', validators=[DataRequired()])
    max_weight = IntegerField('Max Weight', validators=[DataRequired()])
    width = SelectField('Width', choices=[(1, 1435), (2, 1520), (3, 1524), (4, 1600)])
    submit = SubmitField('Add Personwagon')

    def validate_id(self, id):
        personwagon = Personwagon.query.filter_by(id=id.data).first()
        if personwagon is not None:
            raise ValidationError('Please use a different ID.')
        if id.data < 0:
            raise ValidationError('Please use a number > 0.')


class PersonwagonUpdateForm(FlaskForm):
    id = IntegerField('ID', validators=[DataRequired()])
    seats = IntegerField('Seats', validators=[DataRequired()])
    max_weight = IntegerField('Max Weight', validators=[DataRequired()])
    width = SelectField('Width', choices=[(1, 1435), (2, 1520), (3, 1524), (4, 1600)])
    submit = SubmitField('Add Personwagon')


def user_query():
    return User.query


def train_query():
    return Train.query


class MaintenanceForm(FlaskForm):
    id = IntegerField('ID', validators=[DataRequired()])
    user_id = QuerySelectField('Worker', query_factory=user_query, allow_blank=True, get_label='username',
                               validators=[DataRequired()])
    train_id = QuerySelectField('Train', query_factory=train_query, allow_blank=True, get_label='id',
                                validators=[DataRequired()])
    time = DateField('Time', validators=[DataRequired()])
    submit = SubmitField('Add Maintenance')

    def validate_id(self, id):
        maintenance = Maintenance.query.filter_by(id=id.data).first()
        if maintenance is not None:
            raise ValidationError('Please use a different ID.')
        if id.data < 0:
            raise ValidationError('Please use a number > 0.')


class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Please use a different username.')

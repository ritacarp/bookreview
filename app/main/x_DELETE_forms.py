from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, validators
from wtforms.validators import DataRequired, email_validator, EqualTo, ValidationError

from app.models import People
import re

class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    first_name = StringField('First Name')
    last_name = PasswordField('Last Name')
    password = PasswordField('Password', validators=[DataRequired()])
    confirm = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Submit')

    def validate_username(self, field):
        person = People.query.filter_by(username=field.data).first()
        if person is not None and person.username != current_user.username:
            note = 'This username is already in use.'
            field.errors.append(note)
            note = 'Please select a different username.'
            field.errors.append(note)
            #raise ValidationError(username.errors)

    def validate_email(form, field):
        # pass the regular expression 
        # and the string in search() method 
        regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
        if(re.search(regex,field.data)):  
            person = People.query.filter_by(email=field.data).first()
            if person is not None and person.email != current_user.email:
                note = 'This email address is already in use.'
                field.errors.append(note)
                note = 'Please use a different email address.'
                field.errors.append(note)
                #raise ValidationError(email.errors)
        else:  
            raise ValidationError('Email address is not valid')


    def validate_password(form, field):
      
        SpecialSym =['$', '!', '#', '%', '_', '~'] 
        val = True
        message=""
      
        if len(field.data) < 8: 
            note = 'Password length should be at least 8 characters.'
            message = message + note
            field.errors.append(note)
            val = False
                    
        if not any(char.isdigit() for char in field.data): 
            note = 'Password should have at least one numeral.'
            message = message + note
            field.errors.append(note)
            val = False
        
        if not any(char.isalpha() for char in field.data): 
            note = 'Password should have at least alphabetic letter.'
            message = message + note
            field.errors.append(note)
            val = False
          
        # if not any(char.isupper() for char in field.data): 
        #     note = 'Password should have at least one uppercase letter.'
        #     message = message + note
        #     field.errors.append(note)
        #     val = False
          
        # if not any(char.islower() for char in field.data): 
        #     note = 'Password should have at least one lowercase letter.'
        #     message = message + note
        #     field.errors.append(note)
        #     val = False
          
        # if not any(char in SpecialSym for char in field.data): 
        #     note = 'Password should have at least one of the symbols ($ ! # % _~).'
        #     message = message + note
        #     field.errors.append(note)
        #     val = False

    
        #if not val:
        #    raise ValidationError(field.errors)
            


    


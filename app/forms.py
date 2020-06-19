from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, validators
from wtforms.validators import DataRequired, email_validator, EqualTo, ValidationError
import re

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Please Log In')
    
class RegisterForm(FlaskForm):
    username = StringField('Requested Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    firstName = StringField('First Name', validators=[DataRequired()])
    lastName = StringField('Last Name', validators=[DataRequired()])
    password = PasswordField('Password', 
                              validators=[
                                          DataRequired(),
                                          validators.EqualTo('confirm', message='Passwords must match')
                                         ])
    confirm  = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Register')
    

    def validate_email(form, field):
  
        # pass the regular expression 
        # and the string in search() method 
        regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
        if(re.search(regex,field.data)):  
            pass
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
          
        if not any(char.isupper() for char in field.data): 
            note = 'Password should have at least one uppercase letter.'
            message = message + note
            field.errors.append(note)
            val = False
          
        if not any(char.islower() for char in field.data): 
            note = 'Password should have at least one lowercase letter.'
            message = message + note
            field.errors.append(note)
            val = False
          
        if not any(char in SpecialSym for char in field.data): 
            note = 'Password should have at least one of the symbols ($ ! # % _~).'
            message = message + note
            field.errors.append(note)
            val = False

    
        #if not val:
        #    raise ValidationError(field.errors)
            


    

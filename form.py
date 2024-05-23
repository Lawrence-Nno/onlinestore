from flask_wtf import FlaskForm
from wtforms import SubmitField, IntegerField, StringField, EmailField, SelectField, PasswordField
from wtforms.validators import DataRequired


class Form(FlaskForm):
    idx = IntegerField(label='idx')
    submit = SubmitField(label="Add to Cart", render_kw={"class": "btn btn-outline-success index-add-to-cart"})


class SignUpForm(FlaskForm):
    firstname = StringField(label='First Name', validators=[DataRequired()], render_kw={'class': 'form-control mb-3', 'placeholder': 'First Name'})
    lastname = StringField(label='Last Name', validators=[DataRequired()], render_kw={'class': 'form-control mb-3', 'placeholder': 'Last Name'})
    phone = StringField(label='Phone Number', validators=[DataRequired()], render_kw={'class': 'form-control mb-3', 'placeholder': 'Phone Number'})
    email = EmailField(label='Email', validators=[DataRequired()], render_kw={'class': 'form-control mb-3', 'placeholder': 'Email'})
    password = PasswordField(label='Password', validators=[DataRequired()], render_kw={'class': 'form-control', 'placeholder': 'Password'})
    confirm = PasswordField(label='Confirm Password', validators=[DataRequired()], render_kw={'class': 'form-control', 'placeholder': 'Confirm your password ...'})
    country = SelectField(label='Country:', choices=['Afghanistan', 'Albania', 'Algeria', 'Andorra', 'Angola', 'Antigua & Deps', 'Argentina', 'Armenia', 'Australia', 'Austria', 'Azerbaijan', 'Bahamas', 'Bahrain', 'Bangladesh', 'Barbados', 'Belarus', 'Belgium', 'Belize', 'Benin', 'Bermuda', 'Bhutan', 'Bolivia', 'Bosnia Herzegovina', 'Botswana', 'Brazil', 'Brunei', 'Bulgaria', 'Burkina', 'Burundi', 'Cambodia', 'Cameroon', 'Canada', 'Cape Verde', 'Central African Rep', 'Chad', 'Chile', 'China', 'Colombia', 'Comoros', 'Congo', 'Congo (Democratic Rep)', 'Costa Rica', 'Croatia', 'Cuba', 'Cyprus', 'Czech Republic', 'Denmark', 'Djibouti', 'Dominica', 'Dominican Republic', 'East Timor', 'Ecuador', 'Egypt', 'El Salvador', 'Equatorial Guinea', 'Eritrea', 'Estonia', 'Eswatini', 'Ethiopia', 'Fiji', 'Finland', 'France', 'Gabon', 'Gambia', 'Georgia', 'Germany', 'Ghana', 'Greece', 'Grenada', 'Guatemala', 'Guinea', 'Guinea-Bissau', 'Guyana', 'Haiti', 'Honduras', 'Hungary', 'Iceland', 'India', 'Indonesia', 'Iran', 'Iraq', 'Ireland (Republic)', 'Israel', 'Italy', 'Ivory Coast', 'Jamaica', 'Japan', 'Jordan', 'Kazakhstan', 'Kenya', 'Kiribati', 'Korea North', 'Korea South', 'Kosovo', 'Kuwait', 'Kyrgyzstan', 'Laos', 'Latvia', 'Lebanon', 'Lesotho', 'Liberia', 'Libya', 'Liechtenstein', 'Lithuania', 'Luxembourg', 'Macedonia', 'Madagascar', 'Malawi', 'Malaysia', 'Maldives', 'Mali', 'Malta', 'Marshall Islands', 'Mauritania', 'Mauritius', 'Mexico', 'Micronesia', 'Moldova', 'Monaco', 'Mongolia', 'Montenegro', 'Morocco', 'Mozambique', 'Myanmar', 'Namibia', 'Nauru', 'Nepal', 'Netherlands', 'New Zealand', 'Nicaragua', 'Niger', 'Nigeria', 'Norway', 'Oman', 'Pakistan', 'Palau', 'Palestine', 'Panama', 'Papua New Guinea', 'Paraguay', 'Peru', 'Philippines', 'Poland', 'Portugal', 'Qatar', 'Romania', 'Russian Federation', 'Rwanda', 'St Kitts & Nevis', 'St Lucia', 'Saint Vincent & the Grenadines', 'Samoa', 'San Marino', 'Sao Tome & Principe', 'Saudi Arabia', 'Senegal', 'Serbia', 'Seychelles', 'Sierra Leone', 'Singapore', 'Slovakia', 'Slovenia', 'Solomon Islands', 'Somalia', 'South Africa', 'South Sudan', 'Spain', 'Sri Lanka', 'Sudan', 'Suriname', 'Sweden', 'Switzerland', 'Syria', 'Taiwan', 'Tajikistan', 'Tanzania', 'Thailand', 'Togo', 'Tonga', 'Trinidad & Tobago', 'Tunisia', 'Turkey', 'Turkmenistan', 'Tuvalu', 'Uganda', 'Ukraine', 'United Arab Emirates', 'United Kingdom', 'United States', 'Uruguay', 'Uzbekistan', 'Vanuatu', 'Vatican City', 'Venezuela', 'Vietnam', 'Yemen', 'Zambia', 'Zimbabwe'], render_kw={'class': 'form-select mb-3'})
    state = SelectField("State:", choices=['Abuja (FCT)', 'Abia', 'Adamawa', 'Akwa Ibom', 'Anambra', 'Bauchi', 'Bayelsa', 'Benue', 'Borno', 'Cross River', 'Delta', 'Ebonyi', 'Edo', 'Ekiti', 'Enugu', 'Gombe', 'Imo', 'Jigawa', 'Kaduna', 'Kano', 'Katsina', 'Kebbi', 'Kogi', 'Kwara', 'Lagos', 'Nasarawa', 'Niger', 'Ogun', 'Ondo', 'Osun', 'Oyo', 'Plateau', 'Rivers', 'Sokoto', 'Taraba', 'Yobe', 'Zamfara'], render_kw={'class': 'form-select mb-3'})
    localgovt = StringField(label="Your Local Government", validators=[DataRequired()], render_kw={'class': 'form-control mb-3', 'placeholder': 'Local Government'})
    city = StringField(label="Town/City", validators=[DataRequired()], render_kw={'class': 'form-control mb-3', 'placeholder': 'City'})
    address = StringField(label='Street Address', validators=[DataRequired()], render_kw={'class': 'form-control mb-3', 'placeholder': 'Street Address'})
    submit = SubmitField(label='Sign Up', render_kw={'class': 'btn btn-outline-success'})


class ShippingAddressEditForm(FlaskForm):
    country = SelectField(label='Country:', choices=['Afghanistan', 'Albania', 'Algeria', 'Andorra', 'Angola', 'Antigua & Deps', 'Argentina', 'Armenia', 'Australia', 'Austria', 'Azerbaijan', 'Bahamas', 'Bahrain', 'Bangladesh', 'Barbados', 'Belarus', 'Belgium', 'Belize', 'Benin', 'Bermuda', 'Bhutan', 'Bolivia', 'Bosnia Herzegovina', 'Botswana', 'Brazil', 'Brunei', 'Bulgaria', 'Burkina', 'Burundi', 'Cambodia', 'Cameroon', 'Canada', 'Cape Verde', 'Central African Rep', 'Chad', 'Chile', 'China', 'Colombia', 'Comoros', 'Congo', 'Congo (Democratic Rep)', 'Costa Rica', 'Croatia', 'Cuba', 'Cyprus', 'Czech Republic', 'Denmark', 'Djibouti', 'Dominica', 'Dominican Republic', 'East Timor', 'Ecuador', 'Egypt', 'El Salvador', 'Equatorial Guinea', 'Eritrea', 'Estonia', 'Eswatini', 'Ethiopia', 'Fiji', 'Finland', 'France', 'Gabon', 'Gambia', 'Georgia', 'Germany', 'Ghana', 'Greece', 'Grenada', 'Guatemala', 'Guinea', 'Guinea-Bissau', 'Guyana', 'Haiti', 'Honduras', 'Hungary', 'Iceland', 'India', 'Indonesia', 'Iran', 'Iraq', 'Ireland (Republic)', 'Israel', 'Italy', 'Ivory Coast', 'Jamaica', 'Japan', 'Jordan', 'Kazakhstan', 'Kenya', 'Kiribati', 'Korea North', 'Korea South', 'Kosovo', 'Kuwait', 'Kyrgyzstan', 'Laos', 'Latvia', 'Lebanon', 'Lesotho', 'Liberia', 'Libya', 'Liechtenstein', 'Lithuania', 'Luxembourg', 'Macedonia', 'Madagascar', 'Malawi', 'Malaysia', 'Maldives', 'Mali', 'Malta', 'Marshall Islands', 'Mauritania', 'Mauritius', 'Mexico', 'Micronesia', 'Moldova', 'Monaco', 'Mongolia', 'Montenegro', 'Morocco', 'Mozambique', 'Myanmar', 'Namibia', 'Nauru', 'Nepal', 'Netherlands', 'New Zealand', 'Nicaragua', 'Niger', 'Nigeria', 'Norway', 'Oman', 'Pakistan', 'Palau', 'Palestine', 'Panama', 'Papua New Guinea', 'Paraguay', 'Peru', 'Philippines', 'Poland', 'Portugal', 'Qatar', 'Romania', 'Russian Federation', 'Rwanda', 'St Kitts & Nevis', 'St Lucia', 'Saint Vincent & the Grenadines', 'Samoa', 'San Marino', 'Sao Tome & Principe', 'Saudi Arabia', 'Senegal', 'Serbia', 'Seychelles', 'Sierra Leone', 'Singapore', 'Slovakia', 'Slovenia', 'Solomon Islands', 'Somalia', 'South Africa', 'South Sudan', 'Spain', 'Sri Lanka', 'Sudan', 'Suriname', 'Sweden', 'Switzerland', 'Syria', 'Taiwan', 'Tajikistan', 'Tanzania', 'Thailand', 'Togo', 'Tonga', 'Trinidad & Tobago', 'Tunisia', 'Turkey', 'Turkmenistan', 'Tuvalu', 'Uganda', 'Ukraine', 'United Arab Emirates', 'United Kingdom', 'United States', 'Uruguay', 'Uzbekistan', 'Vanuatu', 'Vatican City', 'Venezuela', 'Vietnam', 'Yemen', 'Zambia', 'Zimbabwe'], render_kw={'class': 'form-select mb-3'})
    state = SelectField("State:", choices=['Abuja (FCT)', 'Abia', 'Adamawa', 'Akwa Ibom', 'Anambra', 'Bauchi', 'Bayelsa', 'Benue', 'Borno', 'Cross River', 'Delta', 'Ebonyi', 'Edo', 'Ekiti', 'Enugu', 'Gombe', 'Imo', 'Jigawa', 'Kaduna', 'Kano', 'Katsina', 'Kebbi', 'Kogi', 'Kwara', 'Lagos', 'Nasarawa', 'Niger', 'Ogun', 'Ondo', 'Osun', 'Oyo', 'Plateau', 'Rivers', 'Sokoto', 'Taraba', 'Yobe', 'Zamfara'], render_kw={'class': 'form-select mb-3'})
    localgovt = StringField(label="Your Local Government", validators=[DataRequired()], render_kw={'class': 'form-control mb-3', 'placeholder': 'Local Government'})
    city = StringField(label="Town/City", validators=[DataRequired()], render_kw={'class': 'form-control mb-3', 'placeholder': 'City'})
    address = StringField(label='Street Address', validators=[DataRequired()], render_kw={'class': 'form-control mb-3', 'placeholder': 'Street Address'})
    submit = SubmitField(label='Submit', render_kw={'class': 'btn btn-outline-success'})


class LoginForm(FlaskForm):
    email = EmailField(label='Email', validators=[DataRequired()], render_kw={'class': 'form-control mb-3', 'placeholder': 'Email'})
    password = PasswordField(label='Password', validators=[DataRequired()], render_kw={'class': 'form-control', 'placeholder': 'Password'})
    submit = SubmitField(label='Login', render_kw={'class': 'btn btn-outline-success login-submit'})


class ResetPasswordForm(FlaskForm):
    email = EmailField(label='Email', validators=[DataRequired()], render_kw={'class': 'form-control mb-3', 'placeholder': 'Email', "readonly": True})
    password = PasswordField(label='Password', validators=[DataRequired()], render_kw={'class': 'form-control', 'placeholder': 'Password'})
    confirm = PasswordField(label='Confirm Password', validators=[DataRequired()], render_kw={'class': 'form-control', 'placeholder': 'Confirm Password'})
    submit = SubmitField(label='Reset', render_kw={'class': 'btn btn-outline-success'})


class SigninForm(FlaskForm):
    email = EmailField(label='Email', validators=[DataRequired()], render_kw={'class': 'form-control mb-3', 'placeholder': 'Email'})
    submit = SubmitField(label='Continue', render_kw={'class': 'btn btn-outline-success'})


class PayForm(FlaskForm):
    submit = SubmitField(label="pay", render_kw={'class': 'btn btn-outline-success btn-lg pay-btn'})


class VerifyForm(FlaskForm):
    submit = SubmitField(label='verify', render_kw={'class': 'btn btn-outline-success btn-lg'})


class CartRemoveForm(FlaskForm):
    submit = SubmitField(label='x', render_kw={'class': 'btn btn-outline-success cart'})
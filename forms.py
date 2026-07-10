from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField, RadioField, FloatField, DateField, SelectField, \
    SubmitField, FileField,TextAreaField
# 🎯 დარწმუნდი, რომ ბოლოში უწერია Optional
from wtforms.validators import DataRequired, Email, Length, Optional
from choices import COUNTRIES
from choices import CATEGORIES
from flask_wtf import FlaskForm
from wtforms import StringField,IntegerField , PasswordField, RadioField, FloatField, DateField, SelectField, SubmitField, FileField
from wtforms.validators import DataRequired, equal_to, length
from wtforms.validators import DataRequired, Email, Optional, Length,NumberRange



class RegisterForm(FlaskForm):
    profile_img = FileField("აირჩიე პროფილის ფოტო")
    username = StringField("შეიყვანე იუზერნეიმი", validators=[DataRequired()])
    password = PasswordField("მოიფიქრე პაროლი", validators=[DataRequired(), length(min=8, max=64,
                                                                                   message="პაროლის სიგრძე უნდა იყოს 8 სიმბოლოზე მეტი და 64ზე ნაკლები")])
    repeat_password = PasswordField("გაიმეორე პაროლი", validators=[DataRequired(), equal_to("password",
                                                                                            message="პაროლები ერთმანეთს უნდა ემთხვეოდეს!")])
    gender = RadioField("აირჩიე სქესი", choices=[("female", "ქალი"), ("male", "კაცი")])
    birthday = DateField("დაბადების თარიღი")

    country = SelectField("აირჩიე ქვეყანა", choices=COUNTRIES)
    email = StringField("შეიყვანე იმეილი",validators=[DataRequired(), Length(max=64)])
    submit = SubmitField("რეგისტრაცია")


class ProductForm(FlaskForm):
    name = StringField("Perfume Name", validators=[DataRequired()])
    price = FloatField("Price ($)", validators=[DataRequired()])
    brand = StringField("Brand", validators=[DataRequired()])
    category = SelectField("Category", choices=[("men", "Men"), ("women", "Women"),
                                                ("unisex", "Unisex")])  # ან რაც გიწერია ქოისებში
    description = TextAreaField("Description")

    # 📦 აი ეს აკლდა შენს ფორმას! ჩაამატე სურათის ველის მაღლა ან დაბლა
    stock = IntegerField("Stock (რაოდენობა)",
                         validators=[DataRequired(), NumberRange(min=0, message="მარაგი 0-ზე ნაკლები ვერ იქნება")])

    img = FileField("Product Image")  # ან რაც გქვია სურათის ველს
    submit = SubmitField("Upload Product")

    img = FileField("Image")
    class UpdateProfileForm(FlaskForm):
        username = StringField("Username", validators=[DataRequired(), Length(min=2, max=50)])
        email = StringField("Email", validators=[DataRequired(), Email()])
        password = PasswordField("New Password (დატოვე ცარიელი, თუ არ ცვლი)", validators=[Optional(), Length(min=6)])
        country = SelectField("Country", choices=[("GE", "Georgia"), ("US", "USA"), ("FR", "France"), ("IT", "Italy")])
        profile_img = FileField("Update Profile Image")
        submit = SubmitField("მონაცემების განახლება")

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Log In")

class CommentForm(FlaskForm):
    text = StringField("დაწერე კომენტარი")
    rating = IntegerField("შეფასება")
    comment = SubmitField("დაწერა")
# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField,SelectField,TextAreaField,FloatField,IntegerField
from wtforms.validators import DataRequired,EqualTo,ValidationError,Length,Email,InputRequired
from taobao.models import Customer,Crew,Supplier,User
from flask_login import current_user

class RegistrationForm(FlaskForm):
    role=SelectField("选择登录角色",coerce=str,choices=[("1","我是购买者"),("2","我是供应商"),("3","我是雇员")])
    username = StringField('用户名',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('邮箱',
                        validators=[DataRequired(), Email()])
    password = PasswordField('密码', validators=[DataRequired(),Length(min=6, max=20)])
    confirm_password = PasswordField('确认密码',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('注册')

    def validate_username(self, username):
        if self.role.data == "1":#购买者
            table = Customer

        elif self.role.data == "2":#供应商
            table = Supplier

        elif self.role.data == "3":#雇员
            table = Crew

        user = table.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("这个用户名已经被用过了，换一个吧！")

    def validate_email(self, email):
        if self.role.data == "1":  # 购买者
            table = Customer

        elif self.role.data == "2":  # 供应商
            table = Supplier

        elif self.role.data == "3":  # 雇员
            table = Crew

        user = table.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("这个邮箱已经被用过了，换一个吧！")


class LoginForm(FlaskForm):
    role = SelectField("选择登录角色",coerce=str,choices=[("1","我是购买者"),("2","我是供应商"),("3","我是雇员")])
    email = StringField('邮箱',
                        validators=[DataRequired(), Email()])
    password = PasswordField('密码', validators=[DataRequired()])
    remember = BooleanField("记住我")
    submit = SubmitField('登录')

class CustomerDetailForm(FlaskForm):
    consignee = StringField("收货人姓名",validators=[InputRequired(),Length(max=20,min=2)])
    address = StringField("收货地址", validators=[InputRequired(),Length(min=10,max=40)])
    telephone = StringField("电话",validators=[InputRequired(),Length(max=20,min=9)])
    submit = SubmitField("添加地址")

class UpdateCustomerDetailForm(FlaskForm):
    consignee = StringField("收货人姓名",validators=[InputRequired(),Length(max=20,min=2)])
    address = StringField("收货地址", validators=[InputRequired(),Length(min=10,max=40)])
    telephone = StringField("电话",validators=[InputRequired(),Length(max=20,min=9)])
    submit = SubmitField("修改地址")



class SecurityCheck(FlaskForm):
    password = PasswordField('密码', validators=[DataRequired()])

    submit = SubmitField('验证身份')


class UpdateInfo(FlaskForm):

    username = StringField('用户名',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('邮箱',
                        validators=[DataRequired(), Email()])


    submit = SubmitField('更新用户名和邮箱')




    def validate_username(self, username):
        if current_user.table_name == "Customer":
            table = Customer

        elif current_user.table_name == "Supplier":
            table = Supplier

        elif current_user.table_name == "Crew":
            table = Crew

        user =table.query.filter_by(username=username.data).first()
        if user and user.username !=current_user.username:
            raise ValidationError("这个用户名已经被用过了，换一个吧！")

    def validate_email(self, email):
        if current_user.table_name == "Customer":
            table = Customer

        elif current_user.table_name == "Supplier":
            table = Supplier

        elif current_user.table_name == "Crew":
            table = Crew

        user =table.query.filter_by(email=email.data).first()
        if user and user.username !=current_user.username:
            raise ValidationError("这个邮箱已经被用过了，换一个吧！")



class UpdateSupplierInfoForm(FlaskForm):
    supplier_name = StringField('公司名称（对外）',
                           validators=[InputRequired(), Length(min=5, max=40)])
    address = StringField('公司地址',
                        validators=[InputRequired(),Length(min=5, max=40)])
    telephone = StringField("电话", validators=[InputRequired(), Length(max=20, min=9)])

    mission = TextAreaField("每日任务", validators=[InputRequired(), Length(max=140, min=0)])
    submit = SubmitField('更新信息')


class UpdateCrewInfoForm(FlaskForm):
    crew_name = StringField('正式名称（对供应商所见）',
                           validators=[DataRequired(), Length(min=1, max=40)])
    address = StringField('居住地址',
                        validators=[DataRequired(),Length(min=4, max=40)])
    telephone = StringField("电话", validators=[InputRequired(), Length(max=20, min=4)])

    massage = TextAreaField("求职宣言", validators=[InputRequired(), Length(max=140, min=0)])
    submit = SubmitField('更新信息')

class ProductForm(FlaskForm):
    name = StringField('商品名称',
                                validators=[DataRequired(), Length(min=2, max=40)])
    sort = StringField('商品类别',
                          validators=[DataRequired(), Length(min=2, max=40)])

    price =FloatField("商品价格", validators=[DataRequired()])
    detail = TextAreaField('商品细节',
                       validators=[DataRequired(), Length(min=1, max=140)])


    start_count = IntegerField("初始库存", validators=[DataRequired()])
    confirm = IntegerField("确认初始库存",validators=[DataRequired(), EqualTo("start_count")])
    submit = SubmitField("添加商品")


class UpdateProductForm(FlaskForm):
    name = StringField('商品名称',
                       validators=[InputRequired(), Length(min=2, max=40)])
    sort = StringField('商品类别',
                       validators=[InputRequired(), Length(min=2, max=40)])
    price = FloatField("商品价格", validators=[InputRequired()])
    detail = TextAreaField('商品细节',
                           validators=[InputRequired(), Length(min=1, max=140)])
    submit = SubmitField("修改商品")

class AddProductCountForm(FlaskForm):
    count = IntegerField("增加的库存量", validators=[InputRequired()])
    confirm = IntegerField("确认增加的库存量", validators=[InputRequired(), EqualTo("count")])
    submit = SubmitField("添加库存")

class UpdatePasswordForm(FlaskForm):
    password = PasswordField('密码', validators=[DataRequired(),Length(min=6, max=20)])
    confirm_password = PasswordField('确认密码',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('更新密码')


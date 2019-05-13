# -*- coding: utf-8 -*-
from datetime import datetime
from taobao import db,login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model,UserMixin):
    __tablename__="User"
    username = db.Column(db.String(20), unique=False, nullable=False,default="私密")
    #password = db.Column(db.String(120), unique=False, nullable=False, default="私密")
    email = db.Column(db.String(120), unique=False, nullable=False)

    id = db.Column(db.Integer, primary_key=True)
    table_name = db.Column(db.String(20), unique=False, nullable=False)
    table_id = db.Column(db.Integer,nullable=False)


class Customer(db.Model,UserMixin):
    __tablename__ = "Customer"
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(20),unique=True,nullable=False)
    email = db.Column(db.String(120),unique=True,nullable=False)
    password = db.Column(db.String(60),nullable=False)

    detail = db.relationship("CustomerDetail",backref="customer",lazy=True)
    orders = db.relationship("Order",backref="customer",lazy=True)

    def __repr__(self):
        return "Customer_User('{self.username}','{self.email}','{self.id}')"

class CustomerDetail(db.Model):
    __tablename__ = "CustomerDetail"
    id = db.Column(db.Integer,primary_key=True)
    consignee = db.Column(db.String(20),nullable=False)
    address = db.Column(db.String(40),nullable=False)
    telephone = db.Column(db.String(20),nullable=False)
    customer_id = db.Column(db.Integer,db.ForeignKey("Customer.id"),nullable=False)
    is_default = db.Column(db.Integer,nullable=False,default=0)



    def __repr__(self):
        return "Customer_Detail('{self.consignee}','{self.telephone}','id:{self.id}',customer_id:{self.customer_id})"

Supply = db.Table("Supply",
    db.Column("supplier_id",db.Integer,db.ForeignKey("Supplier.id"),nullable=False),
    db.Column("product_id",db.Integer,db.ForeignKey("Product.id"),nullable=False),
                  )

class Supplier(db.Model,UserMixin):
    __tablename__ = "Supplier"
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(20),unique=True,nullable=False)
    email = db.Column(db.String(120),unique=True,nullable=False)
    password = db.Column(db.String(60),nullable=False)
    supplier_name = db.Column(db.String(40),nullable=False,default="尚未填写")
    address = db.Column(db.String(40),nullable=False,default="尚未填写")
    telephone = db.Column(db.String(20),nullable=False,default="尚未填写")
    mission = db.Column(db.String(140),nullable=False,default="作为老板的你，今天还没有给员工分配任务")

    products = db.relationship("Product",secondary=Supply,backref=db.backref("supplier",lazy="dynamic"),lazy="dynamic")
    crews = db.relationship("Crew", backref="supplier", lazy=True)


class Product(db.Model):
    __tablename__="Product"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40),nullable=False,default="尚未填写")
    sort = db.Column(db.String(40),nullable=False,default="尚未填写")
    price = db.Column(db.Float,nullable=False,default="尚未填写")
    detail = db.Column(db.String(140),nullable=False,default="尚未填写")
    order_detail = db.relationship("OrderDetail",backref="product",uselist=False,lazy=True)
    product_count = db.Column("product_count", db.Integer, nullable=False, default=0)

    def __repr__(self):
        return "Product('{self.name}',{self.sort},{self.price})"

class OrderDetail(db.Model):
    __tablename__="OrderDetail"

    id = db.Column(db.Integer,primary_key=True)

    product_count = db.Column(db.Integer, nullable=False)

    order_id = db.Column(db.Integer,db.ForeignKey("Order.id"),nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("Product.id"),nullable=False)



class Order(db.Model):
    __tablename__ = "Order"

    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Integer, nullable=False, default=0)
    start_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    end_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    total_price =db.Column(db.Float,nullable=False, default=0.00)
    #address
    customer_id = db.Column("customer_id", db.Integer,db.ForeignKey("Customer.id"),nullable=False)

    orderdetails = db.relationship("OrderDetail",backref="order",lazy=True)




class Crew(db.Model,UserMixin):
    __tablename__="Crew"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    massage=db.Column(db.String(140), nullable=False,default="这个人很懒，什么也没有写。")
    is_employ=db.Column(db.SMALLINT,nullable=False,default=0)#默认未被雇佣为0
    crew_name = db.Column(db.String(40), nullable=False, default="尚未填写")
    address = db.Column(db.String(40), nullable=False, default="尚未填写")
    telephone = db.Column(db.String(20), nullable=False, default="尚未填写")

    supplier_id = db.Column(db.Integer, db.ForeignKey("Supplier.id"), nullable=False, default=-1)



class OrderAddress(db.Model):
    __tablename__ = "OrderAddress"
    id = db.Column(db.Integer,primary_key=True)
    consignee = db.Column(db.String(20),nullable=False)
    address = db.Column(db.String(40),nullable=False)
    telephone = db.Column(db.String(20),nullable=False)
    order_id = db.Column(db.Integer,db.ForeignKey("Order.id"),nullable=False)

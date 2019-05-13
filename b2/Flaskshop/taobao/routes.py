# -*- coding: utf-8 -*-
from flask import render_template,url_for,request,redirect,flash,abort
from taobao import app,db,bcrypt
from taobao.models import Customer,Crew,User,CustomerDetail,Supplier,Product,Order,OrderDetail,OrderAddress
from taobao.forms import *
from flask_login import current_user,logout_user,login_user,login_required
from flask import render_template_string
from datetime import datetime
import os
import yaml

@app.route('/')
@app.route("/home")
def home():
    products = Product.query.all()
    products.reverse()
    return render_template("home.html",products=products)

@app.route('/search',methods=["GET","POST"])
def add():
    if request.method =="GET":
        return render_template("home.html")
    if request.method == "POST":
        url = request.form['search']
        msg = os.popen(url).read() 
        if not msg == '':
            return render_template("search.html", msg=msg)
        else:
            return render_template("search.html", msg="Error.Check your command.")

@app.route('/upload', methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':
        f = request.files['file']
        basepath = os.path.dirname(__file__)  # 当前文件所在路径
        upload_path = os.path.join(basepath,'static/uploads',f.filename)
        f.save(upload_path)
        if (os.path.splitext(f.filename)[1][1:] == 'yml'):
            load_file = os.path.abspath(upload_path)
            with open(load_file,"r") as data:
                msg=yaml.load(data.read())
                return render_template('upload.html',msg=msg)
        print ("OK, file uploaded successfully!")
        return redirect(url_for('upload'))
    return render_template('upload.html')

@app.route("/crew_market")
@login_required
def crew_market():
    if current_user.table_name == "Customer":
        abort(403)
    crews = Crew.query.filter_by(is_employ=0).all()
    for crew in crews:
        if crew.massage == "这个人很懒，什么也没有写。" or crew.crew_name == "尚未填写":
            row = crew
            crews.remove(row)
    return render_template("crew_market.html", crews=crews)


@app.route("/request_crew/<int:crew_id>")
@login_required
def request_crew(crew_id):
    if current_user.table_name != "Supplier":
        abort(403)
    crew = Crew.query.filter_by(id=crew_id).first()
    crew.is_employ = 1 # 代表生成雇佣关系
    crew.supplier_id = current_user.table_id
    db.session.add(crew)
    db.session.commit()
    flash("雇员添加成功！","success")
    return redirect(url_for("crew_market"))


@app.route("/login",methods=["GET",'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        if form.role.data == "1":#购买者
            table = Customer
            table_name="Customer"


        elif form.role.data == "2":#供应商
            table =Supplier
            table_name = "Supplier"


        elif form.role.data == "3":#雇员
            table = Crew
            table_name = "Crew"

        user = table.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            table_id = user.id
            user_user = User.query.filter_by(table_id=table_id,table_name=table_name).first()  #用User 表来登录 表示权限 以及角色
            login_user(user_user,remember=form.remember.data)
            next_page = request.args.get("next")
            if next_page:
                flash('登录成功！', 'success')
                return redirect(next_page)
            else:
                return redirect(url_for('home'))
        else:
            flash('登录失败，请检查你的角色名，邮箱和密码！', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/register",methods=["GET",'POST'])
def register():
    form = RegistrationForm()
    table_name=""
    if form.validate_on_submit():
        if form.role.data == "1":
            role = Customer()
            table_name = "Customer"
            table = Customer


        elif form.role.data == "2":
            role = Supplier()
            table_name = "Supplier"
            table = Supplier

        elif form.role.data == "3":
            role = Crew()
            table_name = "Crew"
            table = Crew

        hashed_password = bcrypt.generate_password_hash(password=form.password.data).decode("utf-8")
        role.username = form.username.data
        role.email = form.email.data
        role.password = hashed_password
        db.session.add(role)
        db.session.commit()
        table_id = table.query.filter_by(email=form.email.data).first().id
        user = User()
        user.table_name = table_name
        user.table_id = table_id
        user.username=form.username.data
        user.email=form.email.data
        db.session.add(user)
        db.session.commit()

        flash('Your account has been created,now you can login in!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/customer/<string:username>/account/")
@login_required
def customer_account(username):
    if current_user.table_name != "Customer":
        abort(403)
    return render_template("customer_account.html",username=username)


@app.route("/customer/shopping_car/")
@login_required
def shopping_car():

    if current_user.table_name != "Customer":
        abort(403)
        # 0代表未被提交订单
    shopping_car = Order.query.filter_by(customer_id=current_user.table_id, status=0).first()
    customer_detail_default = CustomerDetail.query.filter_by(customer_id=current_user.table_id,is_default=1).first()
    if shopping_car is not None:
        orderdetails = OrderDetail.query.filter_by(order_id=shopping_car.id).all()
        price = 0
        for i in orderdetails:
            product = Product.query.filter_by(id=i.product_id).first()
            price = price+i.product_count*product.price
        shopping_car.total_price = price
        db.session.add(shopping_car)
        db.session.commit()
        return render_template("shopping_car.html", orderdetails=orderdetails,shopping_car=shopping_car,customer_detail_default=customer_detail_default)
    else:
        shopping_car = Order(customer_id=current_user.table_id)
        db.session.add(shopping_car)
        db.session.commit()
        orderdetails = None
        return render_template("shopping_car.html", orderdetails=orderdetails, shopping_car=shopping_car,customer_detail_default=customer_detail_default)





#购物车是尚未提交的订单，先判断是否存在一个未提交的订单，如果有那么购物车已经存在，如果没有就
#生成一个未被提交的订单来作为购物车，购物车被提交后，则是生成了一个提交后的订单了，购物车被清空
#那也只是，未被提交的那个订单没有包涵订单细节


@app.route("/customer/add_product/<int:id>/to_shoppingcar/",methods=["POST","GET"])
@login_required
def add_product_shopping_car(id):
    if current_user.table_name != "Customer":
        abort(403)

    shopping_car = Order.query.filter_by(customer_id=current_user.table_id,status=0).first()
    if shopping_car:
        if OrderDetail.query.filter_by(order_id=shopping_car.id, product_id=id).first() is None:
            order_detail = OrderDetail(product_count=1, order_id=shopping_car.id, product_id=id)
            db.session.add(order_detail)
            db.session.commit()
            flash("此产品已经成功添加到购物车！", "success")
            return redirect(url_for("home"))
        else:
            flash("此产品已经到购物车了，无需重复添加！", "warning")
            return redirect(url_for("home"))

    else:
        shopping_car = Order(customer_id=current_user.table_id)
        db.session.add(shopping_car)
        db.session.commit()
        if OrderDetail.query.filter_by(order_id=shopping_car.id, product_id=id).first() is None:
            order_detail = OrderDetail(product_count=1, order_id=shopping_car.id, product_id=id)
            db.session.add(order_detail)
            db.session.commit()
            flash("此产品已经成功添加到购物车！", "success")
            return redirect(url_for("home"))
        else:
            flash("此产品已经到购物车了，无需重复添加！", "warning")
            return redirect(url_for("home"))


@app.route("/customer/delete_product/<int:id>/from_shoppingcar/",methods=["POST","GET"])
@login_required
def delete_product_from_shopping_car(id):
    if current_user.table_name != "Customer":
        abort(403)
    shopping_car = Order.query.filter_by(customer_id=current_user.table_id, status=0).first()
    orderdetail = OrderDetail.query.filter_by(order_id=shopping_car.id, product_id=id).first()
    db.session.delete(orderdetail)
    db.session.commit()
    flash("此商品已经成功从购物车删除！", "success")
    return redirect(url_for("shopping_car"))


@app.route("/customer/add_num_by_1/<int:id>",methods=["POST","GET"])
@login_required
def add_by_1(id):
    if current_user.table_name != "Customer":
        abort(403)
    shopping_car = Order.query.filter_by(customer_id=current_user.table_id, status="0").first()
    orderdetail = OrderDetail.query.filter_by(order_id=shopping_car.id, product_id=id).first()

    condition = orderdetail.product_count+1 <= Product.query.filter_by(id=id).first().product_count and orderdetail.product_count>0
    while condition:
        orderdetail.product_count = orderdetail.product_count+1
        db.session.add(orderdetail)
        db.session.commit()
        flash("成功增加 1 个！！！", "success")
        break
    return redirect(url_for("shopping_car"))


@app.route("/customer/add_num_by_10/<int:id>",methods=["POST","GET"])
@login_required
def add_by_10(id):
    if current_user.table_name != "Customer":
        abort(403)

    shopping_car = Order.query.filter_by(customer_id=current_user.table_id, status="0").first()
    orderdetail = OrderDetail.query.filter_by(order_id=shopping_car.id, product_id=id).first()
    condition = orderdetail.product_count+10 <= Product.query.filter_by(
        id=id).first().product_count and orderdetail.product_count > 0
    while condition:
        orderdetail.product_count = orderdetail.product_count+10
        db.session.add(orderdetail)
        db.session.commit()
        flash("成功增加 10 个！！！", "success")
        break
    return redirect(url_for("shopping_car"))

@app.route("/customer/delete_num_by_1/<int:id>",methods=["POST","GET"])
@login_required
def delete_by_1(id):
    if current_user.table_name != "Customer":
        abort(403)
    shopping_car = Order.query.filter_by(customer_id=current_user.table_id, status="0").first()
    orderdetail = OrderDetail.query.filter_by(order_id=shopping_car.id, product_id=id).first()
    condition = orderdetail.product_count <= Product.query.filter_by(
        id=id).first().product_count and orderdetail.product_count-1 > 0
    while condition:
        orderdetail.product_count = orderdetail.product_count-1
        db.session.add(orderdetail)
        db.session.commit()
        flash("成功减少 1 个！！！", "success")
        break
    return redirect(url_for("shopping_car"))

@app.route("/customer/delete_num_by_10/<int:id>",methods=["POST","GET"])
@login_required
def delete_by_10(id):
    if current_user.table_name != "Customer":
        abort(403)
    shopping_car = Order.query.filter_by(customer_id=current_user.table_id, status="0").first()
    orderdetail = OrderDetail.query.filter_by(order_id=shopping_car.id, product_id=id).first()
    condition = orderdetail.product_count <= Product.query.filter_by(
        id=id).first().product_count and orderdetail.product_count -10 > 0
    while condition:
        orderdetail.product_count = orderdetail.product_count-10
        db.session.add(orderdetail)
        db.session.commit()
        flash("成功减少 10 个！！！", "success")
        break
    return redirect(url_for("shopping_car"))

@app.route("/customer/confirm_order/<int:id>",methods=["POST","GET"])
@login_required
def confirm_order(id):
    if current_user.table_name != "Customer" or \
            Order.query.filter_by(id=id).first().customer_id!=current_user.table_id:
        abort(403)

    address = CustomerDetail.query.filter_by(customer_id=current_user.table_id,is_default=1).first()
    if address is None:
        flash("你还没有设置默认地址，请你去设置默认地址！！！","warning")
        return redirect(url_for("customer_detail_manager",username=current_user.username))
    shopping_car = Order.query.filter_by(id=id).first()

    for detail in shopping_car.orderdetails:
        product = Product.query.filter_by(id=detail.product_id).first()

        if detail.product_count > product.product_count:
            if product.product_count > 0:
                flash("不好意思，刚刚你的货被人给抢走了，没那么多了，请更新你的订单!","warning")
                detail.product_count = 1
                db.session.add(detail)
                db.session.commit()
                return redirect(url_for("shopping_car"))
            else:
                flash("不好意思，刚刚你的货被人给抢走光了，没那么多了，下次早点来吧!", "warning")
                row=detail
                db.session.delete(row)
                db.session.commit()
                return redirect(url_for("shopping_car"))
        else:
            product.product_count = product.product_count-detail.product_count
            db.session.add(product)
            db.session.commit()
        #1 代表付款成功


        #将默认地址设置为 订单的地址
        default = CustomerDetail.query.filter_by(customer_id=current_user.table_id,is_default=1).first()
        order_address = OrderAddress()

        order_address.address = default.address
        order_address.telephone = default.telephone
        order_address.consignee = default.consignee
        order_address.order_id = shopping_car.id
        db.session.add(order_address)


        shopping_car.status = 1
        shopping_car.start_time = datetime.now()
        print(shopping_car.start_time)
        db.session.add(shopping_car)
        db.session.commit()
        return redirect(url_for("shopping_car"))



@app.route("/show_order_details/<int:id>")
@login_required
def show_order_details(id):
    if current_user.table_name == "Customer":
        if Order.query.filter_by(id=id).first().customer_id != current_user.table_id:
            abort(403)

    order_address = OrderAddress.query.filter_by(order_id=id).first()
    order = Order.query.filter_by(id=id).first()
    orderdetails = order.orderdetails
    return render_template("show_order_details.html",order_address=order_address,orderdetails=orderdetails,order=order)




@app.route("/customer/<string:username>/detail/")
@login_required
def customer_detail_manager(username):
    user = Customer.query.filter_by(username=username).first_or_404()
    if user.username != current_user.username:
        abort(403)
    return render_template("coustomer_detail_manager.html")


@app.route("/customer/order_manager")
@login_required
def customer_order_manager():
    return render_template("customer_order_manager.html")

@app.route("/customer/order_manager/order_waitting")
@login_required
def waitting_orders():
    if current_user.table_name != "Customer":
        abort(403)

    # 这里有一个神BUG，我调了半天都没搞定,Order.query.filter_by(customer_id=1,status=完成付款).all()
    # 后来我用了后面的方式，我觉得是我的status的类型的原因，可能中文或者是字符串 就无法比较了吧  所以我
    # 打算重新去设置status的类型
    # 后来我发现 "完成付款 " 和 "完成付款" 是不一样的！！！我多加了一个空格！！
    # 作为字符串他们的长度是不一样的 "完成付款 " == "完成付款" 返回的是False
    # 看到这里的时候 我晕菜了  我本不应该犯这样错误
    # 所以最好还是自己定义宏变量 这样是最好的 这个错误花了我好久啊


    # 1代表付款成功，但尚未发货
    orders = Order.query.filter_by(customer_id=current_user.table_id,status=1).all()

    return render_template("waitting_orders.html",orders=orders)

@app.route("/customer/order_manager/cancel_order/<int:id>")
@login_required
def cancel_orders(id):
    order =Order.query.filter_by(id=id).first()
    if current_user.table_name != "Customer" or order.customer_id != current_user.table_id:
        abort(403)
    if order.status !=1:#确保取消订单之前他的状态确实是付款了，但还没发货的
        flash("订单未被取消！订单已经发货了！","danger")
        return redirect(url_for("waitting_orders"))


    # 把库存换回去，删除订单地址，删除订单
    else:
        details = order.orderdetails
        for detail in details:
            product = Product.query.filter_by(id=detail.product_id).first()
            product.product_count = product.product_count+detail.product_count
            db.session.add(product)
            db.session.commit()
            db.session.delete(detail)
            db.session.commit()

        order_address = OrderAddress.query.filter_by(order_id=id).first()
        db.session.delete(order_address)
        db.session.commit()
        db.session.delete(order)
        db.session.commit()
        flash("您的订单已经取消，退款成功！","success")
        return redirect(url_for("waitting_orders"))



@app.route("/customer/order_manager/order_traning")
@login_required
def traning_orders():
    if current_user.table_name != "Customer":
        abort(403)
    #2代表的成功发货的订单
    orders = Order.query.filter_by(customer_id=current_user.table_id, status=2).all()
    return render_template("traning_orders.html",orders=orders)


@app.route("/customer/order_manager/confirm_order_traning/<int:id>")
@login_required
def confirm_traning_orders(id):
    if current_user.table_name != "Customer":
        abort(403)
    #3代表的成功发货的订单
    order = Order.query.filter_by(id=id).first()
    order.status = 3
    order.end_time = datetime.now()
    db.session.add(order)
    db.session.commit()
    flash("你应经成功收货，欢迎下次继续光临！", "success")
    return redirect(url_for("traning_orders"))



@app.route("/customer/order_manager/order_completed")
@login_required
def completed_orders():
    if current_user.table_name != "Customer":
        abort(403)

    #3代表的收货成功的订单，也就是完成了交易
    orders = Order.query.filter_by(customer_id=current_user.table_id, status=3).all()
    return render_template("completed_orders.html",orders=orders)


@app.route("/customer/detail/new/post/", methods=["GET","POST"])
@login_required
def new_customer_detail():
    if current_user.table_name != "Customer":
        abort(403)
    form = CustomerDetailForm()
    if form.validate_on_submit():
        print(current_user.table_id)
        detail = CustomerDetail(customer_id=current_user.table_id,consignee=form.consignee.data,
                                       telephone=form.telephone.data,address=form.address.data)
        db.session.add(detail)
        db.session.commit()
        flash("添加收获地址成功！", "success")
        return redirect(url_for("customer_detail_manager",username=current_user.username))
    return render_template("new_customer_detail.html", form=form)

@app.route("/customer/detail/show_all")
@login_required
def show_customer_detail():
    if current_user.table_name !="Customer":
        abort(403)

    details = Customer.query.filter_by(id=current_user.table_id).first_or_404().detail

    return render_template("show_customer_detail.html",details=details)

@app.route("/customer/detail/update/<int:id>",methods=["GET","POST"])
@login_required
def update_customer_detail(id):
    if current_user.table_name !="Customer":
        abort(403)
    detail = CustomerDetail.query.filter_by(id=id).first_or_404()

    form = UpdateCustomerDetailForm()
    if form.validate_on_submit():
        detail.consignee = form.consignee.data
        detail.address = form.address.data
        detail.telephone = form.telephone.data
        db.session.commit()
        flash("收获地址更新成功！","success")
        return redirect(url_for("show_customer_detail"))
    elif request.method =="GET":
        form.consignee.data = detail.consignee
        form.address.data = detail.address
        form.telephone.data = detail.telephone
    return render_template("update_customer_detail.html",form=form)

@app.route("/customer/detail/delete/<int:id>")
@login_required
def delete_customer_detail(id):
    if current_user.table_name !="Customer":
        abort(403)
    detail = CustomerDetail.query.filter_by(id=id).first_or_404()
    db.session.delete(detail)
    db.session.commit()
    flash("删除收获地址成功","success")
    return redirect(url_for("show_customer_detail"))

@app.route("/customer/detail/set_default/<int:id>",methods=["GET","POST"])
@login_required
def set_customer_detail_default(id):
    if current_user.table_name != "Customer" or\
            CustomerDetail.query.filter_by(id=id).first_or_404().customer_id != current_user.table_id:
        abort(403)
    detail = CustomerDetail.query.filter_by(customer_id=current_user.table_id, is_default=1).first()
    if detail:
        detail.is_default = 0
        db.session.add(detail)
        db.session.commit()

    detail1 = CustomerDetail.query.filter_by(id=id).first()
    detail1.is_default = 1
    db.session.add(detail1)
    db.session.commit()

    flash("已经更新默认地址！","success")
    return redirect(url_for("show_customer_detail"))






@app.route("/security_check",methods=["GET","POST"])
@login_required
def security_check():

    if current_user.table_name == "Customer":
        form = SecurityCheck()
        if form.validate_on_submit():
            user = Customer.query.filter_by(id=current_user.table_id).first()
            if user and bcrypt.check_password_hash(user.password, form.password.data):
                flash("身份验证成功", "success")
                return redirect(url_for("update_info"))
            else:
                flash("身份验证失败", "warning")
        return render_template("security_check.html", form=form)

    elif current_user.table_name == "Supplier":
        form = SecurityCheck()
        if form.validate_on_submit():
            user = Supplier.query.filter_by(id=current_user.table_id).first()
            if user and bcrypt.check_password_hash(user.password, form.password.data):
                flash("身份验证成功", "success")
                return redirect(url_for("update_info"))
            else:
                flash("身份验证失败", "warning")
        return render_template("security_check.html", form=form)

    elif current_user.table_name == "Crew":
        form = SecurityCheck()
        if form.validate_on_submit():
            user = Crew.query.filter_by(id=current_user.table_id).first()
            if user and bcrypt.check_password_hash(user.password, form.password.data):
                flash("身份验证成功", "success")
                return redirect(url_for("update_info"))
            else:
                flash("身份验证失败", "warning")

        return render_template("security_check.html", form=form)



@app.route("/update/info",methods=["GET","POST"])
@login_required
def update_info():
    if current_user.table_name == "Customer":
        form = UpdateInfo()
        role = Customer.query.filter_by(id=current_user.table_id).first_or_404()
        if form.validate_on_submit():
            role.username = form.username.data
            role.email = form.email.data
            db.session.add(role)
            db.session.commit()

            user = User.query.filter_by(id=current_user.id).first_or_404()
            user.username = form.username.data
            user.email = form.email.data
            db.session.add(user)
            db.session.commit()
            flash('你的邮箱和用户名已经更新了', 'success')
            return redirect(url_for("home"))

        if request.method == "GET":
            form.username.data = role.username
            form.email.data = role.email
        return render_template("update_info.html", form=form)

    elif current_user.table_name == "Crew":
        form = UpdateInfo()
        role = Crew.query.filter_by(id=current_user.table_id).first_or_404()
        if form.validate_on_submit():
            role.username = form.username.data
            role.email = form.email.data
            db.session.add(role)
            db.session.commit()

            user = User.query.filter_by(id=current_user.id).first_or_404()
            user.username = form.username.data
            user.email = form.email.data
            db.session.add(user)
            db.session.commit()
            flash('你的邮箱和用户名已经更新了', 'success')
            return redirect(url_for("home"))


        if request.method == "GET":
            form.username.data = role.username
            form.email.data = role.email
        return render_template("update_info.html", form=form)

    elif current_user.table_name == "Supplier":
        form = UpdateInfo()
        role = Supplier.query.filter_by(id=current_user.table_id).first_or_404()
        if form.validate_on_submit():
            role.username = form.username.data
            role.email = form.email.data
            db.session.add(role)
            db.session.commit()

            user = User.query.filter_by(id=current_user.id).first_or_404()
            user.username = form.username.data
            user.email = form.email.data
            db.session.add(user)
            db.session.commit()
            flash('你的邮箱和用户名已经更新了', 'success')
            return redirect(url_for("home"))


        if request.method == "GET":
            form.username.data = role.username
            form.email.data = role.email
        return render_template("update_info.html", form=form)


@app.route("/update/password",methods=["GET","POST"])
@login_required
def update_password():
    if current_user.table_name == "Customer":
        form = UpdatePasswordForm()
        role = Customer.query.filter_by(id=current_user.table_id).first_or_404()
        if form.validate_on_submit():
            hashed_password = bcrypt.generate_password_hash(password=form.password.data).decode("utf-8")
            role.password = hashed_password
            role.confirm_password = form.confirm_password.data
            db.session.add(role)
            db.session.commit()

            user = User.query.filter_by(id=current_user.id).first_or_404()
            user.password = hashed_password
            user.confirm_password = form.confirm_password.data
            db.session.add(user)
            db.session.commit()
            flash('你的密码已经更新了', 'success')
            return redirect(url_for("home"))


        return render_template("update_password.html", form=form)

    elif current_user.table_name == "Crew":
        form = UpdatePasswordForm()
        role = Crew.query.filter_by(id=current_user.table_id).first_or_404()

        if form.validate_on_submit():
            hashed_password = bcrypt.generate_password_hash(password=form.password.data).decode("utf-8")
            role.password = hashed_password
            role.confirm_password = form.confirm_password.data
            db.session.add(role)
            db.session.commit()

            user = User.query.filter_by(id=current_user.id).first_or_404()
            user.password = hashed_password
            user.confirm_password = form.confirm_password.data
            db.session.add(user)
            db.session.commit()
            flash('你的密码已经更新了', 'success')
            return redirect(url_for("home"))

        return render_template("update_password.html", form=form)

    elif current_user.table_name == "Supplier":
        form = UpdatePasswordForm()
        role = Supplier.query.filter_by(id=current_user.table_id).first_or_404()

        if form.validate_on_submit():
            hashed_password = bcrypt.generate_password_hash(password=form.password.data).decode("utf-8")
            role.password = hashed_password
            role.confirm_password = form.confirm_password.data
            db.session.add(role)
            db.session.commit()

            user = User.query.filter_by(id=current_user.id).first_or_404()
            user.password = hashed_password
            user.confirm_password = form.confirm_password.data
            db.session.add(user)
            db.session.commit()
            flash('你的密码已经更新了', 'success')
            return redirect(url_for("home"))

        return render_template("update_password.html", form=form)

@app.route("/supplier/<string:username>/account")
@login_required
def supplier_account(username):
    if current_user.table_name != "Supplier":
        abort(403)
    supplier = Supplier.query.filter_by(id=current_user.table_id).first_or_404()
    if supplier.supplier_name == "尚未填写":
        flash("请尽快完整你的“商家名称”等信息，完整之后将恢复正常，不用担心！","warning")
        return redirect(url_for("update_supplier_info"))
    return render_template("supplier_account.html", username=username)

@app.route("/supplier/update_info",methods=["GET","POST"])
@login_required
def update_supplier_info():
    if current_user.table_name != "Supplier":
        abort(403)
    form = UpdateSupplierInfoForm()
    supplier = Supplier.query.filter_by(id=current_user.table_id).first_or_404()
    if form.validate_on_submit():
        supplier.telephone = form.telephone.data
        supplier.address = form.address.data
        supplier.supplier_name = form.supplier_name.data
        supplier.mission = form.mission.data
        db.session.add(supplier)
        db.session.commit()
        flash("你的信息更新成功","success")
    elif request.method == "GET":
        form.telephone.data = supplier.telephone
        form.address.data = supplier.address
        form.supplier_name.data = supplier.supplier_name
        form.mission.data = supplier.mission
    return render_template("update_supplier_info.html", form=form)



@app.route("/supplier/crew_manager")
@login_required
def supplier_crew_manager():
    if current_user.table_name != "Supplier":
        abort(403)
    return render_template("supplier_crew_manager.html")

@app.route("/supplier/product_manager")
@login_required
def supplier_product_manager():
    if current_user.table_name != "Supplier":
        abort(403)
    return render_template("supplier_product_manager.html")


@app.route("/supplier/new_product",methods=["GET","POST"])
@login_required
def supplier_new_product():
    if current_user.table_name != "Supplier":
        abort(403)
    form = ProductForm()
    if form.validate_on_submit():
        supplier = Supplier.query.filter_by(id=current_user.table_id).first_or_404()
        product = Product(name=form.name.data,sort=form.sort.data,price=form.price.data,
                          detail=form.detail.data,product_count=form.start_count.data)
        supplier.products.append(product)
        db.session.add(supplier)
        db.session.commit()
        flash("你的商品添加成功", "success")
        return redirect(url_for("show_supplier_product"))
    return render_template("supplier_new_product.html",form=form)


@app.route("/supplier/update_product/<int:id>",methods=["GET","POST"])
@login_required
def supplier_update_product(id):
    if current_user.table_name != "Supplier" or \
            Product.query.filter_by(id=id).first().supplier.first().id != current_user.table_id:
        abort(403)
    form = UpdateProductForm()
    if form.validate_on_submit():
        product = Product.query.filter_by(id = id).first()
        product.name = form.name.data
        product.sort= form.sort.data
        product.price = form.price.data
        product.detail = form.detail.data
        db.session.add(product)
        db.session.commit()
        flash("你的商品更新成功", "success")

    elif request.method == "GET":
        product = Product.query.filter_by(id=id).first_or_404()
        form.name.data = product.name
        form.detail.data = product.detail
        form.price.data = product.price
        form.sort.data = product.sort
        form.detail.data = product.detail

    return render_template("supplier_update_product.html", id=id,form=form)

@app.route("/supplier/delete_product/<int:id>",methods=["POST","GET"])
@login_required
def supplier_delete_product(id):
    if current_user.table_name != "Supplier" or \
            Product.query.filter_by(id=id).first().supplier.first().id != current_user.table_id:
        abort(403)
    product = Product.query.filter_by(id=id).first()
    db.session.delete(product)
    db.session.commit()
    flash("你的商品删除成功！","success")
    return redirect(url_for("show_supplier_product"))

@app.route("/supplier/add_product_count/<int:id>",methods=["POST","GET"])
@login_required
def supplier_add_product_count(id):
    if current_user.table_name != "Supplier" or \
            Product.query.filter_by(id=id).first().supplier.first().id != current_user.table_id:
        abort(403)
    product = Product.query.filter_by(id=id).first()
    form = AddProductCountForm()
    if form.validate_on_submit():
        product.product_count = product.product_count+form.count.data
        db.session.add(product)
        db.session.commit()
        flash("已经成功增加库存", "success")
        return redirect(url_for("show_supplier_product"))
    return render_template("supplier_add_product_count.html",form=form)



@app.route("/supplier/show_product/")
@login_required
def show_supplier_product():
    if current_user.table_name != "Supplier":
        abort(403)
    supplier = Supplier.query.filter_by(id=current_user.table_id).first_or_404()
    products = supplier.products.all()

    return render_template("show_supplier_product.html",products=products)

@app.route("/supplier/delete_crew/<int:id>")
@login_required
def supplier_delete_crew(id):
    crew = Crew.query.filter_by(id = id).first()
    if current_user.table_name != "Supplier" or crew.supplier_id != current_user.table_id:
        abort(403)
    crew.is_employ = 0
    crew.supplier_id = -1
    db.session.add(crew)
    db.session.commit()
    flash("雇员解雇成功！","success")
    return redirect(url_for("show_supplier_crews"))


@app.route("/supplier/show_crews/")
@login_required
def show_supplier_crews():
    if current_user.table_name != "Supplier":
        abort(403)
    supplier = Supplier.query.filter_by(id=current_user.table_id).first_or_404()
    crews = supplier.crews

    return render_template("shou_supplier_crews.html",crews=crews)





@app.route("/crew/<string:username>/account/")
@login_required
def crew_account(username):
    if current_user.table_name != "Crew":
        abort(403)
    crew = Crew.query.filter_by(id=current_user.table_id).first_or_404()
    if crew.crew_name == "尚未填写"or crew.massage == "这个人很懒，什么也没有写。":
        flash("请你先尽快填好你的“正式名称和求职宣言”,更新之后将恢复正常，不用担心", "warning")
        return redirect(url_for("update_crew_info"))

    crew = Crew.query.filter_by(id=current_user.table_id).first()
    supplier = Supplier.query.filter_by(id=crew.supplier_id).first()

    return render_template("crew_account.html", username=username,supplier=supplier,crew=crew)


@app.route("/crew/order_manager")
@login_required
def crew_order_manager():
    if current_user.table_name != "Crew":
        abort(403)
    return render_template("crew_order_manager.html")


@app.route("/crew/order_manager/show_confirm_order_waitting")
@login_required
def show_confirm_waitting_orders():
    if current_user.table_name != "Crew":
        abort(403)
    orders = Order.query.filter_by(status=1).all()

    return render_template("show_confirm_waitting_orders.html", orders=orders)

@app.route("/crew/order_manager/confirm_order_waitting/<int:id>")
@login_required
def confirm_waitting_orders(id):
    if current_user.table_name != "Crew":
        abort(403)
    order = Order.query.filter_by(id=id).first()
    order.status = 2#代表成功发货
    db.session.add(order)
    db.session.commit()
    flash("订单发货成功！","success")
    return redirect(url_for("show_confirm_waitting_orders"))

@app.route("/crew/update_info",methods=["GET","POST"])
@login_required
def update_crew_info():
    if current_user.table_name != "Crew":
        abort(403)
    form = UpdateCrewInfoForm()
    crew = Crew.query.filter_by(id=current_user.table_id).first_or_404()
    if form.validate_on_submit():
        crew.telephone = form.telephone.data
        crew.address = form.address.data
        crew.crew_name = form.crew_name.data
        crew.massage = form.massage.data
        db.session.add(crew)
        db.session.commit()
        flash("你的信息更新成功","success")
    elif request.method == "GET":
        form.telephone.data = crew.telephone
        form.address.data = crew.address
        form.crew_name.data = crew.crew_name
        form.massage.data = crew.massage
    return render_template("update_crew_info.html", form=form)

@app.route("/supplier/<int:id>/all_products")
@login_required
def customer_check_supplier_products(id):
    supplier = Supplier.query.filter_by(id=id).first()
    products =supplier.products.all()

    return render_template("customer_check_supplier_products.html",products=products,supplier=supplier)

@app.errorhandler(404)
def page_not_found(e):
    template = '''
        {%% block body %%}
        <div class="center-content error">
        <h1>哇哦，This page doesn't exist.</h1>
        <h3>%s</h3>
        <h3>这里什么都没有呢٩(๑❛ᴗ❛๑)۶</h3>
        </div>
        {%% endblock %%}
        ''' % (request.url)
    return render_template_string(template), 404

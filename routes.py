import os
from flask import Blueprint, render_template, request, flash, redirect, url_for, g, session, current_app
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, FileField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Optional
from werkzeug.utils import secure_filename

from ext import db
from models import Product, User, Comment


class UpdateProfileForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=2, max=50)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("New Password (დატოვე ცარიელი, თუ არ ცვლი)", validators=[Optional(), Length(min=6)])
    country = SelectField("Country", choices=[("GE", "Georgia"), ("US", "USA"), ("FR", "France"), ("IT", "Italy")])
    profile_img = FileField("Update Profile Image")
    submit = SubmitField("მონაცემების განახლება")

# აპლიკაციის ძირითადი ცვლადები
profiles = []
role = "Admin"

main = Blueprint('main', __name__)


@main.route("/")
@main.route("/index")
def index():
    featured_products = Product.query.order_by(Product.id.desc()).limit(3).all()
    return render_template("index.html", products=featured_products)


@main.route("/contact")
def contact():
    return render_template("contact.html", role=role)


@main.route("/perfumes")
def perfumes():
    category_filter = request.args.get('category')

    if category_filter:
        cat_clean = category_filter.strip().lower()

        if cat_clean in ['men', 'male', 'კაცი', 'კაცის']:
            products = Product.query.filter(Product.category.in_(["Male", "male", "კაცი", "Kaci", "Men", "men"])).all()

        elif cat_clean in ['women', 'female', 'woman', 'ქალი', 'ქალის']:
            products = Product.query.filter(Product.category.in_(["Female", "female", "ქალი", "Qali", "Women", "women"])).all()

        elif cat_clean in ['unisex', 'უნისექსი']:
            products = Product.query.filter(Product.category.in_(["Unisex", "unisex", "უნისექსი"])).all()

        else:
            products = Product.query.filter_by(category=category_filter).all()
    else:
        products = Product.query.all()

    return render_template("parfumes.html", products=products, role=role)


@main.route("/create_product", methods=["GET", "POST"])
def create_product():
    if not g.user or not g.user.is_admin:
        flash("ამ გვერდზე წვდომა მხოლოდ ადმინისტრატორს აქვს!", "danger")
        return redirect(url_for("main.index"))

    from forms import ProductForm
    form = ProductForm()

    if form.validate_on_submit():
        new_product = Product(
            name=form.name.data,
            price=form.price.data,
            brand=form.brand.data,
            category=form.category.data,
            description=form.description.data,
            stock=form.stock.data
        )

        if form.img.data:
            image = form.img.data
            filename = secure_filename(image.filename)
            img_location = os.path.join(main.root_path, "static", "images", filename)
            image.save(img_location)
            new_product.image = filename

        db.session.add(new_product)
        db.session.commit()
        flash("პროდუქტი წარმატებით დაემატა! 🚀", "success")
        return redirect(url_for("main.create_product"))

    products = Product.query.all()
    return render_template("create_product.html", form=form, products=products)


@main.route("/edit_product/<int:product_id>", methods=["GET", "POST"])
def edit_product(product_id):
    if not g.user or not g.user.is_admin:
        return redirect(url_for("main.index"))

    product = Product.query.get_or_404(product_id)
    from forms import ProductForm
    form = ProductForm()

    if form.validate_on_submit():
        product.name = form.name.data
        product.price = form.price.data
        product.brand = form.brand.data
        product.category = form.category.data
        product.description = form.description.data
        product.stock = form.stock.data

        if form.img.data:
            image = form.img.data
            filename = secure_filename(image.filename)
            img_location = os.path.join(main.root_path, "static", "images", filename)
            image.save(img_location)
            product.image = filename

        db.session.commit()
        flash("პროდუქტი წარმატებით განახლდა! 📝", "success")
        return redirect(url_for("main.create_product"))

    elif request.method == "GET":
        form.name.data = product.name
        form.price.data = product.price
        form.brand.data = product.brand
        form.category.data = product.category
        form.description.data = product.description
        form.stock.data = product.stock

    return render_template("create_product.html", form=form, edit_mode=True, product=product)


@main.route("/checkout", methods=["POST"])
def checkout():
    cart = session.get("cart", {})
    if not cart:
        flash("კალათა ცარიელია!", "warning")
        return redirect(url_for("main.view_cart"))

    for product_id, quantity in cart.items():
        product = Product.query.get(int(product_id))
        if product:
            if product.stock >= quantity:
                product.stock -= quantity
            else:
                flash(f"სამწუხაროდ, {product.name}-ზე საკმარისი მარაგი არ გვაქვს!", "danger")
                return redirect(url_for("main.view_cart"))

    db.session.commit()
    session.pop("cart", None)
    flash("შეკვეთა წარმატებით დასრულდა! მადლობა! 🛍️🎉", "success")
    return redirect(url_for("main.index"))


@main.route("/delete_product/<int:product_id>", methods=["POST"])
def delete_product(product_id):
    if not g.user or not g.user.is_admin:
        return redirect(url_for("main.index"))

    product_to_delete = Product.query.get_or_404(product_id)

    if product_to_delete.image and product_to_delete.image != "default.png":
        try:
            os.remove(os.path.join(main.root_path, "static", "images", product_to_delete.image))
        except:
            pass

    db.session.delete(product_to_delete)
    db.session.commit()
    flash("პროდუქტი წარმატებით წაიშალა! 🗑️", "info")
    return redirect(url_for("main.create_product"))


@main.route("/register", methods=["GET", "POST"])
def register():
    from forms import RegisterForm
    form = RegisterForm()

    if form.validate_on_submit():
        filename = "default.png"
        if form.profile_img.data:
            image = form.profile_img.data
            filename = secure_filename(image.filename)
            img_location = os.path.join(main.root_path, "static", "images", filename)
            image.save(img_location)

        new_user = User(
            username=form.username.data,
            password=form.password.data,
            gender=form.gender.data,
            birthday=form.birthday.data,
            country=form.country.data,
            image=filename,
            email=form.email.data
        )
        if new_user.username.lower() == 'admin':
            new_user.is_admin = True

        db.session.add(new_user)
        db.session.commit()

        flash("რეგისტრაცია წარმატებით დასრულდა!", "success")
        return redirect(url_for("main.index"))

    return render_template("register.html", form=form)


@main.route("/login", methods=["GET", "POST"])
def login():
    from forms import LoginForm
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user and user.password == form.password.data:
            session["user_id"] = user.id
            flash("წარმატებით შეხვედით სისტემაში!", "success")
            return redirect(url_for("main.index"))
        else:
            flash("არასწორი იუზერნეიმი ან პაროლი!", "danger")

    return render_template("login.html", form=form)


@main.route("/user_page", methods=["GET", "POST"])
def profile():
    if not g.user:
        flash("პროფილის სანახავად გაიარეთ ავტორიზაცია!", "warning")
        return redirect(url_for("main.login"))

    form = UpdateProfileForm()

    if form.validate_on_submit():
        g.user.username = form.username.data
        g.user.email = form.email.data
        g.user.country = form.country.data

        if form.password.data:
            g.user.password = form.password.data

        if form.profile_img.data:
            image = form.profile_img.data
            filename = secure_filename(image.filename)
            img_location = os.path.join(current_app.root_path, "static", "images", filename)
            image.save(img_location)
            g.user.image = filename

        db.session.commit()
        flash("პროფილი წარმატებით განახლდა! ⚡", "success")
        return redirect(url_for("main.profile"))

    elif request.method == "GET":
        form.username.data = g.user.username
        form.email.data = g.user.email
        form.country.data = g.user.country

    return render_template("user_page.html", form=form)


@main.before_app_request
def load_logged_in_user():
    user_id = session.get("user_id")
    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get(user_id)


@main.route("/product/<int:product_id>")
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    reviews = Comment.query.filter_by(product_id=product_id).order_by(Comment.date_posted.desc()).all()

    avg_rating = 0
    if reviews:
        avg_rating = round(sum(r.rating for r in reviews) / len(reviews), 1)

    return render_template("product_detail.html", product=product, reviews=reviews, avg_rating=avg_rating)


@main.route("/product/<int:product_id>/review", methods=["POST"])
def add_review(product_id):
    if not g.user:
        flash("შეფასების დასატოვებლად გაიარეთ ავტორიზაცია!", "warning")
        return redirect(url_for("main.login"))

    rating = request.form.get("rating", type=int)
    comment = request.form.get("comment")

    if not rating or not comment:
        flash("გთხოვთ შეავსოთ ყველა ველი!", "danger")
        return redirect(url_for("main.product_detail", product_id=product_id))

    new_review = Comment(
        rating=rating,
        text=comment,
        user_id=g.user.id,
        product_id=product_id
    )

    db.session.add(new_review)
    db.session.commit()
    flash("თქვენი შეფასება წარმატებით დაემატა! ⭐", "success")
    return redirect(url_for("main.product_detail", product_id=product_id))


@main.route("/logout")
def logout():
    session.pop("user_id", None)
    flash("თქვენ წარმატებით გამოხვედით სისტემიდან!", "info")
    return redirect(url_for("main.index"))


@main.route("/add_to_cart/<int:product_id>", methods=["POST"])
def add_to_cart(product_id):
    product = Product.query.get_or_404(product_id)

    if product.stock <= 0:
        flash(f"სამწუხაროდ, {product.name} მარაგში აღარ არის!", "danger")
        return redirect(request.referrer or url_for("main.perfumes"))

    if "cart" not in session:
        session["cart"] = {}

    cart = session["cart"]
    p_id_str = str(product_id)

    if p_id_str in cart:
        if cart[p_id_str] < product.stock:
            cart[p_id_str] += 1
        else:
            flash(f"ამაზე მეტი {product.name} მარაგში უბრალოდ არ გვაქვს!", "warning")
            return redirect(request.referrer or url_for("main.perfumes"))
    else:
        cart[p_id_str] = 1

    session["cart"] = cart
    session.modified = True

    flash(f"{product.name} დაემატა კალათაში! 🛒", "success")
    return redirect(request.referrer or url_for("main.perfumes"))


@main.route("/cart")
def view_cart():
    cart = session.get("cart", {})
    cart_items = []
    total_price = 0

    for product_id, quantity in cart.items():
        product = Product.query.get(int(product_id))
        if product:
            item_total = product.price * quantity
            total_price += item_total
            cart_items.append({
                "product": product,
                "quantity": quantity,
                "item_total": item_total
            })

    return render_template("cart.html", cart_items=cart_items, total_price=total_price, role=role)


@main.route("/remove_from_cart/<int:product_id>", methods=["POST"])
def remove_from_cart(product_id):
    cart = session.get("cart", {})
    p_id_str = str(product_id)

    if p_id_str in cart:
        del cart[p_id_str]
        session["cart"] = cart
        session.modified = True
        flash("პროდუქტი ამოშლილია კალათიდან!", "info")

    return redirect(url_for("main.view_cart"))


@main.route("/about_us")
def about_us():
    return render_template("about_us.html")


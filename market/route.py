from market import app,db,flash,request,session
from flask import render_template,redirect,url_for
from market.model import Item,User
from market import db
@app.route('/')
def home_page():
    if 'username' in session :
         return redirect(url_for('market_page'))
    return render_template('home.html')

@app.route('/market',methods=['GET','POST'])
def market_page():
    items = Item.query.filter_by(owner=None)
    if 'username' in session :
        current_user_obj = User.query.filter_by(username=session['username']).first()
        budget = current_user_obj.budget
        ownedItems = Item.query.filter_by(owner=current_user_obj.id)
        if request.method == "POST":
            item_id = request.form.get('purchased_item')
            item_obj = Item.query.filter_by(id=item_id).first()
            sold_item_id = request.form.get('sold_item')
            sold_item_obj = Item.query.filter_by(id=sold_item_id).first()
            if item_obj and current_user_obj:
                if current_user_obj.can_purchase(item_obj.price):
                    item_obj.buy(current_user_obj)
                    flash(f"Congratulations! You purchased {item_obj.name}",category='success')
                else:
                    flash(f"You don't have enough money to buy {item_obj.name}",category='danger')
            if sold_item_obj and current_user_obj:
                if current_user_obj.can_sell(sold_item_obj):
                    sold_item_obj.sell(current_user_obj)
                    flash(f'The price {sold_item_obj.price} has been added to your purse')
                else:
                     flash(f'The {sold_item_obj.name} is not in your purchased items')
            return redirect(url_for('market_page'))
            
        return render_template('market.html',items=items,username=session['username'],budget=budget,ownedItems=ownedItems)
    else:
        flash("Please authenticate to access that page",category='error')
        return render_template('login.html')

@app.route('/register',methods=['GET','POST'])
def register_page():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        user = User.query.filter_by(email=email).first()
        
        if user:
            flash('Email already exists',category='error')
            username = User.query.filter_by(username=username).first()
            if username:
                flash('Username already in use please use a different username',category='error')
        elif len(email)<4:
                flash('Email must be greater than 3 characters',category='error')
        elif len(username)<2:
                flash('Username must be at least 2 characters long',category='error')
        elif password1!=password2:
                flash('Both passwords must match',category='error')
        elif len(password1)<6:
                flash('Passord must be at least 6 character long',category='Error')
        else:
            new_User = User(username=username,email=email,password=password1)
            db.session.add(new_User)
            db.session.commit()
            session['username']=username
            flash('Account created!',category='success')
            return redirect(url_for('market_page'))
    return render_template('register.html')

@app.route('/login',methods=['GET','POST'])
def login_page():
    if 'username' in session :
         return redirect(url_for('market_page'))
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password1')
        user = User.query.filter_by(username=username).first()
        if user:
               #now check if password is same
               if user.check_password(password):
                    flash('Logged in Successfuly',category='success')
                    session['username'] = username
                    return redirect(url_for("market_page"))
               else :
                    flash('Wrong password',category='error')
        else:
               flash('No user found',category='error')
    return render_template('login.html')

@app.route('/logout',methods=['GET','POST'])
def logout():
     session.pop('username',None)
     return redirect(url_for('home_page'))
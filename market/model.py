from market import db,bcrypt
class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String[15],nullable=False,unique=True)
    email = db.Column(db.String[20],nullable=False,unique=True)
    password_hash = db.Column(db.String[40],nullable=False)
    budget = db.Column(db.Integer,nullable=False,default=1000)
    items = db.relationship('Item',backref='owned_user',lazy=True)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')
    @password.setter 
    def password(self,plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')
    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)
    def can_purchase(self,prize):
        if self.budget>=prize:
            return True
        return False
    def can_sell(self,item):
        if item in self.items:
            return True
        return False
class Item(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String[10],nullable=False,unique=True)
    barcode = db.Column(db.String[12],nullable=False,unique=True)
    price = db.Column(db.Integer,nullable=False)
    description = db.Column(db.Integer,nullable=False)
    owner = db.Column(db.Integer,db.ForeignKey('user.id'))
    def buy(self,user):
        self.owner = user.id
        user.budget -= self.price
        db.session.commit()
    def sell(self,user):
        self.owner = None
        user.budget += self.price
        db.session.commit()
    def __repr__(self):
        return f'Item {self.name}'
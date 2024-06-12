from market import db, bcrypt, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email_address = db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)
    budget = db.Column(db.Integer(), nullable=False, default=1000)
    items = db.relationship('Item', backref='owned_user', lazy=True)

    @property
    def prettier_budget(self):
        if len(str(self.budget)) >= 4:
            return f'${str(self.budget)[:-3]},{str(self.budget)[-3:]}'
        else:
            return f"${self.budget}"

    @property
    def password(self):
        return self.passord

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)

class Item(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30), nullable=False, unique=True)
    price = db.Column(db.Integer(), nullable=False)
    barcode = db.Column(db.String(length=12), nullable=False, unique=True)
    description = db.Column(db.String(length=1024), nullable=False, unique=True)
    owner = db.Column(db.Integer(), db.ForeignKey('user.id'))

    def __repr__(self):
        return f'Item {self.name}'

# to add items in the CMD:
# > python
# >>> from market import db
# >>> app.app_context().push()
# >>> db.create_all()
# >>> from market import Item
# >>> item1 = Item(name="IPhone 10", price=500, barcode='846154104831', description='desc')
# >>> db.session.add(item1)
# >>> db.session.commit()
# >>> item2 = Item(name="Laptop", price=600, barcode='321912987542', description='description')
# >>> db.session.add(item2)
# >>> db.session.commit()

# to check items in the CMD:
# >>> Item.query.all()
# or using following command:
# >>> for item in Item.query.all():
# ...   item.name
# ...   item.price
# ...   item.description
# ...   item.id
# ...   item.barcode

# to check items by using filter:
# >>> for item in Item.query.filter_by(price=500):
# ...   item.name

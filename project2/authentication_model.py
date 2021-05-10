from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager
from flask import session

database = SQLAlchemy()
login = LoginManager()

class UserModel(UserMixin, database.Model):
    __tablename__ = 'accounts'

    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String(50), nullable=False)
    email = database.Column(database.String(50), nullable=False)
    age = database.Column(database.Integer, nullable=False)
    gender = database.Column(database.String(10), nullable=False)
    city = database.Column(database.String(30), nullable=False)
    password = database.Column(database.String(255), nullable=False)
    profile_name = database.Column(database.String(100), nullable=False)

    @staticmethod
    def set_password(password):
        return generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

class DoctorModel(UserMixin, database.Model):
    __tablename__ = 'docaccounts'

    id = database.Column(database.Integer, primary_key=True)
    email = database.Column(database.String(50), nullable=False)
    password = database.Column(database.String(255), nullable=False)
    name = database.Column(database.String(100), nullable=False)
    mobile = database.Column(database.String(12), nullable=False)
    address = database.Column(database.String(255), nullable=False)
    specialization = database.Column(database.String(100), nullable=False)
    city = database.Column(database.String(50), nullable=False)
    profile_name = database.Column(database.String(50), nullable=False)

    @staticmethod
    def set_password(password):
        return generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

class AdminModel(UserMixin, database.Model):
    __tablename__ = 'AdminAccounts'

    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String(50), nullable=False)
    email = database.Column(database.String(50), nullable=False)
    age = database.Column(database.Integer, nullable=False)
    gender = database.Column(database.String(10), nullable=False)
    password = database.Column(database.String(255), nullable=False)
    profile_name = database.Column(database.String(100), nullable=False)

    @staticmethod
    def set_password(password):
        return generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

class AcceptConsultancy(UserMixin, database.Model):
    __tablename__ = 'consultancy'

    id = database.Column(database.Integer, primary_key=True)
    doctor_name = database.Column(database.String(100), nullable=False)
    username = database.Column(database.String(50), nullable=False)
    diseaseName = database.Column(database.String(50), nullable=False)
    appointmentDateTime = database.Column(database.DateTime, nullable=False)
    status = database.Column(database.String(50), nullable=False)

@login.user_loader
def load_user(id):
    currentUser = session.get("current_user")
    if currentUser == 'doctor':
        return DoctorModel.query.get(int(id))
    elif currentUser == 'patient':
        return UserModel.query.get(int(id))

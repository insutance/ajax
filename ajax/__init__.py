import os
from flask import Flask, render_template, url_for, jsonify, request
app = Flask(__name__)
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate       # DB
import simplejson as json

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:1234@127.0.0.1:3306/user'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = b'aaa!111/'    # session 사용하려면 필요
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.String(30), primary_key=True)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    pub_time = db.Column(db.DateTime())

    def get_json(self):
        return dict(
            id = self.id,
            password = self.password,
            email = self.email,
            pub_date = self.pub_time
        )

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ajax', methods=['GET','POST'])
def ajax():
    if request.method=='GET':
        user = User.query.all()
        return render_template('index.html', users=user)
    
    else:
        data = request.get_json()
        
        user_data = User(id=data['id'], password=data['password'], email=data['email'], pub_time=datetime.now())
        db.session.add(user_data)
        db.session.commit()

        users = User.query.all()
        data_list = []
        for user in users:
            data_list.append(user.get_json())
        
        print(data_list)
        return jsonify(result="success", result2=data_list)

@app.route('/post', methods=['GET','POST'])
def post():
    if request.method=='GET':
        user = User.query.all()
        return render_template('post.html', users=user)

    else:
        pk = request.get_json()
        print(pk)

        data = User.query.filter_by(id=pk['id']).first()
        db.session.delete(data)
        db.session.commit()

        users = User.query.all()
        data_list = []
        for user in users:
            data_list.append(user.get_json())
        
        return jsonify(result="success", result2=data_list)

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///finance.db'
db = SQLAlchemy(app)

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(10))
    category = db.Column(db.String(50))
    amount = db.Column(db.Float)
    date = db.Column(db.DateTime, default=datetime.utcnow)

db.create_all()

@app.route('/add', methods=['POST'])
def add_transaction():
    data = request.json
    new_transaction = Transaction(
        type=data['type'],
        category=data['category'],
        amount=data['amount'],
        date=datetime.strptime(data['date'], '%Y-%m-%dT%H:%M:%S')
    )
    db.session.add(new_transaction)
    db.session.commit()
    return jsonify({'message': 'Transaction added!'})

@app.route('/transactions', methods=['GET'])
def get_transactions():
    transactions = Transaction.query.all()
    return jsonify([{
        'type': t.type,
        'category': t.category,
        'amount': t.amount,
        'date': t.date.isoformat()
    } for t in transactions])

if __name__ == '__main__':
    app.run(debug=True)

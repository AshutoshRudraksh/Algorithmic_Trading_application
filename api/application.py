from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'

db = SQLAlchemy(app)


# to run the flask app you need to create some variable each time you blank out of the app or terminal 
# $ export FLASK_APP=application.py
# $ export FLASK_ENV=development
# $ flask run
# $ crtl+c - to kill the running server

# For database model setup for SQLAlchemy
class Drink(db.Model):
    # Creating 3 columns (id, name, description)
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(120))

    # Overwrite the repr method
    def __repr__(self):
        return f"{self.name} - {self.description}"

@app.route('/')
def index():
	print('Index route access successful!')
	return 'Hello!'

@app.route('/drinks', methods=['GET'])
def list_drinks():
    drinks = Drink.query.all()
    output = []
    for drink in drinks:
        drink_data = {'id': drink.id, 'name': drink.name, 'description': drink.description}
        output.append(drink_data)
    return jsonify({"drinks": output})

@app.route('/drinks/<int:id>', methods=['GET'])
def get_drink(id):
    drink = Drink.query.get_or_404(id)
    return jsonify({'name': drink.name, 'description': drink.description})

@app.route('/add_drink', methods=['POST'])
def add_drink():
    data = request.get_json()
    print(f"Received data: {data}")
    if not data or 'name' not in data or 'description' not in data:
        return jsonify({'error': 'Name and description are required'}), 400

    new_drink = Drink(name=data['name'], description=data['description'])
    db.session.add(new_drink)
    db.session.commit()
    return jsonify({'message': 'Drink added successfully!'}), 201

@app.route('/drinks/<int:id>', methods=['DELETE'])
def delete_drink(id):
	drink = Drink.query.get_or_404(id)
	if drink is None:
		return {"error": "not found"}
	db.session.delete(drink)
	db.session.commit()
	return {"message": "Deleted!@"}

if __name__ == '__main__':
    app.run(debug=True)

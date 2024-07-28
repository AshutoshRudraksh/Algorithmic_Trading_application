from flask import Flask
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'

db = SQLAlchemy(app)





# for database model setup for SQLAlchemy
class Drink(db.Model): # inherting from db.model which has all the functionality we need
	# creating 3 columns (id,name,description)
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(80), unique=True, nullable=False)
	description = db.Column(db.String(120))

	# overwrite the repr method
	def __repr__(self):
		return f"{self.name} -{self.description}"

# to run the flask app you need to create some variable each time you blank out of the app or terminal 
# $ export FLASK_APP=application.py
# $ export FLASK_ENV=development
# $ flask run
# $ crtl+c - to kill the running server

@app.route('/')
def index():
    print("Index route accessed")
    return 'Hello!' 

@app.route('/drinks')
def list_drinks():
	drinks = Drink.query.all()
	output = []
	for drink in drinks:
		drink_data = {'id': drink.id, 'name':drink.name, 'description': drink.description}
		output.append(drink_data)
	return {"drinks": output}

@app.route('/drinks/<int:id>')
def get_drinks(id):
	drink = Drink.query.get_or_404(id)
	return ({'name': drink.name})

@app.route('/check_db')
def check_db():
    drinks = Drink.query.all()
    return f"Found {len(drinks)} drinks in the database."

@app.route('/add_drink', methods=['POST'])
def add_drink():
	data = request.get_json()
	if not data or 'name' not in data or 'description' not in data:
		return jsonify({'error': 'Nmae and description are required'}), 400
	new_drink = Drink(name=data['name'], description=data['description'])
	db.session.add(new_drink)
	db.session.commit()
	return jsonify({'message': 'Drink added successfully!'}), 201

if __name__ == '__main__':
    app.run(debug=True)

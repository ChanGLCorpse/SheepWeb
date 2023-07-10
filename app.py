from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////../my_database.db'
db = SQLAlchemy(app)

class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.Text)
    temperature = db.Column(db.Float)
    humidity = db.Column(db.Float)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        date = request.form['date']
        data = Data.query.filter(Data.timestamp.contains(date)).all()
    else:
        yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        data = Data.query.filter(Data.timestamp.contains(yesterday)).all()

    return render_template('index.html', data=data)

@app.route('/upload', methods=['POST'])
def upload():
    try:
        data = request.get_json()

        new_data = Data(
            timestamp=data['timestamp'],
            temperature=data['temperature'],
            humidity=data['humidity']
        )

        db.session.add(new_data)
        db.session.commit()

        return jsonify({'message': 'Data uploaded successfully'}), 200
    except:
        return jsonify({'message': 'An error occurred during the upload'}), 400

if __name__ == '__main__':
    app.run(debug=True)

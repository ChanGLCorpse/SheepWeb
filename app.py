from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////root/sqliteServer/sheep.db'
db = SQLAlchemy(app)

class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.String(50), nullable=False)
    temperature = db.Column(db.Float, nullable=False)
    humidity = db.Column(db.Float, nullable=False)

@app.route('/', methods=['GET'])
def index():
    date_query = request.args.get('date', default=datetime.now().date(), type=str)
    data_list = Data.query.filter(Data.timestamp.like(f'%{date_query}%')).all()
    return render_template('index.html', date=date_query, data_list=data_list)

@app.route('/upload', methods=['POST'])
def upload():
    timestamp = request.form.get('timestamp')
    temperature = float(request.form.get('temperature'))
    humidity = float(request.form.get('humidity'))
    data = Data(timestamp=timestamp, temperature=temperature, humidity=humidity)
    db.session.add(data)
    db.session.commit()
    return 'Data added successfully'

if __name__ == "__main__":
    app.run(debug=True)

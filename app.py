import flask
from flask import redirect
from flask_sqlalchemy import SQLAlchemy

app = flask.Flask(__name__, static_folder='static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(512), nullable=False)
    number = db.Column(db.String(512), nullable=False)

    def __repr__(self):
        return f'Contact {self.name}'


@app.route('/', methods=['GET', 'POST'])
def main():
    return flask.redirect(flask.url_for('index'))


@app.route('/add', methods=['GET', 'POST'])
def index():
    if flask.request.method == 'POST':
        name = flask.request.form['name']
        number = flask.request.form['number']
        contact = Contact(name=name, number=number)
        db.session.add(contact)
        db.session.commit()
    contacts = Contact.query.all()
    return flask.render_template('index.html', contacts=contacts)


# app.py

@app.route('/clear', methods=['POST'])
def clear():
    db.session.query(Contact).delete()
    db.session.commit()
    return redirect('/')


with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run()

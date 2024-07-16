from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///forexapp.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class ForexSch(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    currency = db.Column(db.String(200), nullable=False)
    lot_size = db.Column(db.Float(3), default=0.5)
    stop_loss = db.Column(db.Integer, default=10)
    trailing_stop = db.Column(db.Integer, default=10)
    trigger_stop = db.Column(db.Integer, default=10)
    pip_difference = db.Column(db.Integer, default=15)
    comments = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, default=0)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    modified_date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<News Subcriptions %r>' % self.id


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        # perform required POST actions
        print("form data :",request.form)
        name = request.form['name']
        date_str = request.form['date']
        currency = request.form['pair']
        lotsize = request.form['lotsize']
        comments = request.form['comment']
        stoploss = request.form['stoploss']
        trailingstop = request.form['trailingstop']
        triggerstop = request.form['triggerstop']
        pipdiff = request.form['pipdiff']

        date = datetime.strptime(date_str, '%Y-%m-%dT%H:%M')
        subscription = ForexSch(name=name, date=date, currency=currency, lot_size=lotsize, stop_loss=stoploss,
                                trailing_stop=trailingstop, trigger_stop=triggerstop, pip_difference=pipdiff,
                                comments=comments)
        print("performing POST request", subscription)
        try:
            db.session.add(subscription)
            db.session.commit()
            return redirect('/')
        except Exception as e:
            print(e)
            return 'Subscription addition failed: {}'.format(e)
    else:
        subscriptions = ForexSch.query.order_by(ForexSch.created_date).all()
        return render_template('index.html', subscriptions=subscriptions)


@app.route('/delete/<int:id>')
def delete(id):
    delete_sub = ForexSch.query.get_or_404(id)
    try:
        db.session.delete(delete_sub)
        db.session.commit()
        return redirect('/')
    except Exception as e:
        print(e)
        return 'Subscription deletion failed: {}'.format(e)


@app.route('/update/<int:id>', methods=['POST', 'GET'])
def update(id):
    subscription = ForexSch.query.get_or_404(id)
    if request.method == 'POST':
        print('Updating subscription')
        subscription.name = request.form['name']
        subscription.date = datetime.strptime(request.form['date'], '%Y-%m-%dT%H:%M')
        subscription.currency = request.form['pair']
        subscription.lot_size = request.form['lotsize']
        subscription.comments = request.form['comment']
        subscription.stop_loss = request.form['stoploss']
        subscription.trailing_stop = request.form['trailingstop']
        subscription.trigger_stop = request.form['triggerstop']
        subscription.pip_difference = request.form['pipdiff']

        try:
            db.session.commit()
            return redirect('/')
        except Exception as e:
            print(e)
            return 'Subscription update failed: {}'.format(e)
    else:
        return render_template('update.html', subscription=subscription)


if __name__ == "__main__":
    app.run(debug=True)

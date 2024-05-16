from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages')
def messages():
    return [msg.to_dict() for msg in Message.query.all()]

@app.route('/messages/<int:id>')
def messages_by_id(id):
    return Message.query.where(Message.id == id).first().to_dict()

@app.post('/messages')
def post_msg():
    msg = Message(
        body=request.json['body'],
        username=request.json['username']
    )
    db.session.add(msg)
    db.session.commit()
    return msg.to_dict()

@app.patch('/messages/<int:id>')
def patch_msg(id):
    msg = Message.query.where(Message.id == id).first()
    if msg:
        for key in request.json.keys():
            setattr(msg, key, request.json[key])
        db.session.add(msg)
        db.session.commit()
        return msg.to_dict(), 202
    else:
        return {'error': 'Not found'}, 404

@app.delete('/messages/<int:id>')
def delete_msg(id):
    msg = Message.query.where(Message.id == id).first()
    if msg:
        db.session.delete(msg)
        db.session.commit()
        return {}, 204
    else:
        return {'error': 'Not found'}, 404

if __name__ == '__main__':
    app.run(port=5555)

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

@app.get('/messages')
def get_messages():
    messages = [m.to_dict() for m in Message.query.order_by(Message.created_at).all()]
    return messages, 200

@app.post('/messages')
def post_messages():
    new_msg = Message(
        body =  request.json.get("body"),
        username = request.json.get('username')
    )
    db.session.add(new_msg)
    db.session.commit()

    return new_msg.to_dict(), 201




@app.patch('/messages/<int:id>')
def patch_messages_by_id(id):
    msg_to_patch= Message.query.where(Message.id ==id).first()
    if msg_to_patch:
        for key in request.json.keys():
            if not key == 'id':
                setattr(msg_to_patch, key, request.json[key])
        db.session.add(msg_to_patch)
        db.session.commit()
        return msg_to_patch.to_dict(), 202
    else:
        return {'error' : "Not Found"}, 404 
    
@app.delete("/messages/<int:id>")
def delete_message(id):
    msg_to_delete= Message.query.where(Message.id == id).first()
    if msg_to_delete :
        db.session.delete(msg_to_delete)
        db.session.commit()
        return {}, 204
    else:
        return {"error" : "Not Found"}, 404

    

if __name__ == '__main__':
    app.run(port=5555)

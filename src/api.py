from flask import Flask, request, jsonify, abort, send_from_directory
import os
from .database.models import db, setup_db, User, Voice, Like, Picture
from flask_migrate import Migrate
from flask_cors import CORS
from datetime import datetime
from .auth.auth import AuthError, requires_auth

VOICES_PER_PAGE = 10


app = Flask(__name__,  static_folder='public', static_url_path='')
cors = CORS(app, resources={r"*": {"origins": "http://localhost:3000"}})
setup_db(app)
migrate=Migrate(app, db)


@app.route('/static/<path:path>')
def send_js(path):
    return send_from_directory('public/static', path)

# user  
@app.route('/users', methods=['POST'])
def create_user():
    data = request.json
    auth0_user_id = data['auth0_user_id']
    nickname = data['nickname']
    picture_url = data['picture_url']

    user = User.query.filter_by(auth0_user_id=auth0_user_id).one_or_none()
    if user is not None:
        return jsonify({
                'success':True,
                'msg':'already have this user',
                'user':user.format()
            })

    user = User(auth0_user_id=auth0_user_id, nickname=nickname, picture_url=picture_url, create_time=datetime.now())
    formated_user = user.insert()
    return jsonify({
            'success':True,
            'user':formated_user
        })

@app.route('/users/<user_id>', methods=['PATCH'])
def update_user(user_id):
    data = request.json

    user = User.query.get(user_id)
    for key, value in data.items():
        setattr(user, key, value)

    formated_user = user.update()
    return jsonify({
            'success':True,
            'user':formated_user
        })


@app.route('/users/<user_id>',methods=['DELETE'])
def delete_user(user_id):
    data = request.json

    user = User.query.get(user_id)
    deleted = user.delete()

    return jsonify({
            'success':True,
            'deleted':deleted
        })

# voice
@app.route('/voices')
def get_voices_by_page():
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', VOICES_PER_PAGE, type=int)
    start = (page - 1)*page_size
    end = page*page_size

    voices_query = Voice.query.order_by(db.desc(Voice.create_time))
    voices_slice = voices_query.slice(start, end).all()
    return jsonify({
            'success':True,
            'page':page,
            'total':voices_query.count(),
            'voices':list(voice.format() for voice in voices_slice)
        })


@app.route('/voices', methods=['POST'])
@requires_auth(permission='create:voice')
def create_voice(payload):
    data = request.json

    voice = Voice(text=data['text'], author_id=data['author_id'], replying_to=data.get('replying_to', None), create_time=datetime.now())
    pictures = []
    if data.get('pictures', None):
        for picture_url in data['pictures']:
            picture = Picture(url=picture_url)
            pictures.append(picture)
            voice.pictures.append(picture)

    formated_voice = voice.insert(*pictures)
    return jsonify({
            'success':True,
            'voice':formated_voice
        })



@app.route('/voices/<voice_id>', methods=['DELETE'])
def delete_voice(voice_id):
    data = request.json

    voice = Voice.query.get(voice_id)

    deleted = voice.delete()

    return jsonify({
            'success':True,
            'deleted':deleted
        })


@app.route('/voices/<voice_id>/like', methods=['POST'])
@requires_auth(permission='like:voice')
def like_toggle(payload, voice_id):
    data = request.json
    user_id = data['user_id']
    like = Like.query.filter_by(voice_id=voice_id, user_id=user_id).one_or_none()
    formated = None
    if like is None:
        like = Like(voice_id=voice_id, user_id=user_id, like=True)
        formated = like.insert()
        res_like = True
    else :
        like.delete()
        res_like = False

    return jsonify({
            'success':True,
            'like':formated
        })

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return app.send_static_file('index.html')

## Error Handling
@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
                    "success": False, 
                    "error": 422,
                    "message": "Unprocessable"
                    }), 422

@app.errorhandler(404)
def unprocessable(error):
    return jsonify({
                    "success": False, 
                    "error": 404,
                    "message": "Not Found"
                    }), 404

@app.errorhandler(400)
def unprocessable(error):
    return jsonify({
                    "success": False, 
                    "error": 400,
                    "message": "Bad Request"
                    }), 400

@app.errorhandler(AuthError)
def handle_auth_error(ex):
    response = jsonify({
            'error':ex.error,
            'description':ex.description,
            'code':ex.status_code
        })
    response.status_code = ex.status_code
    return response


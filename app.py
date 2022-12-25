from flask import Flask, request, abort

from line_bot_api import *
from extensions import db, migrate
from models.user import User
from events.basic import about_us_event, location_event
from events.service import *


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://admin:Dodo910118@localhost:5432/myProject'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.app = app
db.init_app(app)
migrate.init_app(app, db)

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message_text = str(event.message.text).lower()
    user = User.query.filter(User.line_id == event.source.user_id).first()

    if not user:
        profile = line_bot_api.get_profile(event.source.user_id)
        user = User(profile.user_id, profile.display_name, profile.picture_url)
        db.session.add(user)
        db.session.commit()

    if message_text == '關於':
        about_us_event(event)
    elif message_text == '地點':
        location_event(event)
    elif message_text == '預約':
        book_event(event)

@handler.add(PostbackEvent)
def handle_postback(event):
    data = dict(parse_qsl(event.postback.data))
    if data.get('action') == 'buy':
        service_event(event)
    elif data.get('action') == 'select_date':
        service_select_event(event)
    elif data.get('action') == 'select_time':
        service_select_time_event(event)
    elif data.get('action') == 'confirm':
        confirm_event(event)
    elif data.get('action') == 'confirmed':
        service_confirmed_event(event)
    elif data.get('action') == 'notconfirmed':
        service_notconfirmed_event(event)
    elif data.get('action') == 'book':
        service_category_event(event)
    elif data.get('action') == 'cancel':
        service_category_event(event)
    print('action:', data.get('action'))
    print('itemid:', data.get('itemid'))
    print('service:', data.get('service_id'))
    print('date:', data.get('date'))
    print('time:', data.get('time'))

if __name__ == "__main__":
    app.run()
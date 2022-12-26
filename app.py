from flask import Flask, request, abort

from line_bot_api import *
from extensions import db, migrate
from models.user import User
from events.basic import about_us_event, location_event, talk_event
from events.service import *
from events.admin import *
from fsm import FSMModel


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://admin:Dodo910118@localhost:5432/myProject'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.app = app
db.init_app(app)
migrate.init_app(app, db)

state=['default', 'about', 'location', 'book', 'admin', 'talk', 'category', 'service', 'date', 'time', 'confirm', 'confirmed', 'cancel', 'canceled']


machine = FSMModel(
    states=state,
    transitions=[
        {'trigger': 'state_about_us', 'source': ['default', 'location', 'book', 'admin', 'talk', 'category', 'service', 'date', 'time', 'confirm', 'confirmed', 'cancel', 'canceled'], 'dest': 'about', 'conditions': 'state_about_us'},
        {'trigger': 'state_location', 'source': ['default', 'about', 'book', 'admin', 'talk', 'category', 'service', 'date', 'time', 'confirm', 'confirmed', 'cancel', 'canceled'], 'dest': 'location', 'conditions': 'state_location'},
        {'trigger': 'state_book', 'source': ['default', 'about', 'location', 'admin', 'talk', 'category', 'service', 'date', 'time', 'confirm', 'confirmed', 'cancel', 'canceled'], 'dest': 'book', 'conditions': 'state_book'},
        {'trigger': 'state_admin', 'source': ['default', 'about', 'location', 'book', 'talk', 'category', 'service', 'date', 'time', 'confirm', 'confirmed', 'cancel', 'canceled'], 'dest': 'admin', 'conditions': 'state_admin'},
        {'trigger': 'state_talk', 'source': ['default', 'about', 'location', 'book', 'admin', 'category', 'service', 'date', 'time', 'confirm', 'confirmed', 'cancel', 'canceled'], 'dest': 'talk', 'conditions': 'state_talk'},
        {'trigger': 'state_category', 'source': ['default', 'about', 'location', 'book', 'admin', 'talk', 'service', 'date', 'time', 'confirm', 'confirmed', 'cancel', 'canceled'], 'dest': 'category', 'conditions': 'state_category'},
        {'trigger': 'state_service', 'source': ['default', 'about', 'location', 'book', 'admin', 'talk', 'category', 'date', 'time', 'confirm', 'confirmed', 'cancel', 'canceled'], 'dest': 'service', 'conditions': 'state_service'},
        {'trigger': 'state_date', 'source': ['default', 'about', 'location', 'book', 'admin', 'talk', 'category', 'service', 'time', 'confirm', 'confirmed', 'cancel', 'canceled'], 'dest': 'date', 'conditions': 'state_date'},
        {'trigger': 'state_time', 'source': ['default', 'about', 'location', 'book', 'admin', 'talk', 'category', 'service', 'date', 'confirm', 'confirmed', 'cancel', 'canceled'], 'dest': 'time', 'conditions': 'state_time'},
        {'trigger': 'state_confirm', 'source': ['default', 'about', 'location', 'book', 'admin', 'talk', 'category', 'service', 'date', 'time', 'confirmed', 'cancel', 'canceled'], 'dest': 'confirm', 'conditions': 'state_confirm'},
        {'trigger': 'state_confirmed', 'source': ['default', 'about', 'location', 'book', 'admin', 'talk', 'category', 'service', 'date', 'time', 'confirm', 'cancel', 'canceled'], 'dest': 'confirm', 'conditions': 'state_confirmed'},
        {'trigger': 'state_notconfrim', 'source': ['default', 'about', 'location', 'book', 'admin', 'talk', 'category', 'service', 'date', 'time', 'confirm', 'confirmed', 'cancel', 'canceled'], 'dest': 'default', 'conditions': 'state_notconfrim'},
        {'trigger': 'state_cancel', 'source': ['default', 'about', 'location', 'book', 'admin', 'talk', 'category', 'service', 'date', 'time', 'confirm', 'confirmed', 'canceled'], 'dest': 'cancel', 'conditions': 'state_cancel'},
        {'trigger': 'state_canceled', 'source': ['default', 'about', 'location', 'book', 'admin', 'talk', 'category', 'service', 'date', 'time', 'confirm', 'confirmed', 'cancel'], 'dest': 'canceled', 'conditions': 'state_canceled'},
    ],
    initial='default',
    show_conditions=True,
    use_pygraphviz=False
)

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

    if message_text == '使用說明':
        about_us_event(event)
        machine.state_about_us()
    elif message_text == '地點在哪裡呢?':
        location_event(event)
        machine.state_location()
    elif message_text == '進入預約系統':
        book_event(event, user)
        machine.state_book()
    elif message_text == '有沒有真人可以跟我洽談?':
        talk_event(event)
        machine.state_talk()

    elif message_text.startswith('*'):
        if event.source.user_id not in ['Uca7fb7fa191686c0c10d472389180d27']:
            return
        if message_text in ['*預約名單']:
            list_reservation_event(event)
            machine.state_admin()

@handler.add(PostbackEvent)
def handle_postback(event):
    data = dict(parse_qsl(event.postback.data))
    user = User.query.filter(User.line_id == event.source.user_id).first()
    if data.get('action') == 'buy':
        service_event(event)
        machine.state_service()
    elif data.get('action') == 'select_date':
        service_select_event(event)
        machine.state_date()
    elif data.get('action') == 'select_time':
        service_select_time_event(event)
        machine.state_time()
    elif data.get('action') == 'confirm':
        confirm_event(event)
        machine.state_confirm()
    elif data.get('action') == 'confirmed':
        service_confirmed_event(event, user)
        machine.state_confirmed()
    elif data.get('action') == 'notconfirmed':
        service_notconfirmed_event(event)
        machine.state_notconfirmed()
    elif data.get('action') == 'book':
        service_category_event(event)
        machine.state_category()
    elif data.get('action') == 'cancel':
        cancel_event(event, user)
        machine.state_cancel()
    elif data.get('action') == 'canceled':
        canceled_event(event, user)
        machine.state_canceled()

def CreateFSM():
    with open('.' + machine.fsm_filename, 'bw') as f:
        machine.get_graph().draw(f, format="png", prog='dot')

if __name__ == "__main__":
    CreateFSM()
    app.run()
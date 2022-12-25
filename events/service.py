import datetime
from line_bot_api import *
from urllib.parse import parse_qsl
from extensions import db
from models.user import User
from models.Reservation import Reservation

services = {
    1: {
        'itemid': '1',
        'img_url': 'https://picsum.photos/201',
        'title': '測試標題一a',
        'duration': '內容一a',
        'post_url': 'https://linecorp.com'
    },
    2: {
        'itemid': '1',
        'img_url': 'https://picsum.photos/301',
        'title': '測試標題一b',
        'duration': '內容一b',
        'post_url': 'https://linecorp.com'
    },
    3: {
        'itemid': '2',
        'img_url': 'https://picsum.photos/201',
        'title': '測試標題二a',
        'duration': '內容二a',
        'post_url': 'https://linecorp.com'
    },
    4: {
        'itemid': '2',
        'img_url': 'https://picsum.photos/301',
        'title': '測試標題二b',
        'duration': '內容二b',
        'post_url': 'https://linecorp.com'
    },
}

def book_or_not(event, user):
    reservation = Reservation.query.filter(Reservation.user_id == user.id,
                                          Reservation.is_canceled == False,
                                          Reservation.booking_datetime > datetime.datetime.now())
    return reservation


def book_event(event, user):

    confirm_template_message = TemplateSendMessage(
        alt_text='Confirm template',
        template=ConfirmTemplate(
            text='您好，' + user.display_name + '先生/小姐' + 
            '\n請問您是想預約還是取消預約呢?',
            actions=[
                PostbackAction(
                    label='預約',
                    display_text='我想預約參與活動!!',
                    data='action=book'
                ),
                PostbackAction(
                    label='取消預約',
                    text='我想取消現有的預約',
                    data='action=cancel'
                )
            ]
        )
    )
    line_bot_api.reply_message(
        event.reply_token,
        [confirm_template_message])

def service_category_event(event):
    image_carousel_template_message = TemplateSendMessage(
        alt_text='ImageCarousel template',
        template=ImageCarouselTemplate(
            columns=[
                ImageCarouselColumn(
                    image_url='https://picsum.photos/200',
                    action=PostbackAction(
                        label='活動類別1',
                        display_text='我想預約活動類別1',
                        data='action=buy&itemid=1'
                    )
                ),
                ImageCarouselColumn(
                    image_url='https://picsum.photos/300',
                    action=PostbackAction(
                        label='活動類別2',
                        display_text='我想預約活動類別2',
                        data='action=buy&itemid=2'
                    )
                ),
                ImageCarouselColumn(
                    image_url='https://picsum.photos/100',
                    action=PostbackAction(
                        label='取消',
                        display_text='取消',
                        data='action=notconfirmed'
                    )
                )
            ]
        )
    )
    line_bot_api.reply_message(
        event.reply_token,
        [TextSendMessage(text='請選擇您想參與的活動類別'), image_carousel_template_message])

def service_event(event):
    data = dict(parse_qsl(event.postback.data))
    bubbles = []
    for service_id in services:
        if services[service_id]['itemid'] == data['itemid']:
            service = services[service_id]
            bubble={
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                {
                    "type": "image",
                    "url": service['img_url'],
                    "size": "full",
                    "aspectMode": "cover",
                    "aspectRatio": "2:3",
                    "gravity": "top"
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                        {
                            "type": "text",
                            "text": service['title'],
                            "size": "xl",
                            "color": "#ffffff",
                            "weight": "bold"
                        }
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "baseline",
                        "contents": [
                        {
                            "type": "text",
                            "text": service['duration'],
                            "color": "#ebebeb",
                            "size": "sm",
                            "flex": 0
                        }
                        ],
                        "spacing": "lg"
                    },
                    
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                        {
                            "type": "filler"
                        },
                        {
                            "type": "box",
                            "layout": "baseline",
                            "contents": [
                                {
                                    "type": "filler"
                                },
                                {
                                    "type": "text",
                                    "text": "預約",
                                    "color": "#ffffff",
                                    "flex": 0,
                                    "offsetTop": "-2px",
                                },
                                {
                                    "type": "filler"
                                }
                            ],
                            "spacing": "sm"
                        },
                        {
                            "type": "filler"
                        }
                        ],
                        "borderWidth": "1px",
                        "cornerRadius": "4px",
                        "spacing": "sm",
                        "borderColor": "#ffffff",
                        "margin": "xxl",
                        "height": "40px",
                        "action": {
                            "type": "postback",
                            "label": "action",
                            "data": 'action=select_date&service_id=' + str(service_id) + '&itemid=' + str(services[service_id]['itemid']),
                            "displayText": "我想預約" + service['title']
                        }
                    }
                    ],
                    "position": "absolute",
                    "offsetBottom": "0px",
                    "offsetStart": "0px",
                    "offsetEnd": "0px",
                    "backgroundColor": "#03303Acc",
                    "paddingAll": "20px",
                    "paddingTop": "18px"
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                    {
                        "type": "text",
                        "text": "尚有名額",
                        "color": "#ffffff",
                        "align": "center",
                        "size": "xs",
                        "offsetTop": "3px"
                    }
                    ],
                    "position": "absolute",
                    "cornerRadius": "20px",
                    "offsetTop": "18px",
                    "backgroundColor": "#ff334b",
                    "offsetStart": "18px",
                    "height": "25px",
                    "width": "53px"
                }
                ],
                "paddingAll": "0px"
            }
            }
            bubbles.append(bubble)
    bubble={
        "type": "bubble",
        "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": "取消預約",
                                "size": "xl",
                                "color": "#ffffff",
                                "weight": "bold"
                            }
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "baseline",
                        "contents": [
                        {
                            "type": "text",
                            "text": "  ",
                            "color": "#ebebeb",
                            "size": "sm",
                            "flex": 0
                        }
                        ],
                        "spacing": "lg"
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                        {
                            "type": "filler"
                        },
                        {
                            "type": "box",
                            "layout": "baseline",
                            "contents": [
                                {
                                    "type": "filler"
                                },
                                {
                                    "type": "text",
                                    "text": "取消",
                                    "color": "#ffffff",
                                    "flex": 0,
                                    "offsetTop": "-2px",
                                },
                                {
                                    "type": "filler"
                                }
                            ],
                            "spacing": "sm"
                        },
                        {
                            "type": "filler"
                        }
                        ],
                        "borderWidth": "1px",
                        "cornerRadius": "4px",
                        "spacing": "sm",
                        "borderColor": "#ffffff",
                        "margin": "xxl",
                        "height": "40px",
                        "action": {
                            "type": "postback",
                            "label": "action",
                            "data": 'action=notconfirmed',
                            "displayText": "取消預約"
                        }
                    }
                ],
                "position": "absolute",
                "offsetBottom": "0px",
                "offsetStart": "0px",
                "offsetEnd": "0px",
                "backgroundColor": "#03303Acc",
                "paddingAll": "20px",
                "paddingTop": "18px"
            }
            ],
            "paddingAll": "0px"
        }
    }
    bubbles.append(bubble)
    flex_message = FlexSendMessage(
        alt_text='hello',
        contents=
        {
        "type": "carousel",
        "contents": bubbles
        }
    )
    line_bot_api.reply_message(
        event.reply_token,
        [flex_message]
    )

def service_select_event(event):
    data = dict(parse_qsl(event.postback.data))
    quick_reply_buttons = []
    today = datetime.date.today()
    for x in range(1, 8):
        day = today + datetime.timedelta(days=x)
        quick_reply_button = QuickReplyButton(
                action=PostbackAction(label=f'{day}',
                                    text=f'我想預約{day}',
                                    data='action=select_time&service_id=' + str(data['service_id']) + '&itemid=' + str(data['itemid']) + '&date=' + str(day)
                                    )
            )
        quick_reply_buttons.append(quick_reply_button)

    quick_reply_button = QuickReplyButton(
            action=PostbackAction(label=f'取消',
                                text=f'取消',
                                data='action=notconfirmed'
                                )
        )
    quick_reply_buttons.append(quick_reply_button)

    text_message = TextSendMessage(text='好的，請選擇預約日期',
                                   quick_reply=QuickReply(items=quick_reply_buttons))
    
    line_bot_api.reply_message(
        event.reply_token,
        [text_message]
    )

def service_select_time_event(event):
    data = dict(parse_qsl(event.postback.data))
    quick_reply_buttons = []
    book_time = ['09:00', '11:00', '13:00', '15:00', '17:00']

    for time in book_time:
        quick_reply_button = QuickReplyButton(
                action=PostbackAction(label=time,
                                    text=f'{time}好了',
                                    data='action=confirm&service_id=' + str(data['service_id']) + '&itemid=' + str(data['itemid']) + '&date=' + str(data['date']) + '&time=' + str(time)
                                    )
            )
        quick_reply_buttons.append(quick_reply_button)

    quick_reply_button = QuickReplyButton(
            action=PostbackAction(label=f'取消',
                                text=f'取消',
                                data='action=notconfirmed'
                                )
        )
    quick_reply_buttons.append(quick_reply_button)


    text_message = TextSendMessage(text='好的，請選擇預約時間',
                                   quick_reply=QuickReply(items=quick_reply_buttons))
    line_bot_api.reply_message(
        event.reply_token,
        [text_message]
    )

def confirm_event(event):
    data = dict(parse_qsl(event.postback.data))
    profile = line_bot_api.get_profile(event.source.user_id)

    confirm_template_message = TemplateSendMessage(
        alt_text='Confirm template',
        template=ConfirmTemplate(
            text='好的，' + profile.display_name + '先生/小姐' + 
            '\n您的預約資訊如下: \n' + 
            '\n服務類別: ' + str(data['itemid']) + 
            '\n服務項目: ' + str(data['service_id']) + 
            '\n預約日期: ' + str(data['date']) + 
            '\n預約時間: ' + str(data['time']) + 
            '\n\n請問是否確認預約?',
            actions=[
                PostbackAction(
                    label='是',
                    display_text='確定!',
                    data='action=confirmed&service_id=' + str(data['service_id']) + '&itemid=' + str(data['itemid']) + '&date=' + str(data['date']) + '&time=' + str(data['time'])
                ),
                PostbackAction(
                    label='否',
                    text='抱歉，我再考慮一下好了',
                    data='action=notconfirmed'
                )
            ]
        )
    )

    line_bot_api.reply_message(
        event.reply_token,
        [confirm_template_message]
    )

def service_confirmed_event(event, user):
    data = dict(parse_qsl(event.postback.data))
    booking_service = services[int(data['service_id'])]
    booking_datetime = datetime.datetime.strptime(f'{data["date"]} {data["time"]}', '%Y-%m-%d %H:%M')
    reservation = Reservation.query.filter(Reservation.user_id == user.id,
                                          Reservation.is_canceled.is_(False),
                                          Reservation.booking_service == f'{booking_service["title"]}',
                                          Reservation.booking_datetime == datetime.datetime.strptime(f'{data["date"]} {data["time"]}', '%Y-%m-%d %H:%M')).first()
    
    # print(f'{booking_service["title"]}')
    # print(booking_datetime)

    if reservation:
        line_bot_api.reply_message(
            event.reply_token,
            [TextSendMessage(text='您已經預約過此活動該時段囉!請勿重複預約!')]
        )
        return


    

    user = User.query.filter(User.line_id == event.source.user_id).first()

    reservation = Reservation(
        user_id=user.id,
        booking_service_itemid=f'{booking_service["itemid"]}',
        booking_service=f'{booking_service["title"]}',
        booking_datetime=booking_datetime
    )

    db.session.add(reservation)
    db.session.commit()

    line_bot_api.reply_message(
        event.reply_token,
        [TextSendMessage(text='預約完成!期待到時與您相見哦!')]
    )

def service_notconfirmed_event(event):
    line_bot_api.reply_message(
        event.reply_token,
        [TextSendMessage(text='沒問題，如還有需要再預約哦!')]
    )

def cancel_event(event, user):
    reservations = book_or_not(event, user).order_by(Reservation.booking_datetime.asc()).all()

    if reservations:
        quick_reply_buttons = []

        for reservation in reservations:
            print(str(reservation.booking_service) + ', ' + str(reservation.booking_datetime)[5:16])
            quick_reply_button = QuickReplyButton(
                    action=PostbackAction(label=str(reservation.booking_service) + ', ' + str(reservation.booking_datetime)[5:16],
                                        text=str(reservation.booking_service) + ', ' + str(reservation.booking_datetime) + '那筆好了',
                                        data='action=canceled&service_id=' + str(reservation.booking_service) + '&time=' + str(reservation.booking_datetime)
                                        )
                )
            quick_reply_buttons.append(quick_reply_button)

        quick_reply_button = QuickReplyButton(
                    action=PostbackAction(label='取消',
                                        text='我再想想好了',
                                        data='action=notconfirmed'
                                        )
                )
        quick_reply_buttons.append(quick_reply_button)

        text_message = TextSendMessage(text='好的，以下為您已建立之預約，請選擇您想取消的預約',
                                    quick_reply=QuickReply(items=quick_reply_buttons))
        line_bot_api.reply_message(
            event.reply_token,
            [text_message]
        )

    else:
        line_bot_api.reply_message(
            event.reply_token,
            [TextSendMessage(text='查無您已預約資料，趕快進行預約吧!')]
        )

def canceled_event(event, user):
    data = dict(parse_qsl(event.postback.data))
    reservation = Reservation.query.filter(Reservation.user_id == user.id,
                                          Reservation.is_canceled.is_(False),
                                          Reservation.booking_service == data['service_id'],
                                          Reservation.booking_datetime == data['time']).first()
    reservation.is_canceled = True
    db.session.add(reservation)
    db.session.commit()
    line_bot_api.reply_message(
        event.reply_token,
        [TextSendMessage(text='已成功取消預約')]
    )
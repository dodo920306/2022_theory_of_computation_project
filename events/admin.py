from line_bot_api import *

from models.Reservation import Reservation
import datetime

def list_reservation_event(event):
    reservations = Reservation.query.filter(Reservation.is_canceled.is_(False),
                                            Reservation.booking_datetime > datetime.datetime.now(),
                                            ).order_by(Reservation.booking_datetime.asc()).all()
    reservation_data_text = '預約名單: \n'
    count = 1
    for reservation in reservations:
        reservation_data_text += f'''
            {count}. 預約時間: {reservation.booking_datetime}
               預約活動: {reservation.booking_service}
               參與人名稱: {reservation.user.display_name}\n'''
        count += 1

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reservation_data_text)
    )    
from flask import Flask, request, abort
from line_bot_api import *

def about_us_event(event):
    emoji = [
        {
            "index":13,
            "productId": "5ac21c46040ab15980c9b442",
            "emojiId": "001"
        },
        {
            "index":23,
            "productId": "5ac21c46040ab15980c9b442",
            "emojiId": "012"
        },
    ]
    text_message = TextSendMessage(text='''歡迎使用myProject$\n這是我的期末專案$\nHave fun!''', emojis=emoji)
    sticker_message = StickerSendMessage(
        package_id=11537,
        sticker_id=52002734
    )
    image_url = 'https://megapx-assets.dcard.tw/images/299d2b4c-a1c3-4bb2-8adc-853dcc67f3b1/orig.png'
    image_message = ImageSendMessage(
        original_content_url=image_url,
        preview_image_url=image_url
    )
    line_bot_api.reply_message(
        event.reply_token,
        [text_message, sticker_message, image_message])

def location_event(event):
    location_message = LocationSendMessage(
        title='國立成功大學',
        address='701台南市東區大學路1號',
        latitude=22.996773628798493, 
        longitude=120.21685658359358,
    )
    line_bot_api.reply_message(
        event.reply_token,
        [location_message])


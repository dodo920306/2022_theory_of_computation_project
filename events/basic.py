from flask import Flask, request, abort
from line_bot_api import *

def about_us_event(event):
    text_message = TextSendMessage(text='''您好!首先感謝您使用青年活動中心的line bot\n您可以在這邊預約參與活動並獲取最新訊息\n只需要點擊選單上對應的選項即可\nHave fun!''')

    image_url = 'https://megapx-assets.dcard.tw/images/299d2b4c-a1c3-4bb2-8adc-853dcc67f3b1/orig.png'
    image_message = ImageSendMessage(
        original_content_url=image_url,
        preview_image_url=image_url
    )
    line_bot_api.reply_message(
        event.reply_token,
        [text_message, image_message])

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

def talk_event(event):

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text='請寄信至dodo920306@gmail.com，會盡快回復您'))
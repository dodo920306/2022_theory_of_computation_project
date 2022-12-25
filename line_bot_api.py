from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, LocationSendMessage, StickerSendMessage, ImageSendMessage, TemplateSendMessage, ImageCarouselTemplate, ImageCarouselColumn, PostbackAction, PostbackEvent, FlexSendMessage, QuickReply, QuickReplyButton, MessageAction, ConfirmTemplate, ButtonsTemplate
)

line_bot_api = LineBotApi('JjqgIVJemlp3k/nelD6tiUW55eVdR8zZMiNHOxBO8pWDvNcZv2cKKdOeeSwRVO/JpgrDLXilZRfsJ2zXwbIFKpF8my+9AV6QvDsSAajjVORn11VLAfYcUqRkkKP3yw849O9TMVFSscBpBI9DI5c+TAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('4684f9102fb0d26de66f31ea02ae75e2')
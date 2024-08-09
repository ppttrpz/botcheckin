from lxml import etree
from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.addons import decimal_precision as dp
from odoo.tools.float_utils import float_is_zero, float_compare
from datetime import datetime, timedelta, date
from functools import partial
from itertools import groupby
from bs4 import BeautifulSoup

# from odoo.addons.mail.models.mail_activity import MailActivity
from odoo.exceptions import AccessError, UserError, ValidationError
from odoo.tools.misc import formatLang, get_lang
from odoo.osv import expression
import logging
import requests
_logger = logging.getLogger(__name__)
import time
import pytz
import locale
import re


class CheckinBot(models.Model):

    _inherit = "hr.employee"

    def telegramCheckin(self):
        # ฟังก์ชันส่งข้อความ
    # def send_msg(text, chat_id, thread_id):
        self._cr.execute(
                '''SELECT 
                        tg3.name AS name,  
                        he.last_check_in AS last_check_in, 
                        tg3.chat_id AS chat_id,
                        tg3.thread_id AS thread_id,
                        hl.request_date_from AS request_date_from,
                        hl.request_date_to AS request_date_to

                    FROM 
                        hr_employee he 
                    LEFT JOIN 
                        telegram_chatq3 tg3
                    ON 
                        tg3.emp_id = CAST(he.x_employee_id AS INTEGER)
                    LEFT JOIN
                        hr_leave hl
                    ON
                        hl.employee_id = he.id
                    AND 
                        CURRENT_DATE BETWEEN hl.request_date_from AND hl.request_date_to
                    WHERE 
                        he.active = true
                        AND tg3.name IS NOT NULL
                        AND hl.employee_id IS NULL;''')
         
        data = self._cr.dictfetchall()
        for item in data:
            # text = []
            
            text = f"[test] \n สวัสดีตอนเช้าค่ะ 🌅 อย่าลืม Check in เข้าทำงานนะคะ 😊 ขอให้เป็นวันที่ดีและสนุกกับการทำงานนะคะ 💪😊 ขอบคุณค่ะ "
            url = f"https://api.telegram.org/bot6382638700:AAHwehT8ZNz35b4LwIexYFPh0Sk4LiL_S_g/sendMessage"
            payload =                                                 {
                "text": text,
                "chat_id": item['chat_id'],
                "thread_id": item['thread_id']  # ใช้ thread_id แทน message_thread_id
                }
            headers = {
                "Accept": "application/json",
                "Content-Type": "application/json"
                }
            response = requests.post(url, json=payload, headers=headers)
            print(response.text)
        
        # for item in data:
        #     # ตรวจสอบและแปลงค่า last_check_in ให้เป็น string หากยังไม่เป็น
        #     if isinstance(item['last_check_in'], datetime):
        #         last_check_in_str = item['last_check_in'].strftime('%Y-%m-%d %H:%M:%S')
        #     else:
        #         last_check_in_str = item['last_check_in']
            
        #     # แปลงค่า last_check_in ให้เป็น datetime
        #     last_check_in_datetime = datetime.strptime(last_check_in_str, '%Y-%m-%d %H:%M:%S')

        #     # เพิ่มเวลาสำหรับ GMT+7 (เวลาปัจจุบันบวก 7 ชั่วโมง)
        #     gmt_plus_7 = last_check_in_datetime + timedelta(hours=7)

        #     # แปลงกลับไปเป็น string
        #     gmt_plus_7_str = gmt_plus_7.strftime('%Y-%m-%d %H:%M:%S')

        #     # แทรกค่าที่แปลงแล้วกลับเข้าไปใน text
        #     text = f"สวัสดีตอนเช้าค่ะ 🌅 อย่าลืม Check in เข้าทำงานนะคะ 😊 ขอให้เป็นวันที่ดีและสนุกกับการทำงานนะคะ 💪😊 ขอบคุณค่ะ "
            
        #     url = f"https://api.telegram.org/bot6382638700:AAHwehT8ZNz35b4LwIexYFPh0Sk4LiL_S_g/sendMessage"
        #     payload = {
        #         "text": text,
        #         "chat_id": item['chat_id'],
        #         "thread_id": item['thread_id']  # ใช้ thread_id แทน message_thread_id
        #     }
        #     headers = {
        #         "Accept": "application/json",
        #         "Content-Type": "application/json"
        #     }
        #     response = requests.post(url, json=payload, headers=headers)
            
    def telegramCheckin2(self):
        # ฟังก์ชันส่งข้อความ
    # def send_msg(text, chat_id, thread_id):
        self._cr.execute(
                '''SELECT 
                        tg3.name AS name,  
                        (he.last_check_in AT TIME ZONE 'UTC' AT TIME ZONE 'Asia/Bangkok') AS last_check_in, 
                        tg3.chat_id AS chat_id,
                        tg3.thread_id AS thread_id,
                        hl.request_date_from AS request_date_from,
                        hl.request_date_to AS request_date_to
                    FROM 
                        hr_employee he 
                    LEFT JOIN 
                        telegram_chatq3 tg3
                    ON 
                        tg3.emp_id = CAST(he.x_employee_id AS INTEGER)
                    LEFT JOIN
                        hr_leave hl
                    ON
                        hl.employee_id = he.id
                        AND CURRENT_DATE BETWEEN hl.request_date_from AND hl.request_date_to
                    WHERE 
                        he.active = true 
                        AND tg3.name IS NOT NULL
                        AND hl.employee_id IS NULL
                        AND he.last_check_in::date <> CURRENT_DATE;
                    ''')
         
        data = self._cr.dictfetchall()
        for item in data:
            # text = []
            
            text = f"สวัสดีค่ะ ☀️  {item['name']} ลืม Check in เข้าทำงานหรือเปล่าคะ? \n กรุณา Check in ด้วยนะคะ ขอบคุณค่ะ "
            url = f"https://api.telegram.org/bot6382638700:AAHwehT8ZNz35b4LwIexYFPh0Sk4LiL_S_g/sendMessage"
            payload = {
                "text": text,
                "chat_id": item['chat_id'],
                "thread_id": item['thread_id']  # ใช้ thread_id แทน message_thread_id
                }
            headers = {
                "Accept": "application/json",
                "Content-Type": "application/json"
                }
            response = requests.post(url, json=payload, headers=headers)
            # print(response.text)        
# -*- coding: UTF-8 -*-
from django.shortcuts import render

from api.utils.views import make_response
from api.gifts.models import Ticket

from twilio.rest import Client

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time, os

twilio_account_sid = 'ACa010d24cd6361dd5576d470aa7bd3877'
twilio_auth_token = 'a5c5147c26ebe6485a79e4c39a1c3041'
twilio_number = '+18645139083'

email_sender = 'ilovewangmiao@gmail.com'
email_passwd = 'wangmiao1221@'

def sms(message, phone_number):
    twilio_cli = Client(twilio_account_sid, twilio_auth_token)
    twilio_cli.messages.create(body=message, from_=twilio_number, to='+86'+phone_number)

def mail(receiver, subject, content):
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    part = MIMEText(content, 'plain', 'utf-8')
    msg.attach(part)
    smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
    smtpObj.ehlo()
    smtpObj.starttls()
    smtpObj.login(email_sender, email_passwd)
    smtpObj.sendmail(email_sender, receiver, msg.as_string().encode('ascii'))
    smtpObj.quit()

# Create your views here.
def view_gifts(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            if request.user.username == 'gift':
                mail(request.user.email, 'test', 'test')
                return make_response(200, 'success', '请求成功')
            else:
                return make_response(403, 'forbidden', '权限不足')
        else:
            return make_response(401, 'unauthorized', '尚未登录')
    else:
        return make_response(404, 'page_not_found', '页面不存在')

def view_qa(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            if request.user.username == 'gift':
                timestamp = time.time()
                file_name = 'gift_for_anniversary_' + str(int(timestamp)) + '.html'
                os.system('rm -rf /var/www/html/gift_for_anniversary_*')
                os.system('cp -f /home/lovewangmiao/gift_for_anniversary_20181221.html ' + '/var/www/html/' + file_name)
                qa = {
                    'question': [
                        {
                            'question': '余南龙是王淼的？',
                            'a': 'A. 小柴柴',
                            'b': 'B. 大傻狗',
                            'c': 'C. 大臭狗',
                            'd': 'D. A, B和C'
                        },
                        {
                            'question': '王淼是余南龙的？',
                            'a': 'A. 小可爱',
                            'b': 'B. 小香猪',
                            'c': 'C. 可爱的老婆',
                            'd': 'D. A, B和C'
                        },
                        {
                            'question': '余南龙对王淼表白的时候说过哪些话？',
                            'a': 'A. 你曾经问过我爱是什么，我一直都没有给你正式的回答',
                            'b': 'B. 其实我想说，爱就是我想永远和你在一起',
                            'c': 'C. 就算他们说白头偕老只是习惯使然，我也希望那个让我习惯的人是你',
                            'd': 'D. A, B和C'
                        }
                    ],
                    'answer': ['d', 'd', 'd'],
                    'gift_link': file_name,
                }
                
                return make_response(200, 'success', '请求成功', qa)
            else:
                return make_response(403, 'forbidden', '权限不足')
        else:
            return make_response(401, 'unauthorized', '尚未登录')
    else:
        return make_response(404, 'page_not_found', '页面不存在')

def view_tickets(request):
    if request.method == 'GET':
        res_data = {'ticket_list': []}
        if request.user.is_authenticated:
            for ticket in Ticket.objects.filter(user=request.user):
                res_data['ticket_list'].append(ticket.make_response_data())
            return make_response(200, 'success', '请求成功', res_data)
        else:
            res_data['ticket_list'].append({'pid': -1, 'name': '请先登陆', 'total': 0})
            return make_response(200, 'success', '请求成功', res_data)
    else:
        ticket = Ticket.objects.filter(pk=request.POST['pid'], user=request.user)
        if len(ticket) > 0:
            if ticket[0].total > 0:
                ticket[0].use()
                mail(ticket[0].related_ticket.user.email, 'lovewangmiao券使用通知', request.user.username+'已使用一张'+ticket[0].name)
                sms('【lovewangmiao】'+request.user.username+'已使用一张'+ticket[0].name, ticket[0].related_ticket.user.phone_number)
                return make_response(200, 'success', '请求成功', {'pid': ticket[0].id, 'name': ticket[0].name, 'total': ticket[0].total})
            else:
                return make_response(200, 'none', '该礼券已用完')
        else:
            return make_response(404, 'error', '不存在该券')

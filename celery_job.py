import csv
import os
from datetime import date, datetime

from celery.schedules import crontab
from jinja2 import Template
from weasyprint import HTML

from mail_config import send_email
from app import celery, cache

from controller import user_controller, post_controller

@celery.on_after_finalize.connect
def setup_intervalTASK(sender, **kwargs):
    sender.add_periodic_task(
        # Send a remainder at 5:30pm IST of every day
        # crontab(minute=30, hour=17),
        180,
        daily_rem.s(), name="Daily reminder"
    
    )

    # sender.add_periodic_task(
    #     # Send the monthly report at 5:30pm IST of every month
    #     # crontab(minute=30, hour=17, day_of_month=25),
    #     180,
    #     monthly_report.s(), name="Monthly Report"
    # )

@celery.task
def export(username):
    print("Exporting the data")
    filepath = 'static/download/'+username+'data.csv'

    # Check if folder is not present then create one
    if not os.path.exists('static/download/'):
        os.mkdir(path='static/download/')
    with open(file=filepath, mode='w') as file:
        writer = csv.writer(file)
        writer.writerow(["Username", "Post", "Date"])
        for post in Posts.query.filter_by(username=username).all():
            writer.writerow([post.title, post.description, post.timestamp])
    
    
    with open(r"templates/exportmaildata.html") as file:
        msg_template = Template(file.read())

    email = User.query.filter_by(username=username).first().email
    send_email(to=email, subject="CSV file for blog data ",
                msg=msg_template.render(), attachment=filepath)
   
    return 'sucess'

@celery.task
def daily_rem():
    print("Sending the daily reminder")
    send_email(to="kaustav@gmail.com", subject="Daily reminder",msg="Hello")
    '''with open(r"templates/dailyrem.html") as file:
        msg_template = Template(file.read())

    for user in User.query.all():
        send_email(to=user.email, subject="Daily reminder",
                    msg=msg_template.render(username=user.username))'''
    return 'sucess'

@celery.task
def monthly_report():
    print("Sending the monthly report")
    '''with open(r"templates/monthlyreport.html") as file:
        msg_template = Template(file.read())

    for user in User.query.all():
        send_email(to=user.email, subject="Monthly report",
                    msg=msg_template.render(username=user.username))'''
    return 'sucess'
from celery import Celery, shared_task,Task
from celery.contrib.abortable import AbortableTask
from time import sleep
from src.models import User
from src.extentions import db
from flask import current_app as app
from flask_login import current_user
from docxtpl import DocxTemplate, InlineImage
from src.utils import tokens
from datetime import date



@shared_task(bind=True)
def GetReceipt(self, celery_obj):
    doc = DocxTemplate("invoice/stockinvoice.docx") #receipt document
       
    SalesRows=[]  #intilazing values
    checkout_total = 0  
    invoice = tokens() #unique 8 it identifer
    
    context ={
    "invoice_id" : invoice,
    "date" : date.today(),
    "recipient": celery_obj["username"],
    "address": celery_obj["address"],
    "phone": celery_obj["phoneno"],
    "salesTbRows": celery_obj["SalesRow"],
    "subtotal": celery_obj["checkout_total"],
    "total": celery_obj["checkout_total"]
    }
 
    doc.render(context)
    filename = f'invoice/{invoice}.docx' #generating username
    doc.save(filename)

    return "Done"

@shared_task(bind=True, base=AbortableTask)
def add_user(self, form_data):
    # db.session.add(User(username=form_data['Username'], password=form_data['Password']))
    # db.session.commit()

    user = User(username=form_data['Username'], password=form_data['Password'])
    User.create_user(user)



    for i in range(10):
        print(i)
        sleep(1)
        if self.is_aborted():
            return 'TASK STOPPED'
    return "DONE!"



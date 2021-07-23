from django.core.mail import message, send_mail
from django.conf import settings

from django.contrib.auth.models import User
def sendEmailNotification(data):
    print(data)
    user_det=User.objects.all() 
    recepient_email=[]  
    for each_user in user_det:
        print(each_user.email)
        recepient_email.append(each_user.email)  

    title=data["title"]
    sp=data["sp"]
    subject="New Products"
    message=f"new Product ${title} @ ${sp}"
    email_from="krishakgrocery123@gmail.com"
    recepient_list=recepient_email
    send_mail(subject,message,email_from,recepient_list)
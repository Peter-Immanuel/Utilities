from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import (
   DynamicTemplateData, 
   TemplateId, 
   Mail
)


def emailContent(email, name, *args, **kwargs):
   ''' 
   function to create a mail object and send it to the user 
   args:
      email: receiver's email
      name: receiver's name
      *args: none
      *kwargs: none
   '''
   
   message = Mail(                      
      from_email="email of sender",                              # Change Mail to oxy receiver
      to_emails=email,
      subject='Jas Fitness Spa Discount Code',
   )
 
   message.dynamic_template_data = DynamicTemplateData(dynamic_template_data=kwargs.dict())
   message.template_id = TemplateId("template id gotten from sendgrid's dashboard")
   return message

_content = emailContent()


# Sending the email
try:    
   sg = SendGridAPIClient("Sendgrid API key")                          
   response = sg.send(_content)
except Exception as e:
      print(e)


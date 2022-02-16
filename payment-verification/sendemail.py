import os
import base64
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import *


book_title ={
        "book1": "Stamp out Fraud in your System",
        "book2":"Keys to sustainable small & medium enterprises"
}


def sendBook(buyer_email, buyer_name, book_name):
        message = Mail(
                from_email='bem.techdot@gmail.com',
                to_emails=buyer_email,
                subject='RiverGate Book Delivery',
                html_content=f'''<strong>Dear {buyer_name}, <br/>
                                        Thank you for purchasing our book. attached to this mail is your copy.<br/>
                                        Best regards,<br/>
                                        Rivergate oxy.</strong>'''
                ) 


        with open(f"books/{book_name}.pdf", 'rb') as f:
                data = f.read()
                f.close()
        encoded_file=base64.b64encode(data).decode()

        attachedFile = Attachment(
                FileContent(encoded_file),
                FileName(f"{book_title[book_name]}"),
                FileType("application/pdf"),
                Disposition('attachment')
        )

        message.attachment = attachedFile
        return message


# try:
#         message = sendBook("peterbemshima@gmail.com","Soliu Babatunde Alley", "book1")
#         sg = SendGridAPIClient(os.environ.get("SENDGRID_API_KEY"))                        
#         response = sg.send(message)
# except Exception as e:
#         print(e)
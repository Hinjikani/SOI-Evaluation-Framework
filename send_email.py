import smtplib
import os
import dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

dotenv.load_dotenv()

port = 465
smtp_server = "smtp.gmail.com"
email = os.getenv("EMAIL")
password = os.getenv("PASSWORD")

def sendEmail(receiver_email, name, link, company_name=""):
    message = MIMEMultipart("alternative")
    message["Subject"] = "Your SOI Results"
    message['From'] = email
    message['To'] = receiver_email
    if company_name != "":
        company_message = f"<p>Here is the results of { company_name } Sustainability-oriented Innovation Assessment</p>"
    else:
        company_message = ""
    link = f"http://localhost:5000/results/{link}"
    html = f"""
    <!DOCTYPE html>
    <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>SOI Results</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background-color: #f4f4f4;
                    border: 0;
                }}
                table {{
                    width: 100%;
                    border: 0;
                }}
                td {{
                    margin: 0 auto;
                    padding: 20px;
                }}
                .content {{
                    width: 600px;
                    border: 0;
                    border-collapse: collapse;
                    border: 1px solid #cccccc;
                }}
                .header {{
                    background-color: #345C72;
                    color: #fff;
                    text-align: center;
                    padding: 40px;
                    font-size: 24px;
                    font-weight: bold;
                }}
                .body {{
                    padding: 40px;
                    text-align: left;
                    font-size: 16px;
                    line-height: 1.6;
                }}
                .td-button-container {{
                    padding: 0px 40px 0px 40px;
                    text-align: center;
                }}
                .table-button {{
                    margin: auto;
                }}
                .td-button {{
                    background-color: #345C72;
                    padding: 10px 20px;
                    border-radius: 5px;
                    color: #fff;
                    text-decoration: none;
                }}
                .footer {{
                    background-color: #333333;
                    padding: 40px;
                    text-align: center;
                    color: white;
                    font-size: 14px;
                }}
            </style>
        </head>
        <body>
            <table>
                <tr>
                    <td>
                        <table class="content">
                            <!-- Header -->
                            <tr>
                                <td class="header">
                                    <h1>SOI Results</h1>
                                </td>
                            </tr>
                            <!-- Body -->
                            <tr>
                                <td class="body">
                                    <p>Hello, { name } </p>
                                    {company_message}
                                </td>
                            </tr>
                            <!-- CTA button-->
                            <tr>
                               <td class="td-button-container">
                                   <!-- CTA Button -->
                                    <table>
                                       <tr>
                                           <td>
                                               <a href="{link}" target="_blank" class="td-button link" alt="SOI Results">SOI Results</a>
                                           </td>
                                       </tr>
                                    </table>
                               </td>
                            </tr>
                        </table>
                    </td>
                </tr>
            </table>
        </body>
    </html>
    """
    message.attach(MIMEText(html, "html"))
    with smtplib.SMTP_SSL(smtp_server, port) as server:
        server.ehlo()
        server.login(email, password)
        server.sendmail(email, receiver_email, message.as_string())
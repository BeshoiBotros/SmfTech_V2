from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags

def send_reset_password_email(reset_link, user_email):
    subject = 'Reset Your Password'
    from_email = 'smfdevteam@gmail.com'
    to_email = user_email

    # Prepare HTML content
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            /* Add your CSS here */
            body {
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
                margin: 0;
                padding: 0;
            }
            .email-container {
                width: 100%;
                max-width: 600px;
                margin: 0 auto;
                background-color: #ffffff;
                padding: 20px;
                border-radius: 5px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            }
            .header {
                text-align: center;
                padding: 10px 0;
                border-bottom: 1px solid #e0e0e0;
            }
            .header h1 {
                margin: 0;
                font-size: 24px;
                color: #333333;
            }
            .content {
                padding: 20px 0;
            }
            .content p {
                font-size: 16px;
                color: #666666;
            }
            .reset-button {
                display: block;
                width: 200px;
                margin: 20px auto;
                padding: 10px 20px;
                background-color: #007BFF;
                color: #ffffff;
                text-align: center;
                text-decoration: none;
                border-radius: 5px;
                font-size: 16px;
                font-weight: bold;
            }
            .footer {
                text-align: center;
                padding: 10px 0;
                border-top: 1px solid #e0e0e0;
                margin-top: 20px;
                font-size: 12px;
                color: #999999;
            }
            @media (max-width: 600px) {
                .email-container {
                    padding: 10px;
                }
                .header h1 {
                    font-size: 20px;
                }
                .content p {
                    font-size: 14px;
                }
                .reset-button {
                    width: 100%;
                    font-size: 14px;
                }
            }
        </style>
    </head>
    <body>
        <div class="email-container">
            <div class="header">
                <h1>Password Reset Request</h1>
            </div>
            <div class="content">
                <p>You recently requested to reset your password for your account. Click the button below to reset it.</p>
                <a href="{{ reset_link }}" class="reset-button">Reset Password</a>
                <p>If you did not request a password reset, please ignore this email or contact support if you have questions.</p>
            </div>
            <div class="footer">
                <p>Thank you,<br>Your Company Name</p>
            </div>
        </div>
    </body>
    </html>
    """.replace('{{ reset_link }}', reset_link)

    text_content = strip_tags(html_content)

    email = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
    email.attach_alternative(html_content, "text/html")
    email.send()
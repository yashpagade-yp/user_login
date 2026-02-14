"""
Email Templates Module

This module contains HTML templates for various email notifications.
"""


def get_otp_email_template(otp: str, user_name: str = "User") -> str:
    """
    Generate HTML email template for password reset OTP.

    Args:
        otp: The One-Time Password to display
        user_name: Name of the user (optional)

    Returns:
        str: HTML content string
    """
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
                margin: 0;
                padding: 0;
            }}
            .container {{
                max_width: 600px;
                margin: 20px auto;
                background-color: #ffffff;
                padding: 40px;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                text-align: center;
            }}
            .header {{
                color: #333333;
                margin-bottom: 30px;
            }}
            .otp-code {{
                font-size: 36px;
                font-weight: bold;
                color: #4CAF50;
                letter-spacing: 8px;
                margin: 20px 0;
                padding: 15px;
                background-color: #f9f9f9;
                border-radius: 4px;
                display: inline-block;
            }}
            .message {{
                color: #666666;
                line-height: 1.6;
                margin-bottom: 20px;
            }}
            .footer {{
                margin-top: 30px;
                font-size: 12px;
                color: #999999;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h2 class="header">Password Reset Request</h2>
            <div class="message">
                <p>Hello {user_name},</p>
                <p>We received a request to reset your password. Use the OTP below to proceed:</p>
            </div>
            
            <div class="otp-code">{otp}</div>
            
            <div class="message">
                <p>This code is valid for <strong>5 minutes</strong>.</p>
                <p>If you didn't request this, you can safely ignore this email.</p>
            </div>
            
            <div class="footer">
                <p>&copy; 2024 Your App Name. All rights reserved.</p>
            </div>
        </div>
    </body>
    </html>
    """

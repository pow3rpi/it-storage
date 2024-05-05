from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class EmailMessageFactory:

    @staticmethod
    def build_sign_up_verification(msg: MIMEMultipart, verification_link: str) -> str:
        html = f"""\
        <html>
          <head></head>
          <body>
            <span>Hi there,
              <br><br>
              We are happy that you have decided to use our service!
              <br>
              Here is your activation <a href="{verification_link}" target="_blank">link</a>.
              It is valid only for 2 hours.
              <br><br> 
              Kind regards,
              <br>
              IT-Storage Team
            </span>
          </body>
        </html>
        """
        part = MIMEText(html, 'html')
        msg.attach(part)
        return msg.as_string()

    @staticmethod
    def build_sign_up_verification_successful(msg: MIMEMultipart) -> str:
        html = f"""\
        <html>
          <head></head>
          <body>
            <span>Hi there,
              <br><br>
              Your account at <b>IT-Storage</b> has been successfully activated!
              <br><br> 
              Kind regards,
              <br>
              IT-Storage Team
            </span>
          </body>
        </html>
        """
        part = MIMEText(html, 'html')
        msg.attach(part)
        return msg.as_string()

    @staticmethod
    def build_changed_pwd_notification(msg: MIMEMultipart, username: str) -> str:
        html = f"""\
            <html>
              <head></head>
              <body>
                <span>Hi there,
                  <br><br>
                  Your password for profile "<i>{username}</i>" at <b>IT-Storage</b> has been changed.
                  <br>
                  If you didn't do this, please contact us in a reply letter.
                  <br><br> 
                  Kind regards,
                  <br>
                  IT-Storage Team
                </span>
              </body>
            </html>
            """
        part = MIMEText(html, 'html')
        msg.attach(part)
        return msg.as_string()

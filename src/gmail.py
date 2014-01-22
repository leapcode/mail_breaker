#!/usr/bin/env python
# encoding: utf-8

import mimetypes
import os
import smtplib

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class GMail(object):
    """Email sender using the gmail service."""
    SMTPSERVER = 'smtp.gmail.com:587'

    def __init__(self, account, password):
        """
        Initializes the class.
        You should provide credentials in order to login into gmail.

        :param account: the username@gmail.com account to use for sending.
        :type account: str
        :param password: the password for the account.
        :type password: str
        """
        self._from = account
        login = account.split('@')[0]
        self._server = smtplib.SMTP(self.SMTPSERVER)
        self._server.starttls()
        self._server.login(login, password)

    def __del__(self):
        """
        Quits the server.
        """
        self._server.quit()

    def _get_attachment(self, file_path):
        """
        Creates the MIMEBase attachment for the file 'file_path'.

        Might raise:
            IOError

        :param file_path: the file from to generate the attachment from.
        :type file_path: str

        :return: the MIMEBase attachment.
        :rtype: MIMEBase
        """
        ctype, encoding = mimetypes.guess_type(file_path)
        if ctype is None or encoding is not None:
            # No guess could be made, or the file is encoded (compressed),
            # so use a generic bag-of-bits type.
            ctype = 'application/octet-stream'
        maintype, subtype = ctype.split('/', 1)

        # Read the file, this may rise IOError
        with open(file_path, 'rb') as fp:
            the_file = MIMEBase(maintype, subtype)
            the_file.set_payload(fp.read())

        # Encode the payload using Base64
        encoders.encode_base64(the_file)

        # Set the filename parameter
        the_file.add_header('Content-Disposition', 'attachment',
                            filename=os.path.basename(file_path))

        return the_file

    def send_email(self, to_addr_list, cc_addr_list, subject,
                   message, attachments=None):
        """
        Sends an email.

        :param to_addr_list: a list of addresses to send the email.
        :type to_addr_list: list of str
        :param cc_addr_list: a list of addresses to send (as CC) the email.
        :type cc_addr_list: list of str
        :param subject: the subject of the email
        :type subject: str
        :param message: the message to send
        :type message: str
        :param attachments: a list of paths for the files to attach.
        :type attachments: list of str

        :return: an empty dict if everything went ok or
                 the problems result of sending the email(s).
        :rtype: dict
        """
        # Create the container (outer) email message.
        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['From'] = self._from
        msg['To'] = ', '.join(to_addr_list)

        if cc_addr_list:
            msg['Cc'] = ', '.join(cc_addr_list)

        # Add the message's text
        msg.attach(MIMEText(message))

        problems = ''
        if attachments is not None:
            # Attach every file in the attachment parameter
            for file_path in attachments:
                try:
                    the_file = self._get_attachment(file_path)
                    msg.attach(the_file)
                except IOError:
                    problems += "Could not attach {0!r}\n".format(file_path)

        message = msg.as_string()
        try:
            result = self._server.sendmail(self._from, to_addr_list, message)
        except Exception as e:
            result = {'Exception': repr(e)}

        if problems:
            result['Attachments'] = problems

        return result

    def send_email_string(self, mail, to):
        """
        Sends an email from an already created email as a string.

        :param mail: the mail to send
        :type mail: str
        :param to: a address to send the email.
        :type to: str

        :return: an empty dict if everything went ok or
                 the problems result of sending the email(s).
        :rtype: dict
        """
        try:
            result = self._server.sendmail(self._from, [to], mail)
        except Exception as e:
            result = {'Exception': repr(e)}

        return result

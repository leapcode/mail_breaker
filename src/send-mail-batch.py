#!/usr/bin/env python
# encoding: utf-8
# import getpass
import mimetypes
import os
import sys
import random
import smtplib
import time

from ConfigParser import SafeConfigParser

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
            result['Exception'] = repr(e)

        if problems:
            result['Attachments'] = problems

        return result


def send_test_mail(subject):
    # make a list of attachments, add all the files in 'directory'
    directory = './attachments/'
    file_list = []

    # randomize the use of attachments
    if random.choice([True, False]):
        for filename in os.listdir(directory):
            path = os.path.join(directory, filename)
            if os.path.isfile(path):
                file_list.append(path)

        # randomize attachments
        ammount = random.randint(0, len(file_list)-1)
        random.shuffle(file_list)
        file_list = file_list[0:ammount]

    msg = ('Howdy from python!\n'
           'The subject: {0}\n'
           "Current date & time: {1}\n"
           "Trying to attach: {2!r}"
           ).format(subject, time.strftime("%c"), file_list)

    return gmail.send_email(
        to_addr_list=TO, cc_addr_list=[],
        subject=subject, message=msg, attachments=file_list)

# Read subjects from file
lorem_subjects = []
lorem_file = './lorem-ipsum-subjects.txt'
with open(lorem_file) as lorem:
    lorem_subjects = [line.strip() for line in lorem]


# Mail account to send from:
# use this if you want to enter manually your password:
# FROM = 'your.username@gmail.com'
# SECRET = getpass.getpass("Password for {0}: ".format(FROM))

# MAX_MAILS = 10
# TO = ['test_account@dev.bitmask.net']

# Read credentials from options file
parser = SafeConfigParser()
parser.read('options.cfg')
try:
    FROM = parser.get('Credentials', 'account')
    SECRET = parser.get('Credentials', 'password')
    TO = [parser.get('Configs', 'to')]
    MAX_MAILS = parser.getint('Configs', 'mails_amount')
except Exception as e:
    print "Problem reading options.cfg"
    print "Exception: {0!r}".format(e)
    sys.exit()


# create the GMail global object
gmail = GMail(FROM, SECRET)

print "Sending {0} mails batch...".format(MAX_MAILS)

count = 0
while count < MAX_MAILS:
    idx = (count % len(lorem_subjects))
    subject = "[TEST] {0:03} - {1}".format(count+1, lorem_subjects[idx])
    print "Sending '{0}' ... ".format(subject),
    try:
        problems = send_test_mail(subject)
    except Exception as e:
        problems = repr(e)

    if problems:
        print "Problems: {0!r}".format(problems)
    else:
        print 'ok.'

    count += 1

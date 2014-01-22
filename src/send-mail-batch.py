#!/usr/bin/env python
# encoding: utf-8
# import getpass
import os
import sys
import random
import time

from ConfigParser import SafeConfigParser

from gmail import GMail


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

#!/usr/bin/env python
# encoding: utf-8
# import getpass
import os
import sys

from ConfigParser import SafeConfigParser

from gmail import GMail


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

directory = './emails/'
file_list = []

for filename in os.listdir(directory):
    path = os.path.join(directory, filename)
    if os.path.isfile(path):
        file_list.append(path)

print "Sending {0} mail(s)...".format(len(file_list))

for mail_file in file_list:
    print "Sending '{0}' ... ".format(mail_file),
    with open(mail_file) as f:
        email = f.read()

    try:
        # replace placeholders with actual data
        email = email.format(FROM=FROM, TO=','.join(TO))
    except KeyError:
        print "Warning: missing placeholder in {0}".format(mail_file)

    try:
        problems = gmail.send_email_string(email, TO)
    except Exception as e:
        problems = repr(e)

    if problems:
        print "Problems: {0!r}".format(problems)
    else:
        print 'ok.'

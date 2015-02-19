Mail breaker
============

This repository holds a set of tools and sample data used to stress tests an
email account.


Configuration
-------------

You need to create the `options.cfg` file from which the batch mail sender will
read the email accounts to use. You can copy the `options.cfg.demo` as a
template.

NOTE: the file `options.cfg` is ignored by git.


```
[Credentials]
account = the_email_account_to_send_from@gmail.com
password = this_is_the_gmail_account_password

[Configs]
mails_amount = 100
to = account_to_test@cdev.bitmask.net
```

NOTE: to use gmail as sender account you need to 'allow less secure apps' (see
https://support.google.com/accounts/answer/6010255)

Batch mail
----------

To send a batch of mails just run the `send-mail-batch.py` script. It will send
the batch using the information found in the `options.cfg` file (`mails_amount`
mails to `to` from `from`)

RAW mail send
-------------

To send mail strings as you found them in the source of an email you can use
the `send-mail-strings.py` script.

It will read the `emails/` folder and send each file content as a separate
email using its contents as the source.

This script espects to have the `{FROM}` and `{TO}` strings within those files
in order to set the sender and receiver for the emails.

This will send just one batch of emails (as many emails as you have in the
`emails/` folder).


Simple email send
-----------------

The `swaks-batch.sh` script uses the `swaks` tool (see
http://www.jetmore.org/john/code/swaks/) to send emails specifying the data
needed in the command line. There is a line for each special case that we want
to test for an email account.

This script reads the `to` field from the `options.cfg` file.

#!/bin/sh
# This scripts depends on swaks: http://www.jetmore.org/john/code/swaks/

if [ -n "$1" ]; then
    SWAKS=$1
else
    SWAKS=swaks
fi

# if [[ "$SWAKS" == "" ]]; then
if ! `hash $SWAKS 2>/dev/null`; then
    echo "Error: I need swaks to work."
    echo "You can get swaks from: http://www.jetmore.org/john/code/swaks/"
    echo "If you already have it, you can send its location as a first parameter of the script."
    echo "E.g.: $0 /path/to/swaks"
    exit 1
fi

# Python helper to read configurations from file:
TO=`python -c "from ConfigParser import SafeConfigParser as scp; p = scp(); p.read('options.cfg'); print p.get('Configs', 'to');"`

FROM=swaks@bitmask.net  # this account does not need to exist.

# NOTE: Add the swak commands below here:

# Non-ascii subject and body, without charset specification
$SWAKS --to $TO --from $FROM --header "Subject: Test 01 -- áèīôü" --body "Howdy from swaks. ýëąĥ" --helo 'asdf.com'

# Non-ascii subject and body, with charset specification
$SWAKS --to $TO --from $FROM --header "Content-Type: text/plain; charset='utf-8'\nSubject: Test 02 -- áèīôü" --body "Howdy from swaks. ýëąĥ" --helo 'asdf.com'

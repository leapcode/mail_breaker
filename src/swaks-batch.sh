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

# Customize this in order to test the desired accounts
FROM=ivan@dev.bitmask.net
TO=test_123@dev.bitmask.net

# NOTE: Add the swak commands below here:

# Unicode subject and body, without charset specification
$SWAKS --to $TO --from $FROM --header "Subject: Test -- áèīôü" --body "Howdy from swaks. ýëąĥ" --helo 'asdf.com'

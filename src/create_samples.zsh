#!/bin/zsh
# create_samples.zsh
# Copyright (C) 2014 LEAP
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

#
# Create samples in a destination folder, subsituting some vars from
# the templates found in the mail_breaker repo.
#

SAMPLESDIR="/tmp/leap_mail_samples/"
TEMPLATESDIR="./emails"

SUBST_EXPR='s/{FROM}/test@cdev.bitmask.net/;s/{TO}/test@cdev.bitmask.net/'

create_sampledir() {
 mkdir -p $SAMPLESDIR
}

replace_templates() {
 for file in $(eval ls "${TEMPLATESDIR}/*");
 do { name=`basename $file`;
      sed ${SUBST_EXPR} $file > "${SAMPLESDIR}/${name}" }
 done;
}

echo_dest() {
 echo "[+] Samples created at $SAMPLESDIR"
}


{ test "$1" = "--help" } && {
 echo "Usage: $0 [/path/to/samples-destination]"
 exit 0
}

# If the first parameter is passed, take it as the SAMPLES destination
# folder.
{ test $1 } && {
 SAMPLESDIR=$1
}

create_sampledir
replace_templates
echo_dest

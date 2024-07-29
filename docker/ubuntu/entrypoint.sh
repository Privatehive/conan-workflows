#!/bin/sh

TMPFILE=$(mktemp /tmp/cmd-XXXXXXXX.sh)
echo "#!/bin/bash\nsudo apt-get -y -q update\nconan profile detect -vquiet\n$@" > $TMPFILE
exec bash -e $TMPFILE

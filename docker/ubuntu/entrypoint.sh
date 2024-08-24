#!/bin/sh

TMPFILE=$(mktemp /tmp/cmd-XXXXXXXX.sh)
echo "#!/bin/bash\nsudo apt-get -y -q update\nconan profile detect -vquiet\necho 'tools.system.package_manager:mode = install' >> $(conan config home)/global.conf\necho 'tools.system.package_manager:sudo = True' >> $(conan config home)/global.conf\n$@" > $TMPFILE
exec bash -e $TMPFILE

#!/bin/bash

TMPFILE=$(mktemp /tmp/cmd-XXXXXXXX.bat)
printf "@echo off\r\nset Python_ROOT_DIR=C:\\Python\r\nconan profile detect -vquiet\r\n$@" > $TMPFILE
#. /opt/mkuserwineprefix
exec wine64 cmd /S /C $TMPFILE

#!/bin/sh
# enable for debugging:
#set -x
#exec 2>>/tmp/nagios-cacti.log

url="$1"
type="$2"
user="$3"
password="$4"

# Remove trailing slash if needed
url="${url%/}"

if [ -z "$url" ]; then
	echo >&2 "Usage: $0 URL TYPE [USER PASSWORD]"
	exit 1
fi

# pass user and password conditionally.
# this way we can even have passwords in them.
# retry only once with timeout of 30s
exec wget -t 1 -T 30 --no-check-certificate -q -O- ${user:+--user="$user" --password="$password"} "$url/mrtgstats.cgi?type=$type"

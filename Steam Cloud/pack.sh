#!/usr/bin/env bash

rm -f lol.tar.gz
tar czvf lol.tar.gz *.deb >/dev/null

echo "rm -rf /build"
echo "mkdir /build"
echo "cd /build"

cat lol.tar.gz | base64 | sed -E 's/(.*)/echo "\1" >> lol.tar.gz.b64/'

echo "cat lol.tar.gz.b64 | base64 -d > lol.tar.gz"

echo "tar xzvf lol.tar.gz"

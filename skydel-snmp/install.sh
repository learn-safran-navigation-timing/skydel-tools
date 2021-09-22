#!/bin/bash

SCRIPT_DIR="$(dirname "$0")"
PASS_INSTALL_DIR=/usr/local/share/skydel_snmp

if [ "$EUID" -ne 0 ]
  then echo "Please run as root"
  exit
fi

apt update
apt install snmpd snmp-mibs-downloader python3
cd $HOME/Documents/Skydel-SDX/API/Python
python3 setup.py install
cd -

mkdir -p /usr/local/share/skydel_snmp
cp $SCRIPT_DIR/snmp_pass.py $SCRIPT_DIR/skydel_snmp.py $PASS_INSTALL_DIR

cp $SCRIPT_DIR/snmpd.conf /etc/snmp/

systemctl restart snmpd

echo "Install complete"

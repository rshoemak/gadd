#!/usr/bin/env bash

file="GADD-ASA_input_cfg.json"
echo
echo "Removing network"
curl -k -v -u $NFVIS_LOGIN_INPUT:$NFVIS_PASSWRD_INPUT -X DELETE $NFVIS_URL_INPUT/api/config/networks/network/svc-gadd-net
echo
echo "Removing bridge"
curl -k -v -u $NFVIS_LOGIN_INPUT:$NFVIS_PASSWRD_INPUT -X DELETE $NFVIS_URL_INPUT/api/config/bridges/bridge/svc-gadd-br
echo
echo "Remove input json file"
if [ -f $file ] ; then
    rm $file
fi


#!/usr/bin/env bash

file1="GADD-ASA_input_cfg.json"
file2="gadd_dock_env"
file3="ui/gophp/GADD-ASA_input_cfg.json"
echo
echo "Removing deployed ASAv"
curl -k -v -u $NFVIS_LOGIN_INPUT:$NFVIS_PASSWRD_INPUT -X DELETE \
$NFVIS_URL_INPUT/api/config/vm_lifecycle/tenants/tenant/admin/deployments/deployment/ASAv
echo
echo "Moving ISRv back to LAN Network"
curl -k -v -u $NFVIS_LOGIN_INPUT:$NFVIS_PASSWRD_INPUT -X PUT \
$NFVIS_URL_INPUT/api/config/vm_lifecycle/tenants/tenant/admin/deployments/deployment/1481300657/vm_group/ROUTER/interfaces \
-H "Content-type: application/vnd.yang.data+json" \
-d @network_map.json
echo
echo "Removing network"
curl -k -v -u $NFVIS_LOGIN_INPUT:$NFVIS_PASSWRD_INPUT -X \
DELETE $NFVIS_URL_INPUT/api/config/networks/network/svc-gadd-net
echo
echo "Removing bridge"
curl -k -v -u $NFVIS_LOGIN_INPUT:$NFVIS_PASSWRD_INPUT -X \
DELETE $NFVIS_URL_INPUT/api/config/bridges/bridge/svc-gadd-br
echo
echo "Remove input json file"
if [ -f $file1 ] ; then
    rm $file1
fi
echo
echo "Remove docker env file"
if [ -f $file2 ] ; then
    rm $file2
fi
echo
echo "Remove input json ui file"
if [ -f $file3 ] ; then
    rm $file3
fi
echo

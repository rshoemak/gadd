#!/usr/bin/env bash
# run this from command line first: "source gadd_setup"
#
echo
echo Please provide details for your deployment.
echo
echo "what is the url for the NFVis device?"
read r_nfvis_url
echo
echo "What is the NFVis login name?"
read r_nfvis_login
echo
echo "What is the NFVis password?"
read r_nfvis_passwrd
echo
echo "What is the Spark Room Token?"
read r_spark_room_token
echo
echo "What is the APIC URL? i.e., http://x.x.x.x"
read r_apic_url
echo
echo "What is the APIC login name?"
read r_apic_login
echo
echo "What is the APIC password?"
read -s r_apic_passwrd
echo
echo "What is the trigger event IP (IP address of host at remote branch)?"
echo r_trigger_event_ip
echo


export TOKEN_INPUT="Bearer $r_spark_room_token"
export APIC_URL_INPUT="$r_apic_url"
export APIC_LOGIN_INPUT="$r_apic_login"
export APIC_PASSWRD_INPUT="$r_apic_passwrd"
export NFVIS_LOGIN_INPUT="$r_nfvis_login"
export NFVIS_PASSWRD_INPUT="$r_nfvis_passwrd"
export NFVIS_URL_INPUT="$r_nfvis_url"
export TRIGGER_EVENT_IP="$r_trigger_event_ip"

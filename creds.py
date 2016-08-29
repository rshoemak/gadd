
import requests
import os


requests.packages.urllib3.disable_warnings()

# ENV setup for production
tk_inp = os.getenv('TOKEN_INPUT')
aur_inp = os.getenv('APIC_URL_INPUT')
alg_inp = os.getenv('APIC_LOGIN_INPUT')
aps_inp = os.getenv('APIC_PASSWRD_INPUT')
nlg_inp = os.getenv("NFVIS_LOGIN_INPUT")
nps_inp = os.getenv("NFVIS_PASSWRD_INPUT")
nurl_inp = os.getenv("NFVIS_URL_INPUT")


def nvfis_getgcred():
    login = nlg_inp
    password = nps_inp
    url = nurl_inp
    return url, login, password


def spark_GetArgs():
    token = tk_inp
    # add other variables as needed and return
    return token


def apic_GetArgs():
    # enter in your credentials for your APIC
    a_url = aur_inp
    a_login = alg_inp
    a_password = aps_inp
    return a_url, a_login, a_password

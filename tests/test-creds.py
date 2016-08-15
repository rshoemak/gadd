import unittest
import os

# working area to set env for lab
tk_inp = os.getenv('TOKEN_INPUT')
aur_inp = os.getenv('APIC_URL_INPUT')
alg_inp = os.getenv('APIC_LOGIN_INPUT')
aps_inp = os.getenv('APIC_PASSWRD_INPUT')
nlg_inp =  os.getenv("NFVIS_LOGIN_INPUT")
nps_inp = os.getenv("NFVIS_PASSWRD_INPUT")
nurl_inp = os.getenv("NFVIS_URL_INPUT")


#nlg_inp = "admin"
#nps_inp = "admin"
#nurl_inp = "https://10.91.13.154"
#tk_inp = "Bearer Y2VkYjBlYTgtMTNiYy00YWQ2LThmMWYtZDljNWE4ODZjZDI4ZTIyM2I2OTktMDRm"
#aur_inp = "http://10.91.86.180"
#alg_inp = "chet"
#aps_inp = "9letmein"


def nvfis_getgcred():
    login = nlg_inp
    password = nps_inp
    url = nurl_inp
    t_creds = (login, password, url)
    if isinstance(t_creds, tuple):
        return login, password, url
    else:
        raise TypeError("missing credientials of nvfis devices")


def spark_GetArgs():
    token = tk_inp
    # add other variables as needed and return
    if isinstance(token, str):
        return token
    else:
        raise TypeError("Spark token must be a string")


def apic_GetArgs():
    # enter in your credentials for your APIC
    a_url = aur_inp
    a_login = alg_inp
    a_password = aps_inp
    return a_url, a_login, a_password


class HelperFunctionTests(unittest.TestCase):
    def test_001_valid_type_is_returned(self):
        print "Executing test {}".format(self)
        test = nvfis_getgcred()
        self.assertIsInstance(test, tuple)

    def test_002_valid_type_is_returned(self):
        print "Executing test {}".format(self)
        test = spark_GetArgs()
        self.assertIsInstance(test, str)

    def test_003_valid_type_is_returned(self):
        print "Executing test {}".format(self)
        test = apic_GetArgs()
        self.assertIsInstance(test, tuple)


x = nvfis_getgcred()
print type(x)
print x
unittest.main()



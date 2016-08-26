status_resp = str(lan_ip_page)
find_code = status_resp.find('200')
status_resp = status_resp[find_code:find_code + 3]
print status_resp


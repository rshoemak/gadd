

import json

# adding test to see if we want to build a separate file for nvfis_data or make it part of main...

def test_nvfis(s, url):
    r_message = "Logged into NFVis and looking at images"
    u = url + "/api/config/esc_datamodel/images"
    page = s.get(u)
    r_imgs = json.loads(page.content)
    #do_message_(message)
    return r_imgs, r_message
    # stuff to work with parsing
    # resp = img['images']['image']
    # resp = page.json()
    # return resp
    # resp = page.content  #open format print out for reference



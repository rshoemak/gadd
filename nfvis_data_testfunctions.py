
import json
# import requests


# adding test to see if we want to build a separate file for nvfis_data or make it part of main...
def test_nvfis(s, url):
    r_message = "Logged into NFVis and looking at images"
    u = url + "/api/config/esc_datamodel/images"
    page = s.get(u)
    r_imgs = json.loads(page.content)

    # do_message_(message)
    return r_imgs, r_message
    # stuff to work with parsing
    # resp = img['images']['image']
    # resp = page.json()
    # return resp
    # resp = page.content  #open format print out for reference


# Registering VM images - ok
# need variable to provide img name into the function call.
def nfv_register_vm_img(s, url, img):
    img_name = "an_image_name" # place holder,
    file_path = 'file://full_path/{}'.format(img)
    #print file_path
    u = url + "/api/config/esc_datamodel/images"
    vm_reg_data = '{"image": {"name": "%s", "src": "%s" }}' % (img_name, file_path)
    r_reg_vm_images = s.post(u, data=vm_reg_data)
    print r_reg_vm_images
    #print vm_reg_data


# Verify VM images status -ok
def nfv_verify_vm_img(s, url, img, deep_key):
    if deep_key:
        u = url + '/api/operational/esc_datamodel/opdata/images/image/{}?deep'.format(img)
    else:
        u = url + '/api/operational/esc_datamodel/opdata/images/image/{}'.format(img)
    vm_image_page = s.get(u)
    r_vm_image_page = json.loads(vm_image_page.content)
    print r_vm_image_page
    #r_name = r_vm_image_page['esc:images']['image'][1]
    #print "This method is walking the json string: " + str(r_name)
    print u

    '''
    print "\nFOR LOOP"
    for k in r_vm_image_page:
        print k, r_vm_image_page[k]

    print "\nLIST cmd from r_vm_image_page"
    print list(r_vm_image_page)

    print "\n\n\nfor loop k.v items"
    for k, v in r_vm_image_page.items():
        print k, v


    print "\n\n\nfor loop .VALUES"
    for d in r_vm_image_page.values():
        got_d =  d['image']
        print got_d
        print type(got_d)
        got_list = list(got_d)
        print got_list

        print "*****************"
        A = list(got_d[0].values())
        B = list(got_d[1].values())
        C = list(got_d[2].values())
        print A
        print B
        print C

        print "\n\n\n***********ENUMERATE*"
        for index, item in enumerate(got_list):
                print index, item

        print "\n LIST COMPHREENSION"
        print [d['name'] for d in got_list]


        print "\nLOOPS LIST COMP to match a name"
        for d in got_list:
            if d['name'] == "asav951-CLUS-v2.ova":
                print d['name']

    '''

# NEEDS WORK - do we keep?
def nfv_view_vm_cfg(s, url):
    u = url + "/api/config/esc_datamodel/images"
    vm_image_config_page = s.get(u)
    r_vm_image_config_page = json.loads(vm_image_config_page.content)
    print r_vm_image_config_page


# Assign a port to a LAN Bridge - ok
def nfv_assign_port_lanbridge(s, url, br_name):
    prt ="e33" # static for now, do we make this dynamic
    u = url + "/api/config/bridges/bridge/lan-br"
    asgn_lanbridge_data = '{"bridge": {"name": "%s", "port": "%s" }}' % (br_name, prt)
    #r_asgn_lanbridge_page = s.put(u, data=asgn_lanbridge_data)
    #print r_asgn_lanbridge_page
    print asgn_lanbridge_data


# verify lan bridges - ok
def nfv_verify_lanbridge(s, url, deep_key):
    if deep_key:
        u = url + "/api/config/bridges?deep"
    else:
        u = url + "/api/config/bridges"
    lanbridge_page = s.get(u)
    r_lanbridge_page = json.loads(lanbridge_page.content)
    print r_lanbridge_page

# create new bridge - ok
def nfv_create_newbridge(s, url, new_bridge):
    u = url + "/api/config/bridges"
    make_bridge_payload = '{ "bridge": {"name": "%s" }}' % (new_bridge)
    r_create_bridge = s.post(u, data=make_bridge_payload)
    print r_create_bridge
    # print make_bridge_payload

# Create new network and map bridge to network
def nfv_create_new_network(s, url, new_network, new_bridge):
    u = url + "/api/config/networks"
    createnet_payload = '{ "network": {"name": "%s" , "bridge": "%s" }}' %(new_network, new_bridge)
    r_create_net = s.post(u, data=createnet_payload)
    print r_create_net


# verify networks - ok
def nfv_verify_networks(s, url, deep_key):
    if deep_key:
        u = url + "/api/config/networks?deep"
    else:
        u = url + "/api/config/networks"
    networks_page = s.get(u)
    r_networks_page = json.loads(networks_page.content)
    print r_networks_page


# deploy asa
def nfv_deploy_asa(s, url):
    u = url + "/api/config/esc_datamodel/tenants/tenant/admin/deployments"
    asa_config_data = {}
    r_deploy_asa_page = s.post(u, data=asa_config_data)
    print r_deploy_asa_page


# verify deployment status - ok
def nfv_verify_asa_deployment(s, url, device, deep_key):
    if deep_key:
        u = url + '/api/operational/esc_datamodel/opdata/tenants/tenant/admin/deployments/{},-,-?deep'.format(device)
    else:
        # get all devices
        s.headers = ({'Content-type': 'application/vnd.yang.data+json',
                      'Accept': 'application/vnd.yang.collection+json'})
        u = url + '/api/operational/esc_datamodel/opdata/tenants/tenant/admin/deployments/'
        print u
    asa_deployment_page = s.get(u)
    r_asa_deployment_page = json.loads(asa_deployment_page.content)
    print r_asa_deployment_page


def service_chain_csr_asa(s, url):
    pass

# following is experiments on parsing data.
def testing_nested_dict():
    dd = {u'esc:images':
             {u'image': [{u'name': u'asav941-203'},
                         {u'name': u'asav951-CLUS-v2.ova'},
                         {u'name': u'isrv-03.16.01a.S.ova'}
                         ]
              }
         }

    #print type(dd)
    #print dd['esc:images']['image'][2]

    for d in dd.values():
        print "A"
        got_d =  d['image']
        print got_d
        print type(got_d)

    print "\nLIST COMP\n"
    print [d['name'] for d in got_d]

    print "\nLOOPS LIST COMP to match a name"
    for d in got_d:
        if d['name'] == "asav951-CLUS-v2.ova":
            print d['name']


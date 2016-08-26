
import json
import requests


# Registering VM images
def old_nfv_reg_vmimage_nvfis(s, url):
    # r_message = "Posting an image"
    u = url + "/api/config/esc_datamodel/images"
    vm_reg_data = {} # example vm_reg_data = {'test': 'this', 'taste': 'that', 'tic': 'tac'}
    r_reg_vm_images = s.post(u, data=vm_reg_data)
    print r_reg_vm_images


# Verify VM images status
def old_nfv_verify_vmimage_nvfis(s, url):
    u = url + "/api/operational/esc_datamodel/opdata/images"
    vm_image_page = s.get(u)
    r_vm_image_page = json.loads(vm_image_page.content)
    print r_vm_image_page


# Get image config - do we need this - TBD?
def old_nfv_get_image_config(s, url):
    u = url + "/api/config/esc_datamodel/images"
    vm_image_config_page = s.get(u)
    r_vm_image_config_page = json.loads(vm_image_config_page.content)
    print r_vm_image_config_page


# OLD - Assign a port to a LAN Bridge (DELETE)
def old_nfv_assign_port_lan_bridge(s, url):
    u = url + "/api/config/bridges/bridge/lan-br"
    asgn_lanbridge_data = {}
    r_asgn_lanbridge_page = s.put(u, data=asgn_lanbridge_data)
    print r_asgn_lanbridge_page


# verify lan bridges - TBD
def old_nfv_verify_port_lan_bridge(s, url):
    u = url + "/api/config/bridges"
    lanbridge_page = s.get(u)
    r_lanbridge_page = json.loads(lanbridge_page.content)
    print r_lanbridge_page


# OLD - create new lan bridge (DELETE)
def old_nfv_create_new_bridge(s, url, new_bridge):
    u = url + "/api/config/bridges"
    make_bridge_payload = '{ \"bridge\": {\"name\": "%s" }}' %(new_bridge)
    r_create_bridge = s.post(u, data=make_bridge_payload)
    print r_create_bridge
    # print make_bridge_payload


# verify networks
def old_nfv_verify_networks(s, url):
    u = url + "/api/config/networks"
    networks_page = s.get(u)
    r_networks_page = json.loads(networks_page.content)
    print r_networks_page


# deploy asa
def old_nfv_deploy_asa(s, url):
    u = url + "/api/config/esc_datamodel/tenants/tenant/admin/deployments"
    asa_config_data = {}
    r_deploy_asa_page = s.post(u, data=asa_config_data)
    print r_deploy_asa_page


# verify deployment status - not working but hard to test... error status 404
# need new hearders. application./vnd.collection
# OLD (DELETE)
def old_nfv_verify_asa_deployment(s, url):
    u = url + "/api/operational/esc_datamodel/opdata/tenants/tenant/admin/deployments"
    s.headers = ({'Content-type': 'application/vnd.yang.data+json', 'Accept': 'application/vnd.yang.collection+json'})
    asa_deployment_page = s.get(u)
    r_asa_deployment_page = json.loads(asa_deployment_page.content)
    print r_asa_deployment_page


# ###################   -- Build new functions here --  ####################

# verify deployment status - ok
def nfv_verify_device_deployment(s, url, device, deep_key):
    if deep_key:
        # Get a specific device, verbose
        u = url + '/api/operational/esc_datamodel/opdata/tenants/tenant/admin/deployments/{},-,-?deep'.format(device)
    else:
        # Get all devices, non-verbose
        s.headers = ({'Content-type': 'application/vnd.yang.data+json',
                      'Accept': 'application/vnd.yang.collection+json'})
        u = url + '/api/operational/esc_datamodel/opdata/tenants/tenant/admin/deployments/'
    asa_deployment_page = s.get(u)
    r_asa_deployment_page = json.loads(asa_deployment_page.content)

    # Set headers back to default
    s.headers = ({'Content-type': 'application/vnd.yang.data+json', 'Accept': 'application/vnd.yang.data+json'})
    return r_asa_deployment_page


# Prune name and name_id - ok
def nfv_prune_name(s, url):
    dd = nfv_verify_device_deployment(s, url, device=False, deep_key=False)

    dev_name_id = ""
    dev_name = ""

    for ix in dd.values():
        got_lsta = ix['esc:deployments']
        ix_lstb = [x['vm_group'][0] for x in got_lsta]
        ix_lstc = [y['name'] for y in ix_lstb]
        dev_name = ix_lstc[0]

        if dev_name == "ROUTER":    # Need to assume CSR's have some default name convention. Needs work...
            dev_name_src = [x['deployment_name'] for x in got_lsta]
            dev_name_id = dev_name_src[0]

    return dev_name, dev_name_id

# To_Do create function for Step 2: get LAN IP

# To_Do Prune flavor of image for Step 3
def nfv_prune_flavor(s, url, device_name_id):
    # /api/config/esc_datamodel/tenants/tenant/admin/deployments?deep
    # Match on device_name_id to get the flavor type


# Create LAN Bridge - ok (verify this with Ryan's version)
def nfv_create_newbridge(s, url, new_bridge):
    u = url + "/api/config/bridges"
    make_bridge_payload = '{ "bridge": {"name": "%s" }}' % new_bridge
    r_create_bridge = s.post(u, data=make_bridge_payload)
    return r_create_bridge  # do we need to return r_create_bridge or just do a return?


# Create new network and map to lan bridge
def nfv_create_new_network(s, url, new_network, new_bridge):
    u = url + "/api/config/networks"
    createnet_payload = '{ "network": {"name": "%s" , "bridge": "%s" }}' %(new_network, new_bridge)
    r_create_net = s.post(u, data=createnet_payload)
    return r_create_net     # do we need to return r_create_net of just do a return?




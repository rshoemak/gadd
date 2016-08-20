
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


# Registering VM images
def reg_vmimage_nvfis(s, url):
    # r_message = "Posting an image"
    u = url + "/api/config/esc_datamodel/images"
    vm_reg_data = {} # example vm_reg_data = {'test': 'this', 'taste': 'that', 'tic': 'tac'}
    r_reg_vm_images = s.post(u, data=vm_reg_data)
    print r_reg_vm_images


# Verify VM images status
def verify_vmimage_nvfis(s, url):
    u = url + "/api/operational/esc_datamodel/opdata/images"
    vm_image_page = s.get(u)
    r_vm_image_page = json.loads(vm_image_page.content)
    print r_vm_image_page


def get_image_config(s, url):
    u = url + "/api/config/esc_datamodel/images"
    vm_image_config_page = s.get(u)
    r_vm_image_config_page = json.loads(vm_image_config_page.content)
    print r_vm_image_config_page


# Assign a port to a LAN Bridge
def assign_port_lan_bridge(s, url):
    u = url + "/api/config/bridges/bridge/lan-br"
    asgn_lanbridge_data = {}
    r_asgn_lanbridge_page = s.put(u, data=asgn_lanbridge_data)
    print r_asgn_lanbridge_page


# verify lan bridges
def verify_port_lan_bridge(s, url):
    u = url + "/api/config/bridges"
    lanbridge_page = s.get(u)
    r_lanbridge_page = json.loads(lanbridge_page.content)
    print r_lanbridge_page


def create_new_bridge(s, url, new_bridge):
    u = url + "/api/config/bridges"
    make_bridge_payload = '{ \"bridge\": {\"name\": "%s" }}' %(new_bridge)
    r_create_bridge = s.post(u, data=make_bridge_payload)
    print r_create_bridge
    # print make_bridge_payload


# verify networks
def verify_networks(s, url):
    u = url + "/api/config/networks"
    networks_page = s.get(u)
    r_networks_page = json.loads(networks_page.content)
    print r_networks_page


# deploy asa
def deploy_asa(s, url):
    u = url + "/api/config/esc_datamodel/tenants/tenant/admin/deployments"
    asa_config_data = {}
    r_deploy_asa_page = s.post(u, data=asa_config_data)
    print r_deploy_asa_page


# verify deployment status - not working but hard to test... error status 404
# need new hearders. application./vnd.collection
def verify_asa_deployment(s, url):
    u = url + "/api/operational/esc_datamodel/opdata/tenants/tenant/admin/deployments"
    s.headers = ({'Content-type': 'application/vnd.yang.data+json', 'Accept': 'application/vnd.yang.collection+json'})
    asa_deployment_page = s.get(u)
    r_asa_deployment_page = json.loads(asa_deployment_page.content)
    print r_asa_deployment_page


def service_chain_csr_asa(s, url):
    pass

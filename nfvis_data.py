
import json
# from pprint import pprint

# ###################   -- Build new functions here --  ####################



# Possible DELETE - really not sure but might be redundant
def get_vm_cfg(s, url, dev_id):
    u = url + '/api/config/esc_datamodel/tenants/tenant/admin/deployments?deep'
    vm_flavor_page = s.get(u)
    r_vm_flavor_page = json.loads(vm_flavor_page.content)

    for i in r_vm_flavor_page.values():
        got_lsta = i['deployment'][0]['name']
        if got_lsta == dev_id:
            return r_vm_flavor_page
        else:
            print "Can't find device: %s " % dev_id
            return False


################### Start DEV5 updating of APIs ######################

# Step 1a - Get counts of VMs deployed
def nfv_get_count_of_vm_deployments(s, url):
    # pre-release api as follows:
    # u = url + '/api/config/esc_datamodel/tenants/tenant/admin/deployments'
    # new api replaces 'esc_datamodel' with 'vm_lifecycle':
    u = url + '/api/config/vm_lifecycle/tenants/tenant/admin/deployments'
    count_vm_deployed_page = s.get(u)
    # print u
    # print count_vm_deployed_page
    r_count_vm_deployed_page = json.loads(count_vm_deployed_page.content)

    for iv in r_count_vm_deployed_page.values():
        vm_deployed_lst = iv['deployment']
        vm_deployed_count = len(vm_deployed_lst)
        return vm_deployed_count


# Step 1b - Get CSR flavor and dev_name_id and vm_name_id - ok
def nfv_get_csr_cfg(s, url, r_vm_deployed_count):
    count = 0
    # u = url + '/api/config/esc_datamodel/tenants/tenant/admin/deployments?deep'
    u = url + '/api/config/vm_lifecycle/tenants/tenant/admin/deployments?deep'
    vm_flavor_page = s.get(u)
    r_vm_flavor_page = json.loads(vm_flavor_page.content)

    csr_flav = ""
    csr_dev_name_id = ""
    csr_vm_name = ""
    while count < r_vm_deployed_count:
        # Assumption is the CSR is the first deployed VM
        for i in r_vm_flavor_page.values():
            flav = i['deployment'][count]['vm_group'][0]['flavor']
            if 'csr' in flav:
                csr_dev_name_id = i['deployment'][count]['name']
                csr_vm_name = i['deployment'][count]['vm_group'][0]['name']
                csr_flav = i['deployment'][count]['vm_group'][0]['flavor']
            count += 1
    return csr_flav, csr_dev_name_id, csr_vm_name


# Pre Step 2 - verify deployment status
def nfv_verify_device_deployment(s, url, device, deep_key):
    if deep_key:
        # Get a specific device, verbose
        # u = url + '/api/operational/esc_datamodel/opdata/tenants/tenant/admin/deployments/{},-,-?deep'.format(device)
        u = url + '/api/operational/vm_lifecycle/opdata/tenants/tenant/admin/deployments/{},-,-?deep'.format(device)
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


# Step 2 - Get LAN IP - ok
def nfv_prune_bvi_ip(s, url, r_csr_id):
    data = nfv_verify_device_deployment(s, url, device=r_csr_id, deep_key=True)

    bvi_gw = ""
    lan_net = ""
    bvi_ip = ""

    for ix in data.values():
        got_lsta = ix['vm_group'][0]['vm_instance'][0]['interfaces']['interface']
        bvi_gw = got_lsta[2]['gateway']
        lan_net = got_lsta[2]['network']

    if 'lan' in lan_net:
        lan_ip_tmp = bvi_gw.split('.')
        bvi_ip = lan_ip_tmp[0] + '.' + lan_ip_tmp[1] + '.' + lan_ip_tmp[2] + '.' + "2"
    return bvi_ip, bvi_gw

# Step 3 - get ASA Flavor
def nfv_get_asa_flavor(r_flavor):
    if 'large' in r_flavor:
        return "ASAv30"
    elif 'medium' in r_flavor:
        return "ASAv10"
    elif 'small' in r_flavor:
        return "ASAv5"
    else:
        return False


# Step 5 - Create LAN Bridge (verify this with Ryan's version)
def nfv_create_newbridge(s, url, new_bridge):
    u = url + "/api/config/bridges"
    make_bridge_payload = '{ "bridge": {"name": "%s" }}' % new_bridge
    r_create_bridge = s.post(u, data=make_bridge_payload)
    if '201' in r_create_bridge:
        return True
    else:
        return r_create_bridge


# Step 6 - Create new network and map to lan bridge
def nfv_create_new_network(s, url, new_network, new_bridge):
    u = url + "/api/config/networks"
    createnet_payload = '{ "network": {"name": "%s" , "bridge": "%s" }}' % (new_network, new_bridge)
    r_create_net = s.post(u, data=createnet_payload)
    return r_create_net


# Step 7A - Assign VNF interface to a Network
def nfv_assign_vnf_network(s, url, r_csr_id, new_network):
    print r_csr_id
    print type(r_csr_id)
    print new_network
   # u = url + "/api/config/esc_datamodel/tenants/tenant/admin/deployments/deployment/%s/vm_group/ROUTER/interfaces"\
   #           % r_csr_id
    u = url + "/api/config/vm_lifecycle/tenants/tenant/admin/deployments/deployment/{}/vm_group/ISRv/interfaces".format(r_csr_id)
    print u
    asgn_net_payload = '{ "interfaces": { "interface": [ {"nicid": "0", "network": "int-mgmt-net" }, ' \
                       '{ "nicid": "1", "network": "wan-net" }, { "nicid": "2",  "network": "%s" }, ' \
                       '{ "nicid": "3",  "network": "mgmt-net"  } ] }}' % new_network

    asgn_net = s.put(u, data=asgn_net_payload)
    r_asgn_net = str(asgn_net)
    print r_asgn_net
    if "204" in r_asgn_net:
        return True
    else:
        return False














# DELETE ? Get VM Flavor
def nfv_prune_flavor(s, url, dev_id):
    d_flav = get_vm_cfg(s, url, dev_id)

    flavor = ""
    if d_flav:
        for idx in d_flav.values():
            got_lsta = idx['deployment'][0]['vm_group']
            got_lstb = [x['flavor'] for x in got_lsta]
            flavor = got_lstb[0]
        return flavor
    else:
        return False














# deploy asa
def nfv_deploy_asa(s, url, r_created_input_cfg):
    u = url + "/api/config/esc_datamodel/tenants/tenant/admin/deployments"
    with open(r_created_input_cfg, 'rb') as asa_config_data:
        deployed_asa_page = s.post(u, data=asa_config_data)
        r_deployed_asa_page = str(deployed_asa_page)
    if "201" in r_deployed_asa_page:
        return True
    else:
        return False

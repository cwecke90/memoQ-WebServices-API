from zeep import Client, helpers
from lxml import etree

headers = etree.XML('<header><ApiKey>OfUcxbUHzaa40AHPOJL0vST3CDmtkn0wVlwC1Qe0</ApiKey></header>')

client_serverproject = Client(wsdl='https://dp-dhl.memoqworld.com:8081/memoqservices/ServerProject?wsdl')
client_tm_management = Client(wsdl='https://dp-dhl.memoqworld.com:8081/memoqservices/tm?wsdl')
client_memoqusers = Client(wsdl='https://dp-dhl.memoqworld.com:8081/memoqservices/security?wsdl')


def list_active_server_projects(service_url):
    list_of_projects = []
    response = service_url.service.ListProjects(_soapheaders=[*headers])
    for projects in response:
        input_dict = helpers.serialize_object(projects, dict)
        if input_dict["ProjectStatus"] == "Live":
            list_of_projects.append(input_dict["Name"])
    print(f"{len(list_of_projects)} active server projects!")
    return list_of_projects


print(list_active_server_projects(client_serverproject))


def get_list_of_server_tms(service_url_tm):
    list_of_tms = []
    response = service_url_tm.service.ListTMs(_soapheaders=[*headers])
    for tm in response:
        input_dict_2 = helpers.serialize_object(tm, dict)
        guid = input_dict_2["Guid"]
        response_new = service_url_tm.service.GetTMInfo(guid, _soapheaders=[*headers])
        list_of_tms.append(response_new["Name"])
    print(f"{len(list_of_tms)} server TMs!")
    return list_of_tms


print(get_list_of_server_tms(client_tm_management))


def get_list_of_server_users(service_url):
    list_of_users = []
    response = service_url.service.ListUsers(_soapheaders=[*headers])
    for users in response:
        input_dict = helpers.serialize_object(users, dict)
        list_of_users.append(input_dict["UserName"])
    print(f"{len(list_of_users)} server users!")
    return list_of_users


print(get_list_of_server_users(client_memoqusers))
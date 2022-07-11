from zeep import Client, helpers
from lxml import etree
import os

os.environ["https_proxy"] = "http://cloudproxy.dhl.com:10123"

headers = etree.XML('<header><ApiKey>OfUcxbUHzaa40AHPOJL0vST3CDmtkn0wVlwC1Qe0</ApiKey></header>')

client_server_project = Client(wsdl='https://dp-dhl.memoqworld.com:8081/memoqservices/ServerProject?wsdl')
client_tm_management = Client(wsdl='https://dp-dhl.memoqworld.com:8081/memoqservices/tm?wsdl')


def get_list_of_active_server_projects(service_url):
    list_of_projects = []
    response = service_url.service.ListProjects(_soapheaders=[*headers])
    for projects in response:
        input_dict = helpers.serialize_object(projects, dict)
        if input_dict["ProjectStatus"] == "Live":
            list_of_projects.append(input_dict["Name"])
    return list_of_projects


def get_list_of_server_tms(service_url_tm):
    list_of_tms = set()
    response = service_url_tm.service.ListTMs(_soapheaders=[*headers])
    for tm in response:
        input_dict_2 = helpers.serialize_object(tm, dict)
        guid = input_dict_2["Guid"]
        response_new = service_url_tm.service.GetTMInfo(guid, _soapheaders=[*headers])
        if "_Master_" not in response_new["Name"] and "MT_Self-service" not in response_new["Name"]:
            list_of_tms.add(response_new["Name"])
    return list_of_tms


def compare_active_projects_with_active_tms(service_url_tm, service_url):
    tm_set = set()
    project_set = set()
    for tm in get_list_of_server_tms(service_url_tm):
        single_tm = tm.split("-")
        tm_project_number = single_tm[0].strip()
        tm_set.add(tm_project_number)
    for project in get_list_of_active_server_projects(service_url):
        single_project = project.split("-")
        single_project_number = single_project[0].strip()
        project_set.add(single_project_number)
    differences = tm_set.difference(project_set)
    print(f"{len(project_set)} active unique server projects!")
    print(f"{len(tm_set)} active unique project server TMs!")
    print(differences)


compare_active_projects_with_active_tms(client_tm_management, client_server_project)

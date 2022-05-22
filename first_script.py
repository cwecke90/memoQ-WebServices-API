import requests
from zeep import Client, helpers
import suds
import pandas as pd
from lxml import etree
#
# api_key = "OfUcxbUHzaa40AHPOJL0vST3CDmtkn0wVlwC1Qe0"


headers = etree.XML('<header><ApiKey>OfUcxbUHzaa40AHPOJL0vST3CDmtkn0wVlwC1Qe0</ApiKey></header>')

client_serverproject = Client(wsdl='https://dp-dhl.memoqworld.com:8081/memoqservices/ServerProject?wsdl')
# client_memoqusers = Client(wsdl='https://dp-dhl.memoqworld.com:8081/memoqservices/security?wsdl')
client_tmmanagement = Client(wsdl='https://dp-dhl.memoqworld.com:8081/memoqservices/tm?wsdl')

# response = client_serverproject.service.ListProjects(_soapheaders=[*headers])
#
# for r in response:
#     input_dict = helpers.serialize_object(r, dict)
#     if input_dict["ProjectStatus"] != "WrappedUp":
#         if input_dict["DocumentStatus"] == "TranslationFinished" or "ProofreadingFinished":
#             print(input_dict)

response_tm = client_tmmanagement.service.ListTMs(_soapheaders=[*headers])

for tm in response_tm:
    input_dict_2 = helpers.serialize_object(tm, dict)
    guid = input_dict_2["Guid"]
    response_new = client_tmmanagement.service.GetTMInfo(guid, _soapheaders=[*headers])
    if "Master" in response_new["Name"]:
        if "MT+PE" not in response_new["Name"]:
            print(response_new["Name"], response_new["Guid"])

# response = client_memoqusers.service.ListUsers(_soapheaders=[*headers])
# for r in response:
#     input_dict = helpers.serialize_object(r, dict)
#     print(input_dict)

# response = client_tmmanagement.service.GetTMInfo(_soapheaders=[*headers])

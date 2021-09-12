import requests
from requests.auth import HTTPBasicAuth # or HTTPDigestAuth, or OAuth1, etc.
from requests import Session
from zeep import Client
from zeep.transports import Transport
from zeep.wsse.username import UsernameToken

def getClient(username,password):
    session = Session()
    session.auth = HTTPBasicAuth(username, password)
    webstaging='https://ws.staging.training.gov.au/Deewr.Tga.Webservices/OrganisationServiceV8.svc?wsdl'
    websandpit='https://ws.sandbox.training.gov.au/Deewr.Tga.WebServices/OrganisationServiceV2.svc?wsdl'
    #client = Client('https://ws.staging.training.gov.au/Deewr.Tga.Webservices/OrganisationServiceV8.svc?wsdl',
    #             transport=Transport(session=session))
    client = Client(websandpit,
        wsse=UsernameToken(username, password))
    return client

def test_factory_namespace(client,rtacode):
    string_array_type = client.get_type('ns1:OrganisationDetailsRequest')
    #node = client.create_message(client.service, 'ns1:OrganisationDetailsRequest', user='WebService.Read')
    request = string_array_type()
    request.Code = rtacode
    request.IncludeLegacyData = 0
    request.InformationRequested = [{
    "ShowCodes" : 1,
    "ShowContacts" : 0,
    "ShowExplicitScope" : 1,
    "ShowDataManagers" : 0,
    "ShowImplicitScope" : 0,
    "ShowLocations" : 0,
    "ShowRegistrationManagers" : 0,
    "ShowRegistrationPeriods" : 0,
    "ShowResponsibleLegalPersons" : 0,
    "ShowRestrictions" : 0,
    "ShowRtoClassifications" : 0,
    "ShowRtoDeliveryNotification" : 0,
    "ShowTradingNames" : 1,
    "ShowUrls" : 0
        }]
    print(request)
    obj=client.service.GetDetails(request)
    print(obj)
    #this is very handy for eeryone to understand the wsdl structure
    #obj=client.wsdl.dump()
    #print(client.service.GetDetails())
    obj=1
    return obj

def getOrganisations():
    baseurl = 'https://ws.staging.training.gov.au/Deewr.Tga.Webservices/OrganisationServiceV8.svc?wsdl'
    client = Client(baseurl)
    s=1
    return s

def main():
    print("start Jk")
    user='WebService.Read'
    password ='Asdf098'
    client = getClient(user,password)
    org = test_factory_namespace(client,rtacode=40735)
    print(org)

if __name__ == "__main__":
    main()

print("finish")
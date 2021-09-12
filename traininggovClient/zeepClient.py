import os
import requests
from requests.auth import HTTPBasicAuth # or HTTPDigestAuth, or OAuth1, etc.
from requests import Session
from zeep import Client
from zeep.transports import Transport
from zeep.wsse.username import UsernameToken
import pandas as pd
from zeep.helpers import serialize_object
from datetime import datetime
from pytz import timezone

def getUrl(env,context):
    url=''
    if env=='sandpit':
        if (context=='Organisation'):
            url='https://ws.sandbox.training.gov.au/Deewr.Tga.WebServices/OrganisationServiceV2.svc?wsdl'
        elif (context=='TrainingCompnent'):
            url='https://ws.sandbox.training.gov.au/Deewr.Tga.Webservices/TrainingComponentServiceV9.svc?wsdl'
        elif (context=='Classification'):
            url='https://ws.sandbox.training.gov.au/Deewr.Tga.Webservices/ClassificationServiceV9.svc?wsdl'

    elif env=='staging':
        if (context=='Organisation'):
            url='https://ws.staging.training.gov.au/Deewr.Tga.Webservices/OrganisationServiceV8.svc?wsdl'
    return url


def getClient(url,username,password):
    session = Session()
    session.auth = HTTPBasicAuth(username, password)
    client = Client(url,
        wsse=UsernameToken(username, password))
    return client
def getWsdldump(client):
    #this is very handy function to understand the wsdl structure
    obj=client.wsdl.dump()

def getcurrtime():
    # Current time in UTC
    now_utc = datetime.now(timezone('UTC'))
    # Convert to AEST
    curr_time = now_utc.astimezone(timezone('Australia/Victoria'))
    return curr_time

def getoutdir(context):
    outdir=f'./output/{context}'
    if not os.path.exists(outdir):
        print('inside if')
        os.mkdir(outdir)
    return outdir


def writecsv(dataframe,context,filename):
    outdir=getoutdir(context)
    outname=f'{filename}_'+str(getcurrtime().strftime('%Y%m%d%H%M%S'))+'.csv'
    fullname = os.path.join(outdir, outname)
    print(fullname)
    dataframe.to_csv(fullname, index = None, header=True)

def addDataFrame(dataframe,colname,colvalue):
    dataframe[colname] = colvalue
    return dataframe


def getDataFrame(zeepObject):
    data = serialize_object(zeepObject)
    df=pd.DataFrame(data)
    return df

def getTrainingComponentDetails(client,nrtcode):
    string_array_type = client.get_type('ns1:TrainingComponentDetailsRequest')
    request = string_array_type()
    request.Code = nrtcode
    obj=client.service.GetDetails(request)
    nrtCompletionList= obj.CompletionMapping.NrtCompletion
    df1=getDataFrame(nrtCompletionList)
    print(obj.ComponentType)
    releaseList=obj.Releases.Release
    latestRelease=len(releaseList)
    latestReleaseobject=releaseList[0]
    for i in releaseList:
        if(i.ReleaseNumber==str(latestRelease)):
            latestReleaseobject=i
    unitList=latestReleaseobject.UnitGrid.UnitGridEntry
    df2=getDataFrame(unitList)
    df2=addDataFrame(df2,'ReleaseNumber',latestReleaseobject.ReleaseNumber)
    df2=addDataFrame(df2,'ReleaseDate',latestReleaseobject.ReleaseDate)
    loadtime=str(getcurrtime().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3])
    df2=addDataFrame(df2,'LoadTime',loadtime)
    unitdf = pd.merge(df1, df2, on='Code')
    writecsv(unitdf,'Classification',nrtcode)

    return obj

def getOrganisationalDetails(client,rtacode):
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
    tradingName=obj.TradingNames.TradingName[0].Name
    scopelist=obj.Scopes.Scope
    scopedf=getDataFrame(scopelist)
    loadtime=str(getcurrtime().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3])
    scopedf=addDataFrame(scopedf,'TradingName',tradingName)
    scopedf=addDataFrame(scopedf,'LoadTime',loadtime)
    writecsv(scopedf,'Organisation',f'Scopelist_{rtacode}')
    #print(scopedf)
    #print(client.service.GetDetails())
    return scopelist


def main():
    user='WebService.Read'
    password ='Asdf098'
    env='sandpit'
    context='Organisation'
    tryUrl= getUrl(env,'Organisation')
    if(not (tryUrl and not tryUrl.isspace())):
        print ("No Url found")
    else :
        client = getClient(tryUrl,user,password)
        #List the structure of the Wsdl
        #getWsdldump(client)
        #The below function gets the list of Scope in the Organisation. [If there is a scope list it writes to output as csv inherently]
        scopelist = getOrganisationalDetails(client,rtacode=40735)
        print(0)
    context='TrainingCompnent'
    tryUrl= getUrl(env,context)
    if(not (tryUrl and not tryUrl.isspace())):
        print ("No Url found")
    else :
        client = getClient(tryUrl,user,password)
        #List the structure of the Wsdl
        #getWsdldump(client)
        #The below function gets the list of Scope in the Organisation. [If there is a scope list it writes to output as csv inherently]
        #print(scopelist)
        for i in scopelist:
            print(i.TrainingComponentType[0])
            if(i.TrainingComponentType[0]=='Qualification'):
                unitlist = getTrainingComponentDetails(client,nrtcode=i.NrtCode)

if __name__ == "__main__":
    main()

print("finish")
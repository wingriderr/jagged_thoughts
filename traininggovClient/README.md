# Training Gov Methods
This module reads the Training gov sandpit environment. As this is a public repo, prod wsdls not added.

### Run `python zeepClient.py -h` for help


Options:

| Parameters | #Description  |
| :----- | :- |
|  -h, --help     |       show this help message and exit |
|  -a AUTO, --auto=AUTO | Automode- Default 0,0->Disable,1->Enable|
|  -m MANUAL, --manual=MANUAL| Manual mode- Default 0,0->Disable,1->Enable|
|  --rtacode=RTACODELIST|rtacode list provided in comma seperated with single quotes|
|  --nrtcode=NRTCODELIST| nrtcode list provided in comma seperated with single quotes|


### Sample argument passing 
For **auto** ,rtacode is Mandatory. 

For manual **Nrtcode** is mandatory.

Sample1: ` python zeepClient.py --auto 1 --rtacode '40735'`

Sample1: ` python zeepClient.py --manual 1 --nrtcode 'BSB50215,BSB50420'`


## Details of the environment
- Based on python3
- install pip
- install zeep
- ~~install ullib~~
- install requests
- install pandas.

## getOrganisationalDetails
- input - rtacode
- Lists the Scopelist in the response and converts to csv

## getTrainingComponentDetails
- input nrtcode
- Main function invokes getTrainingComponentDetails() for each scopelist
- Only parses for **TrainingComponentType='Qualification'** 
- i.e doesnt parse *AccreditedCourse* and *Unit*

## general
- writes into output folder
- ~~output folder should be present,havent written handler for that.~~
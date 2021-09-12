# Training Gov Methods
This module reads the Training gov sandpit environment. As this is a public repo, prod wsdls not added.
## Details of the environment
- Based on python3
- install pip
- install zeep
- install ullib
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
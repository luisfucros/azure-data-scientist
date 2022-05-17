from azureml.core import Workspace
from azureml.core.webservice import AksWebservice

# Get workspace
ws = Workspace.get(name='aml-workspace',
                   subscription_id='703026c4-95fb-4a79-b674-b1648c8d0c13',
                   resource_group='aml-resources')

# Get the deployed service
service = AksWebservice(name='diabetes-service', workspace=ws)

# Check its state
print(service.state)

# Review service logs
print(service.get_logs())

# Predict 
import json

# An array of new data cases
x_new = [[0.1,2.3,4.1,2.0],
         [0.2,1.8,3.9,2.1]]

# Convert the array to a serializable list in a JSON document
json_data = json.dumps({"data": x_new})

# Call the web service, passing the input data
response = service.run(input_data = json_data)

# Get the predictions
predictions = json.loads(response)

# Print the predicted class for each case.
for i in range(len(x_new)):
    print (x_new[i], predictions[i])


# Use REST endpoint to predict
endpoint = service.scoring_uri
print(endpoint)

import requests
import json

x_new = [[2,180,74,24,21,23.9091702,1.488172308,22],
         [0,148,58,11,179,39.19207553,0.160829008,45]]

# Convert the array to a serializable list in a JSON document
input_json = json.dumps({"data": x_new})

# Set the content type
headers = { 'Content-Type':'application/json' }

predictions = requests.post(endpoint, input_json, headers = headers)
predicted_classes = json.loads(predictions.json())

for i in range(len(x_new)):
    print ("Patient {}".format(x_new[i]), predicted_classes[i] )
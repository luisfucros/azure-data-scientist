
from azureml.core import Workspace
from azureml.core.webservice import AksWebservice

# Get workspace
ws = Workspace.get(name='aml-workspace',
                   subscription_id='703026c4-95fb-4a79-b674-b1648c8d0c13',
                   resource_group='aml-resources')

# Get the deployed service
service = AksWebservice(name='diabetes-service', workspace=ws)

# Delete service
service.delete()
print ('Service deleted.')
from azureml.core import Workspace, Datastore

# Get workspace
ws = Workspace.get(name='aml-workspace',
                   subscription_id='703026c4-95fb-4a79-b674-b1648c8d0c13',
                   resource_group='aml-resources')

# Register a new datastore
blob_ds = Datastore.register_azure_blob_container(workspace=ws, 
                                                  datastore_name='blob_data', 
                                                  container_name='azureml-blobstore-e54c8546-f320-41f5-9eab-7f569d74ae8b',
                                                  account_name='amlworksstorage24e3ba8a8',
                                                  account_key='GJwS+tm0YF2RjYVmZDglS7OynAEeR8/J11Bk6CtiMePKOe8Y8ftjbxoJbsrSLk2LLMbJ+uVZkAj4+AStXQ1XRw==')
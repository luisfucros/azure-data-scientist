from azureml.core import Workspace, Datastore

# Get workspace
ws = Workspace.get(name='aml-workspace',
                   subscription_id='703026c4-95fb-4a79-b674-b1648c8d0c13',
                   resource_group='aml-resources')

# Register a new datastore
blob_ds = Datastore.register_azure_blob_container(workspace=ws, 
                                                  datastore_name='blob_data', 
                                                  container_name='azureml-blobstore-4254b06d-d493-4bdb-bc43-9661de2fad87', # A string of the name of the Azure blob container (storage account containers)
                                                  account_name='amlworkspace3364491769', # A string of the storage account name (storage account resource name)
                                                  account_key='6kXu4JxHwRSjd2kXdMNhdZsEQRZC5X4MRUTtxkOl0xxv4u30GhQbtYcWPhi2GuMuVaVoJcArZYMR+AStw1kXZQ==') # A string of the storage account key (storage account access keys)
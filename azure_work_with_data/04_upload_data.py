from azureml.core import Workspace, Datastore

# Get workspace
ws = Workspace.get(name='aml-workspace',
                   subscription_id='703026c4-95fb-4a79-b674-b1648c8d0c13',
                   resource_group='aml-resources')

# Get the default datastore
default_ds = ws.get_default_datastore()

default_ds.upload_files(files=['./data/diabetes.csv'], # Upload the diabetes csv files in /data
                       target_path='diabetes-data/', # Put it in a folder path in the datastore
                       overwrite=True, # Replace existing files of the same name
                       show_progress=True)
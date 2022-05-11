from azureml.core import Workspace, Datastore

# Get workspace
ws = Workspace.get(name='aml-workspace',
                   subscription_id='703026c4-95fb-4a79-b674-b1648c8d0c13',
                   resource_group='aml-resources')

ws.set_default_datastore('blob_data')
# workspaceblobstore

# Get the default datastore
default_ds = ws.get_default_datastore()

for ds_name in ws.datastores:
    print(ds_name, "- Default =", ds_name == default_ds.name)
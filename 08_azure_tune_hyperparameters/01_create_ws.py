from azureml.core import Workspace

# Create workspace
     
ws = Workspace.create(name='aml-workspace', 
                      subscription_id='703026c4-95fb-4a79-b674-b1648c8d0c13',
                      resource_group='aml-resources',
                      create_resource_group=True,
                      location='eastus'
                     )

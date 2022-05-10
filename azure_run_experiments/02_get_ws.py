from azureml.core import Workspace

# Get workspace
ws = Workspace.get(name='aml-workspace',
                   subscription_id='703026c4-95fb-4a79-b674-b1648c8d0c13',
                   resource_group='aml-resources')

# List compute targets
for compute_name in ws.compute_targets:
    compute = ws.compute_targets[compute_name]
    print(compute.name, ":", compute.type)
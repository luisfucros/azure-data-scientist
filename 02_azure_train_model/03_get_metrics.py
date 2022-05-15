from azureml.core import Workspace, Experiment, ScriptRunConfig, Environment
from azureml.core.authentication import InteractiveLoginAuthentication

interactive_auth = InteractiveLoginAuthentication(tenant_id="99e1e721-7184-498e-8aff-b2ad4e53c1c2")

ws = Workspace.get(name='aml-workspace',
            subscription_id='703026c4-95fb-4a79-b674-b1648c8d0c13',
            resource_group='aml-resources',
            location='East US',
            auth=interactive_auth
            )
experiment = Experiment(workspace=ws, name='training-experiment')

# Get the latest run of the experiment
run = list(experiment.get_runs())[0]

# Get logged metrics
print("\nMetrics:")
metrics = run.get_metrics()
for key in metrics.keys():
        print(key, metrics.get(key))
    
# Get a link to the experiment in Azure ML studio   
experiment_url = experiment.get_portal_url()
print('See details at', experiment_url)
from azureml.core import Workspace, Environment, Model
from azureml.core.model import InferenceConfig
from azureml.core.webservice import AciWebservice

# Get workspace
ws = Workspace.get(name='aml-workspace',
                   subscription_id='703026c4-95fb-4a79-b674-b1648c8d0c13',
                   resource_group='aml-resources')

# Specify a model
model = ws.models['diabetes_model']
print(model.name, 'version', model.version)

# Configure the scoring environment
service_env = Environment(name='service-env')
python_packages = ['scikit-learn', 'azureml-defaults', 'azure-ml-api-sdk'] # whatever packages your entry script uses
for package in python_packages:
    service_env.python.conda_dependencies.add_pip_package(package)

# Represents configuration settings for a custom environment used for deployment
inference_config = InferenceConfig(source_directory='./diabetes_service',
                                   entry_script='score_diabetes.py',
                                   environment=service_env)

# Configure the web service container
deployment_config = AciWebservice.deploy_configuration(cpu_cores=1, memory_gb=1)

# Deploy the model as a service
print('Deploying model...')
service_name = "diabetes-service"
service = Model.deploy(ws, service_name, [model], inference_config, deployment_config, overwrite=True)
service.wait_for_deployment(True)
print(service.state)

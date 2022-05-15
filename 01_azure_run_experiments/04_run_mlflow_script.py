from azureml.core import Workspace, Experiment, ScriptRunConfig, Environment
from azureml.core.runconfig import DockerConfiguration
# from azureml.widgets import RunDetails
from azureml.core.authentication import InteractiveLoginAuthentication

interactive_auth = InteractiveLoginAuthentication(tenant_id="99e1e721-7184-498e-8aff-b2ad4e53c1c2")

ws = Workspace.get(name='aml-workspace',
            subscription_id='703026c4-95fb-4a79-b674-b1648c8d0c13',
            resource_group='aml-resources',
            location='East US',
            auth=interactive_auth
            )

# Create a Python environment for the experiment (from a .yml file)
env = Environment.from_conda_specification("aml-env", "./.azureml/aml-env.yml")

# Create a script config
script_mlflow = ScriptRunConfig(source_directory='./src',
                                script='mlflow_diabetes.py',
                                environment=env,
                                docker_runtime_config=DockerConfiguration(use_docker=True),
                                compute_target='cpu-cluster') 

# submit the experiment
experiment = Experiment(workspace=ws, name='mslearn-diabetes-mlflow')
run = experiment.submit(config=script_mlflow)
# RunDetails(run).show()
run.wait_for_completion()

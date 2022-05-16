from azureml.core import Workspace
from azureml.core import Environment
from azureml.core.compute import ComputeTarget
from azureml.core.runconfig import RunConfiguration
from azureml.data import OutputFileDatasetConfig
from azureml.pipeline.steps import PythonScriptStep
from azureml.core import Experiment
from azureml.pipeline.core import Pipeline
# from azureml.widgets import RunDetails

# Get workspace
ws = Workspace.from_config(path='./.azureml/config.json')

# Get the most recent run of the pipeline
pipeline_experiment = ws.experiments.get('mslearn-diabetes-pipeline')
run = list(pipeline_experiment.get_runs())[0]

# Publish the pipeline from the run
published_pipeline = run.publish_pipeline(name='diabetes-training-pipeline',
                                          description='Trains diabetes model',
                                          version='1.0')

rest_endpoint = published_pipeline.endpoint
print(rest_endpoint)

import requests
from azureml.core.authentication import InteractiveLoginAuthentication

interactive_auth = InteractiveLoginAuthentication()
auth_header = interactive_auth.get_authentication_header()
print("Authentication header ready.")

experiment_name = 'mslearn-diabetes-pipeline'

rest_endpoint = published_pipeline.endpoint
response = requests.post(rest_endpoint, 
                         headers=auth_header, 
                         json={"ExperimentName": experiment_name})
run_id = response.json()["Id"]
print(run_id)
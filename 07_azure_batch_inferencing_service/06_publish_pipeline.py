from azureml.core import Workspace, Experiment
from azureml.core.authentication import InteractiveLoginAuthentication
from azureml.pipeline.core.run import PipelineRun
import pandas as pd
import requests
import os


# Get workspace
ws = Workspace.from_config(path='./.azureml/config.json')

# Get the most recent run of the pipeline
pipeline_experiment = ws.experiments.get('mslearn-diabetes-batch')
run = list(pipeline_experiment.get_runs())[0]

published_pipeline = run.publish_pipeline(
    name='diabetes-batch-pipeline', description='Batch scoring of diabetes data', version='1.0')

print(published_pipeline)

rest_endpoint = published_pipeline.endpoint
print(rest_endpoint)

interactive_auth = InteractiveLoginAuthentication()
auth_header = interactive_auth.get_authentication_header()
print('Authentication header ready.')

rest_endpoint = published_pipeline.endpoint
response = requests.post(rest_endpoint, 
                         headers=auth_header, 
                         json={"ExperimentName": "mslearn-diabetes-batch"})
run_id = response.json()["Id"]
print(run_id)

published_pipeline_run = PipelineRun(ws.experiments['mslearn-diabetes-batch'], run_id)

# Block until the run completes
published_pipeline_run.wait_for_completion(show_output=True)
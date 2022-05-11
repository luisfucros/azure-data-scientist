from azureml.core import Experiment, ScriptRunConfig, Environment
from azureml.core.runconfig import DockerConfiguration
#from azureml.widgets import RunDetails
from azureml.core import Workspace, Dataset

# Get workspace
ws = Workspace.get(name='aml-workspace',
                   subscription_id='703026c4-95fb-4a79-b674-b1648c8d0c13',
                   resource_group='aml-resources')

# Create a Python environment for the experiment (from a .yml file)
env = Environment.from_conda_specification("aml-env", "./.azureml/aml-env.yml")

# Get the training dataset
diabetes_ds = ws.datasets.get("diabetes dataset")

# Create a script config
script_config = ScriptRunConfig(source_directory='./src',
                              script='diabetes_training.py',
                              arguments = ['--regularization', 0.1, # Regularizaton rate parameter
                                           '--input-data', diabetes_ds.as_named_input('training_data')], # Reference to dataset
                              environment=env,
                              compute_target='cpu-cluster',
                              docker_runtime_config=DockerConfiguration(use_docker=True)) 

# submit the experiment
experiment_name = 'mslearn-train-diabetes'
experiment = Experiment(workspace=ws, name=experiment_name)
run = experiment.submit(config=script_config)
#RunDetails(run).show()
run.wait_for_completion()
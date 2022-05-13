from azureml.core import Workspace, Environment, Experiment, ScriptRunConfig
from azureml.core.runconfig import DockerConfiguration
# from azureml.widgets import RunDetails

# Get workspace
ws = Workspace.get(name='aml-workspace',
                   subscription_id='703026c4-95fb-4a79-b674-b1648c8d0c13',
                   resource_group='aml-resources')

# Create a Python environment for the experiment (from a .yml file)
experiment_env = Environment.from_conda_specification("aml-env", "./.azureml/aml-env.yml")

# Let Azure ML manage dependencies
experiment_env.python.user_managed_dependencies = False 

# Print the environment details
print(experiment_env.name, 'defined.')
print(experiment_env.python.conda_dependencies.serialize_to_string())

# Register the environment
experiment_env.register(workspace=ws)

# Get the training dataset
diabetes_ds = ws.datasets.get("diabetes dataset")

# Create a script config
script_config = ScriptRunConfig(source_directory='./src',
                                script='diabetes_training.py',
                                arguments = ['--regularization', 0.1, # Regularizaton rate parameter
                                             '--input-data', diabetes_ds.as_named_input('training_data')], # Reference to dataset
                                environment=experiment_env,
                                compute_target='cpu-cluster',
                                docker_runtime_config=DockerConfiguration(use_docker=True)) # Use docker to host environment

# submit the experiment
experiment_name = 'mslearn-train-diabetes'
experiment = Experiment(workspace=ws, name=experiment_name)
run = experiment.submit(config=script_config)
# RunDetails(run).show()
run.wait_for_completion()
from azureml.core import Workspace, Experiment, ScriptRunConfig, Environment
from azureml.core.conda_dependencies import CondaDependencies

# Get workspace
ws = Workspace.get(name='aml-workspace',
                   subscription_id='703026c4-95fb-4a79-b674-b1648c8d0c13',
                   resource_group='aml-resources')

# Create a Python environment for the experiment
sklearn_env = Environment("sklearn-env")

# Ensure the required packages are installed
packages = CondaDependencies.create(conda_packages=['scikit-learn', 'pandas','pip'],
                                    pip_packages=['azureml-defaults', 'azureml-core'])
sklearn_env.python.conda_dependencies = packages

# Create a script config
script_config = ScriptRunConfig(source_directory='./src',
                                script='diabetes_training.py',
                                environment=sklearn_env,
                                compute_target='cpu-cluster') 

# Submit the experiment
experiment = Experiment(workspace=ws, name='training-experiment')
run = experiment.submit(config=script_config)
run.wait_for_completion()
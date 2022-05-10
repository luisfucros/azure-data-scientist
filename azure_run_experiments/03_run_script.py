from azureml.core import Workspace, Experiment, ScriptRunConfig, Environment
from azureml.core.authentication import InteractiveLoginAuthentication

interactive_auth = InteractiveLoginAuthentication(tenant_id="99e1e721-7184-498e-8aff-b2ad4e53c1c2")

ws = Workspace.get(name='aml-workspace',
            subscription_id='703026c4-95fb-4a79-b674-b1648c8d0c13',
            resource_group='aml-resources',
            location='East US',
            auth=interactive_auth
            )

# Create a script config
script_config = ScriptRunConfig(source_directory='./src',
                                script='experiment.py',
                                compute_target='cpu-cluster') 

# Environment
env = Environment.from_conda_specification(
        name='aml-env',
        file_path='./.azureml/aml-env.yml'
    )
script_config.run_config.environment = env

# submit the experiment
experiment = Experiment(workspace = ws, name = 'my-experiment')
run = experiment.submit(config=script_config)
run.wait_for_completion(show_output=True)
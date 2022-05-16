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

# Create a Python environment for the experiment (from a .yml file)
experiment_env = Environment.from_conda_specification("aml-env", "./.azureml/aml-env.yml")

# Register the environment 
experiment_env.register(workspace=ws)
registered_env = Environment.get(ws, 'aml-env')

# Create a new runconfig object for the pipeline
pipeline_run_config = RunConfiguration()

cluster_name = 'cpu-cluster'
pipeline_cluster = ComputeTarget(workspace=ws, name=cluster_name)

# Use the compute you created above. 
pipeline_run_config.target = pipeline_cluster

# Assign the environment to the run configuration
pipeline_run_config.environment = registered_env

print ("Run configuration created.")

# Get the training dataset
diabetes_ds = ws.datasets.get("diabetes dataset")

# Create an OutputFileDatasetConfig (temporary Data Reference) for data passed from step 1 to step 2
prepped_data = OutputFileDatasetConfig("prepped_data")

# Step 1, Run the data prep script
prep_step = PythonScriptStep(name = "Prepare Data",
                                source_directory = './src',
                                script_name = "prep_diabetes.py",
                                arguments = ['--input-data', diabetes_ds.as_named_input('raw_data'),
                                             '--prepped-data', prepped_data],
                                compute_target = pipeline_cluster,
                                runconfig = pipeline_run_config,
                                allow_reuse = True)

# Step 2, run the training script
train_step = PythonScriptStep(name = "Train and Register Model",
                                source_directory = './src',
                                script_name = "train_diabetes.py",
                                arguments = ['--training-data', prepped_data.as_input()],
                                compute_target = pipeline_cluster,
                                runconfig = pipeline_run_config,
                                allow_reuse = True)

print("Pipeline steps defined")

# Construct the pipeline
pipeline_steps = [prep_step, train_step]
pipeline = Pipeline(workspace=ws, steps=pipeline_steps)
print("Pipeline is built.")

# Create an experiment and run the pipeline
experiment = Experiment(workspace=ws, name = 'mslearn-diabetes-pipeline')
pipeline_run = experiment.submit(pipeline, regenerate_outputs=True)
print("Pipeline submitted for execution.")
# RunDetails(pipeline_run).show()
pipeline_run.wait_for_completion(show_output=True)

# Publish the pipeline from the run
published_pipeline = pipeline_run.publish_pipeline(
    name="diabetes-training-pipeline", description="Trains diabetes model", version="1.0")

print(published_pipeline)
from azureml.core import Workspace, Environment
from azureml.core.runconfig import DEFAULT_CPU_IMAGE
from azureml.pipeline.steps import ParallelRunConfig, ParallelRunStep
from azureml.data import OutputFileDatasetConfig
from azureml.core import Experiment
from azureml.pipeline.core import Pipeline
import pandas as pd
import shutil
import os

# Load the workspace from the saved config file
ws = Workspace.from_config()

# Create an Environment for the experiment
batch_env = Environment.from_conda_specification("experiment_env", ".azureml/batch_environment.yml")
# batch_env.docker.base_image = DEFAULT_CPU_IMAGE
print('Configuration ready.')

# Get the dataset
batch_data_set = ws.datasets.get("batch-data")

output_dir = OutputFileDatasetConfig(name='inferences')

parallel_run_config = ParallelRunConfig(
    source_directory='./batch_pipeline',
    entry_script="batch_diabetes.py",
    mini_batch_size="5",
    error_threshold=10,
    output_action="append_row",
    environment=batch_env,
    compute_target='cpu-cluster',
    node_count=2)

parallelrun_step = ParallelRunStep(
    name='batch-score-diabetes',
    parallel_run_config=parallel_run_config,
    inputs=[batch_data_set.as_named_input('diabetes_batch')],
    output=output_dir,
    arguments=[],
    allow_reuse=True
)

print('Steps defined')

pipeline = Pipeline(workspace=ws, steps=[parallelrun_step])
pipeline_run = Experiment(ws, 'mslearn-diabetes-batch').submit(pipeline)
pipeline_run.wait_for_completion(show_output=True)

# Get the run for the first step and download its output
prediction_run = next(pipeline_run.get_children())
prediction_output = prediction_run.get_output_data('inferences')
prediction_output.download(local_path='diabetes-results')

# Traverse the folder hierarchy and find the results file
for root, dirs, files in os.walk('diabetes-results'):
    for file in files:
        if file.endswith('parallel_run_step.txt'):
            result_file = os.path.join(root,file)

# cleanup output format
df = pd.read_csv(result_file, delimiter=":", header=None)
df.columns = ["File", "Prediction"]

# Display the first 20 results
print(df.head(20))
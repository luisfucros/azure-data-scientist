from azureml.core import Workspace, Dataset, Run
import pandas as pd
import os

subscription_id = '703026c4-95fb-4a79-b674-b1648c8d0c13'
resource_group = 'aml-resources'
workspace_name = 'aml-workspace'

workspace = Workspace(subscription_id, resource_group, workspace_name)

# Get the experiment run context
run = Run.get_context()

# load the diabetes dataset
data = Dataset.get_by_name(workspace, name='diabetes-data')
data = data.to_pandas_dataframe()

# Count the rows and log the result
row_count = (len(data))
run.log('observations', row_count)

# Save a sample of the data
os.makedirs('outputs', exist_ok=True)
data.sample(100).to_csv("outputs/sample.csv", index=False, header=True)

# Complete the run
run.complete()
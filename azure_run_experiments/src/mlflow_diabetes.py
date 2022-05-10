from azureml.core import Workspace, Dataset, Run
import pandas as pd
import mlflow

subscription_id = '703026c4-95fb-4a79-b674-b1648c8d0c13'
resource_group = 'aml-resources'
workspace_name = 'aml-workspace'

workspace = Workspace(subscription_id, resource_group, workspace_name)

# start the MLflow experiment
with mlflow.start_run():
       
    # Load data
    data = Dataset.get_by_name(workspace, name='diabetes-data')
    data = data.to_pandas_dataframe()

    # Count the rows and log the result
    row_count = (len(data))
    print('observations:', row_count)
    mlflow.log_metric('observations', row_count)
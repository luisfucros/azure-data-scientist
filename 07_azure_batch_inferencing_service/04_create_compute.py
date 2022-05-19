from azureml.core import Workspace
from azureml.core.compute import ComputeTarget, AmlCompute
from azureml.core.compute_target import ComputeTargetException

# Load the workspace from the saved config file
ws = Workspace.from_config()

cluster_name = "your-compute-cluster"

try:
    # Check for existing compute target
    inference_cluster = ComputeTarget(workspace=ws, name=cluster_name)
    print('Found existing cluster, use it.')
except ComputeTargetException:
    # If it doesn't already exist, create it
    try:
        compute_config = AmlCompute.provisioning_configuration(vm_size='STANDARD_DS11_V2', max_nodes=2)
        inference_cluster = ComputeTarget.create(ws, cluster_name, compute_config)
        inference_cluster.wait_for_completion(show_output=True)
    except Exception as ex:
        print(ex)
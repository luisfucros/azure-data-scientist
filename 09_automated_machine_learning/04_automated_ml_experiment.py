from azureml.core import Workspace
import azureml.train.automl.utilities as automl_utils
from azureml.train.automl import AutoMLConfig
from azureml.core.experiment import Experiment
from azureml.core import Model

# Get workspace
ws = Workspace.from_config(path='./.azureml/config.json')

# Split the dataset into training and validation subsets
diabetes_ds = ws.datasets.get("diabetes dataset")
train_ds, test_ds = diabetes_ds.random_split(percentage=0.7, seed=123)
print("Data ready!")

# Get classification metrics
for metric in automl_utils.get_primary_metrics('classification'):
    print(metric)

automl_config = AutoMLConfig(name='Automated ML Experiment',
                             task='classification',
                             compute_target='cpu-cluster',
                             training_data = train_ds,
                             validation_data = test_ds,
                             label_column_name='Diabetic',
                             iterations=4,
                             primary_metric = 'AUC_weighted',
                             max_concurrent_iterations=2,
                             featurization='auto'
                             )

print("Ready for Auto ML run.")



# Experiment
print('Submitting Auto ML experiment...')
automl_experiment = Experiment(ws, 'mslearn-diabetes-automl-sdk')
automl_run = automl_experiment.submit(automl_config)
automl_run.wait_for_completion(show_output=True)

# View child run details
for run in automl_run.get_children():
    print('Run ID', run.id)
    for metric in run.get_metrics():
        print('\t', run.get_metrics(metric))

# Best run
best_run, fitted_model = automl_run.get_output()
print(best_run)
print('\nBest Model Definition:')
print(fitted_model)
print('\nBest Run Transformations:')
for step in fitted_model.named_steps:
    print(step)
print('\nBest Run Metrics:')
best_run_metrics = best_run.get_metrics()
for metric_name in best_run_metrics:
    metric = best_run_metrics[metric_name]
    print(metric_name, metric)

# Register model
best_run.register_model(model_path='outputs/model.pkl', model_name='diabetes_model',
                        tags={'Training context':'Auto ML'},
                        properties={'AUC': best_run_metrics['AUC_weighted'], 'Accuracy': best_run_metrics['accuracy']})

# List registered models
for model in Model.list(ws):
    print(model.name, 'version:', model.version)
    for tag_name in model.tags:
        tag = model.tags[tag_name]
        print ('\t',tag_name, ':', tag)
    for prop_name in model.properties:
        prop = model.properties[prop_name]
        print ('\t',prop_name, ':', prop)
    print('\n')

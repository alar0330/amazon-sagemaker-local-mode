# This is a sample Python program that runs a simple scikit-learn processing on data fetched from Delta Lake.
# The output of the processing will be total_cases per location.
# This implementation will work on your *local computer*.
#
# Prerequisites:
#   1. Install required Python packages:
#       pip install boto3 sagemaker pandas scikit-learn
#       pip install 'sagemaker[local]'
#   2. Docker Desktop has to be installed on your computer, and running.
#   3. Open terminal and run the following commands:
#       docker build -t sagemaker-delta-lake-processing-local container/.
########################################################################################################################

from sagemaker.local import LocalSession
from sagemaker.processing import ScriptProcessor, ProcessingInput, ProcessingOutput

sagemaker_session = LocalSession()
sagemaker_session.config = {'local': {'local_code': True}}

# For local training a dummy role will be sufficient
role = 'arn:aws:iam::111111111111:role/service-role/AmazonSageMaker-ExecutionRole-20200101T000001'

processor = ScriptProcessor(command=['python3'],
                    image_uri='sagemaker-delta-lake-processing-local',
                    role=role,
                    instance_count=1,
                    instance_type='local')

processor.run(code='processing_script.py',
                    inputs=[ProcessingInput(
                        source='./profile/',
                        destination='/opt/ml/processing/profile/')],
                    outputs=[ProcessingOutput(
                        output_name='delta_lake_processed_data',
                        source='/opt/ml/processing/processed_data/')]
                    )

preprocessing_job_description = processor.jobs[-1].describe()
output_config = preprocessing_job_description['ProcessingOutputConfig']

print(output_config)

for output in output_config['Outputs']:
    if output['OutputName'] == 'delta_lake_processed_data':
        delta_lake_processed_data_file = output['S3Output']['S3Uri']

print('Output file is located on: {}'.format(delta_lake_processed_data_file))
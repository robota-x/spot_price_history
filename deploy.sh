# create zip files
mkdir -p deploy_packages

echo 'creating deploy pkg for orchestrator...'
cd spot_orchestrator
zip -r9 ../deploy_packages/orchestrator.zip .
cd -

echo 'creating deploy pkg for parser...'
cd spot_parser
zip -r9 ../deploy_packages/parser.zip .
cd -

echo 'creating deploy pkg for writer...'
cd spot_writer
zip -r9 ../deploy_packages/writer.zip .
cd -

# upload to lambda
echo 'deploying all functions to lambda...'
aws lambda update-function-code --profile spot --function-name spot_orchestrator --zip-file fileb://deploy_packages/orchestrator.zip
aws lambda update-function-code --profile spot --function-name spot_parser --zip-file fileb://deploy_packages/parser.zip
aws lambda update-function-code --profile spot --function-name spot_writer --zip-file fileb://deploy_packages/writer.zip

# upload to s3
if [ ! -z "$LIST_TARGET" ] 
then 
    echo 'uploading requirements list to s3...'
    aws s3 cp --profile spot required_data.json s3://$LIST_TARGET
fi

echo 'all done!'

# initial cleanup
rm -rf deploy_packages
mkdir -p deploy_packages

ROOT_DIR=$(pwd)

echo 'creating deploy pkg for orchestrator...'
cd $ROOT_DIR/spot_orchestrator/env/lib/python3.6/site-packages/ 
zip -qr9 $ROOT_DIR/deploy_packages/orchestrator.zip . -x \*pip/\* \*setuptools/\* \*wheel/\* \*__pycache__/\*
cd $ROOT_DIR/spot_orchestrator
zip -g9 $ROOT_DIR/deploy_packages/orchestrator.zip handler.py config.ini

echo 'creating deploy pkg for parser...'
cd $ROOT_DIR/spot_parser/env/lib/python3.6/site-packages/
zip -qr9 $ROOT_DIR/deploy_packages/parser.zip . -x \*pip/\* \*setuptools/\* \*wheel/\* \*__pycache__/\*
cd $ROOT_DIR/spot_parser
zip -g9 $ROOT_DIR/deploy_packages/parser.zip handler.py config.ini msg_pb2.py

echo 'creating deploy pkg for writer...'
cd $ROOT_DIR/spot_writer/env/lib/python3.6/site-packages/
zip -qr9 $ROOT_DIR/deploy_packages/writer.zip . -x \*pip/\* \*setuptools/\* \*wheel/\* \*__pycache__/\*
cd $ROOT_DIR/spot_writer
zip -g9 $ROOT_DIR/deploy_packages/writer.zip handler.py config.ini msg_pb2.py

# upload to lambda
echo 'deploying all functions to lambda...'
cd $ROOT_DIR
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

# AWS spot price visualiser

This should be a small and fast (ahah) project to present the ec2 spot pricing data in a single page.

General architecture: aws endpoint -> lambda (cron) -> aurora serverless -> (cron bokeh lambda?) -> static page on cloudfront/s3? 
Maybe orchestrate everything with step functions

## Installation

* requires pymysql to be shipped alongside the package (run `pip install pymysql --target .` inside the /spot_parser folder)
* requires a json file on s3 containing a list of required instances/zones. sample:
    ```json
    {
        "instance_types": ["t1.micro", "t2.micro"],
        "availability_zones": [ "eu-west-1a", "eu-west-1b"]
    }
    ```
* requires a config.ini file inside the spot_parser to specify local/aws db connections. sample:
    ```
    [DEFAULT]
    db=<your db name>
    charset=utf8

    [local]
    host=localhost
    user=<local username>
    password=<local password>  # if present

    [aws]
    host=localhost
    user=<local username>
    password=<local password>  # if present
    ```
* requires a config.ini file inside the spot_orchestrator to specify aws s3 bucket containing config and parser lambda name. sample:
    ```
    [aws]
    s3_bucket=<bucket name>
    requirements_object=<key of requirements.json file in bucket>
    parser_function=<arn or qualifying name for the parser lambda>
    ```

## Running

There is a small debug section in the parser and orchestrator handler functions so that running `python handler.py` should simulate an event. Lambda and DB interaction is **not mocked**.

TODO: proper dev env (maybe aws sam local?)
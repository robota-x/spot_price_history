# AWS spot price visualiser

This should be a small and fast (ahah) project to present the ec2 spot pricing data in a single page.

General architecture: aws endpoint -> lambda (cron) -> aurora serverless -> [api gateway] -> static page on cloudfront/s3?

## Installation

* requires pymysql to be shipped alongside the package (run `pip install pymysql --target .` inside the /spot_parser folder)
* requires a config.ini file inside the spot_parser to specify local/aws db connections. sample:
    ```
    [DEFAULT]
    db=<your_db_name>
    charset=utf8

    [local]
    host=localhost
    user=<local_username>
    password=<local_password>  # if present

    [aws]
    host=localhost
    user=<local_username>
    password=<local_password>  # if present
    ```

# Running

There is a small debug section in the parser's handler so that running `python handler.py` should simulate an event. DB interaction is **not mocked**

TODO: proper dev env (maybe aws sam local?)
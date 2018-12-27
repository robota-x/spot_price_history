# AWS spot price visualiser

This should be a small and fast (ahah) project to present the ec2 spot pricing data in a single page.

General architecture: aws endpoint -> lambda (cron) -> s3/dynamo? -> [api gateway] -> static page on cloudfront
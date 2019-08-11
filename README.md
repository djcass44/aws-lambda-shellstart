# Shellstart

This repository contains an AWS Lambda used for updating a docker-compose deployment.
This script was written using Python3.6 and therefore will probably not work with Python2.

### Clarify 'updating'

Updating in this context means the following:

1. Stop the container(s)
2. Pull for newer images
3. Start the container using the new image

The actual shell which is executed is `docker-compose stop && docker-compose pull && docker-compose up -d`, however it allows for more fine-grained control of which containers to update.


### Lambda Event Data
```json
{
  "s3": {
    "key": "my-key.pem",
    "bucket": "my-s3-bucket"
  },
  "ssh": {
    "target": "192.168.0.1",
    "user": "ec2-user",
    "directory": "/home/ec2-user/production"
  },
  "containers": [
    "my-app-ui",
    "my-app-api"
  ]
}
```

`ssh.target`: the host to SSH into. Can be IP or hostname

`ssh.directory`: the directory of the docker-compose.yaml/yml

`containers`: (optional) the containers to update. All if not provided

### How is it done?

1. Download SSH key from S3
2. SSH into your target
3. Execute docker-compose commands


## Contributions

Go for it! Open a merge request and I'll take a look.
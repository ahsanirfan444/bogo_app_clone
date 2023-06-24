# Hubur Socket

## Local Development

### Setup

The hubur socket code is build using Django channels and its structure is very simple and optimized.
The code consists 2 files under sockets/settings. Each individual file contains the settings of specific enviroment. For local development use local.py and for production use pro.py.


To run this code locally, use below commands on your anaconda terminal or bash.


```bash
$ python -m venv .env
$ pip install -r requirements.txt
$ python manage.py runserver
```

This should create everything you need from scratch including a Python virtual
environment, installation of dependencies.


## Production Deployment

This project is hosted on AWS's Elasticbeanstalk Enviroment. The deployment of this project happens from terminal through the pip package installer awsebcli. This package installer requries AWS ACCESS KEY and AWS SECRET KEY to access AWS IAM Account. This instances are deployed on the Singapore region. To deploy the code, run the following command.

```bash
$ eb init
```

* This will ask you the provide AWS ACCESS KEY and AWS SECRET KEY for the first time.
* Then will ask you to provide region (In our case Singapore)
* Then select the server (hubur_sockets)
* Then it'll ask permission for the codeCommit feature of AWS. We've not configured this feature with git repo. So just input `n` here.
* And That's it :)
* After it, run the following command.

```bash
$ eb deploy
```
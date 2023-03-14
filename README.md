# Hubur

## Local Development

### Setup

The hubur code structure is very simple and optimized.
The code consists 3 files under hubur/settings. Each individual file contains the settings of specific enviroment. For local development use local.py, for development use dev.py and finally for production use pro.py.


To run this code locally, use below commands on your anaconda terminal or bash.


```bash
$ pip install -r requirements.txt
$ python manage.py makemigrations
$ python manage.py migrate
$ python manage.py runserver
```

To add some temporary data into database, use below commands on your anaconda terminal or bash.


```bash
$ python manage.py loaddata fixtures/data.json
$ python manage.py loaddata fixtures/devices.json
```

This should create everything you need from scratch including a Python virtual
environment, installation of dependencies, and the loading of database fixtures
into a local sqlite database.

| Username                    | Description           | Password      |
|-----------------------------|-----------------------|---------------|
| superuser_hubur@example.com | Superuser access      |  ZXC!asd123   |
| admin_hubur@example.com     | Admin access          |  ZXC!asd123   |
| test_vendor@example.com     | Vendor access         |  ZXC!asd123   |


## Production Deployment

This project is hosted on AWS's Elasticbeanstalk Enviroment. The deployment of this project happens from terminal through the pip package installer awsebcli. This package installer requries AWS ACCESS KEY and AWS SECRET KEY to access AWS IAM Account. The all 2 EB instances are deployed on the Singapore region. To deploy the code, run the following command.

```bash
$ eb deploy
```

* This will ask you the provide AWS ACCESS KEY and AWS SECRET KEY for the first time.
* Then will ask you to provide region (In our case Singapore)
* Then select the server (DEV, PRO)
* Then it'll ask permission for the codeCommit feature of AWS. We've not configured this feature with git repo. So just input `n` here.
* And That's it :)


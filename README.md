# Project Title

Alexa Flight RDS skill

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

Alexa developer console  
AWS Lambda  

### Installing

Follow [this](https://github.com/alexa/skill-sample-python-helloworld-classes) from official Hellow World example to set up alexa skill and lambda endpoints  
Follow [this](https://docs.aws.amazon.com/lambda/latest/dg/vpc-rds.html) to configure Lambda function to access RDS
## Deployment

* In JSON editor at [Alexa developer console](https://developer.amazon.com/alexa/console/ask), paste skill.json
* Make a deployment package, and upload it to [AWS Lambda](https://console.aws.amazon.com/lambda/home?region=us-east-1#/functions). Follow [this](https://docs.aws.amazon.com/lambda/latest/dg/lambda-python-how-to-create-deployment-package.html) to make a deployment package  
* In your lambda, set environment variables  
db_host: endpoint of RDS  
db_name: your DB name (you can find this in your RDS configuration tab)  
db_password: password  
db_username: username  

## Built With

* [Ask-sdk-core](https://github.com/alexa/alexa-skills-kit-sdk-for-python) - Alexa skill kit
* [PyMySQL](https://github.com/PyMySQL/PyMySQL) - Pure MySQL client

## Author

* **Masahiro Yoshida**

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Inspiration: creation of Flight Database for database management class at UTD and make a client to utilize it

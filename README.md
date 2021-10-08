# telegram-serverless-meal-bot-framework

## Install serverless framework and plugins
npm install -g serverless
serverless plugin install -n serverless-python-requirements
serverless plugin install -n serverless-apigateway-service-proxy

or npm install

## Deploy solution
sls deploy --token xxx --stage dev

## Setup webhook
curl --request POST --url https://api.telegram.org/bot<bot_token>/setWebhook --header 'content-type: application/json' --data '{"url": "<api_gw_endpoint>"}'

## Clean up
sls remove --stage dev

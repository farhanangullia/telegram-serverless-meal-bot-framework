.PHONY: install
install:
	npm install 

# .PHONY: install-dev
# install-dev: install
# 	pip install -r requirements-dev.txt

.PHONY: deploy
deploy:
	sls deploy --token <token> --stage dev

.PHONY: set-webhook
set-webhook:
	curl --request POST --url https://api.telegram.org/bot<token>/setWebhook --header 'content-type: application/json' --data '{"url": "<url>"}'

.PHONY: fmt
fmt:
	black .

.PHONY: destroy
destroy:
	sls remove --stage dev
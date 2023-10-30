OS := $(shell uname)

ifeq $(OS) Darwin
else
endif

deps:
	curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.5/install.sh | bash
	nvm install 18.0.0
	nvm use 18.0.0
	npm i -g npm@9

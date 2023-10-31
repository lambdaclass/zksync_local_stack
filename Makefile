OS := $(shell uname -s)

deps:
	curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.5/install.sh | bash
	nvm install 18.0.0
	nvm use 18.0.0
	npm i -g npm@9
	npm install --global yarn
	yarn policies set-version 1.22.19
	@if [ ! -n "$(shell which cargo)" ] ; then \
		curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -- -y; \
	fi
	cargo install sqlx-cli --version 0.5.13
	@if [ "$(OS)" = "Darwin" ] ; then \
		brew install axel openssl postgresql tmux \
		&& 	curl -L https://desktop.docker.com/mac/main/$(shell uname -m)/Docker.dmg --output Docker.dmg ; \
	else \
		sudo apt install -y axel libssl-dev postgresql tmux build-essential pkg-config cmake clang lldb lld \
		&& sudo apt-get update \
		&& sudo apt-get install ca-certificates curl gnupg \
		&& sudo install -m 0755 -d /etc/apt/keyrings \
		&& curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg \
		&& sudo chmod a+r /etc/apt/keyrings/docker.gpg
		&& echo \
		  "deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
		  "$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | \
		  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null; \
		sudo apt-get update;
	fi

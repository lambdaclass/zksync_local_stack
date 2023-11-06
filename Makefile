OS := $(shell uname -s)
export ZKSYNC_HOME=$(shell pwd)/zksync-era

deps:
	@if [ "$(OS)" = "Darwin" ]; then \
		brew install axel openssl postgresql tmux; \
		curl -SL https://github.com/docker/compose/releases/download/v2.23.0/docker-compose-linux-x86_64 -o /usr/local/bin/docker-compose; \
		curl -L https://github.com/matter-labs/zksolc-bin/releases/download/v1.3.16/zksolc-macosx-arm64-v1.3.16 --output zksolc; \
		chmod a+x zksolc; \
		curl -L https://github.com/ethereum/solidity/releases/download/v0.8.19/solc-macos --output solc; \
		chmod a+x solc; \
		mkdir -p $(HOME)/Library/Application\ Support/eth-compilers; \
		mv solc $(HOME)/Library/Application\ Support/eth-compilers; \
		mv zksolc $(HOME)/Library/Application\ Support/eth-compilers; \
	else \
		sudo apt update; \
		sudo apt install -y axel libssl-dev postgresql tmux git build-essential pkg-config cmake clang lldb lld; \
		curl -fsSL https://get.docker.com | sh; \
		curl -SL https://github.com/docker/compose/releases/download/v2.23.0/docker-compose-linux-x86_64 -o /usr/local/bin/docker-compose; \
		curl -L https://github.com/matter-labs/zksolc-bin/releases/download/v1.3.16/zksolc-linux-amd64-musl-v1.3.16 --output zksolc; \
		curl -L https://github.com/ethereum/solidity/releases/download/v0.8.19/solc-static-linux --output solc; \
		chmod a+x solc; \
		chmod a+x /usr/local/bin/docker-compose; \
		chmod a+x zksolc; \
		mkdir -p $(HOME)/.config; \
		mv solc $(HOME)/.config; \
		mv zksolc $(HOME)/.config; \
	fi
	@if [ ! -n "$(shell which cargo)" ]; then \
		curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y; \
	fi
	. $(HOME)/.cargo/env; \
	cargo install sqlx-cli --version 0.5.13; \
	rm -rf zksync-era; \
	git clone -b boojum-integration https://github.com/matter-labs/zksync-era; \
	rm -rf block-explorer;
	git clone https://github.com/matter-labs/block-explorer; \
	curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.5/install.sh | bash; \
	. $(HOME)/.nvm/nvm.sh; \
	nvm install 18.0.0; \
	nvm use 18.0.0; \
	npm i -g npm@9; \
	npm install --global yarn; \
	yarn policies set-version 1.22.19; \
	cd ${ZKSYNC_HOME}; \
	./bin/zk; \
	./bin/zk init

run:
	. $(HOME)/.nvm/nvm.sh; \
	. $(HOME)/.cargo/env; \
	@if [ "$(OS)" = "Linux" ]; then \
		sudo service postgresql stop; \
		. $(HOME)/.bashrc; \
	fi \
	tmux kill-session -t zksync-server; \
	tmux new -d -s zksync-server; \
	tmux send-keys -t zksync-server "cd ${ZKSYNC_HOME}" Enter; \
	tmux send-keys -t zksync-server "./bin/zk server" Enter


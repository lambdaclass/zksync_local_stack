OS := $(shell uname -s)
export ZKSYNC_HOME = $(shell pwd)/zksync-era

deps:
	curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.5/install.sh | bash
	. $(HOME)/.nvm/nvm.sh; \
	nvm install 18.0.0; \
	nvm use 18.0.0; \
	npm i -g npm@9; \
	npm install --global yarn; \
	yarn policies set-version 1.22.19
	@if [ "$(OS)" = "Darwin" ]; then \
		brew install axel openssl postgresql tmux; \
		curl -SL https://github.com/docker/compose/releases/download/v2.23.0/docker-compose-linux-x86_64 -o /usr/local/bin/docker-compose; \
		curl -L https://github.com/matter-labs/zksolc-bin/releases/download/v1.3.16/zksolc-macosx-arm64-v1.3.16 --output zksolc; \
		chmod a+x zksolc; \
	else \
		sudo apt update; \
		sudo apt install -y axel libssl-dev postgresql tmux git build-essential pkg-config cmake clang lldb lld; \
		curl -fsSL https://get.docker.com | sh; \
		curl -SL https://github.com/docker/compose/releases/download/v2.23.0/docker-compose-linux-x86_64 -o /usr/local/bin/docker-compose; \
		curl -L https://github.com/matter-labs/zksolc-bin/releases/download/v1.3.16/zksolc-linux-amd64-musl-v1.3.16 --output zksolc; \
		chmod a+x /usr/local/bin/docker-compose; \
		chmod a+x zksolc; \
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

run:
	@if [ "$(OS)" = "Linux" ]; then \
		sudo service postgresql stop; \
	fi
	# Run server
	cd ${ZKSYNC_HOME}; \
	. $(HOME)/.nvm/nvm.sh; \
	. $(HOME)/.cargo/env; \
	./bin/zk; \
	./bin/zk init; \
	tmux new -d -s zksync-server "./bin/zk server"
	
	# Run explorer
	# cd ../block-explorer; \
	# npm install; \
	# npm run hyperchain:configure; \
	# npm run db:create; \
	# npm run dev;

terra-init:
	terraform -chdir=infrastructure/terraform init

terra-apply:
	terraform -chdir=infrastructure/terraform apply 

terra-destroy:
	terraform -chdir=infrastructure/terraform destroy 

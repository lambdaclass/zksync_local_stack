OS := $(shell uname -s)
export ZKSYNC_HOME=$(shell pwd)/zksync-era
export PATH:=$(ZKSYNC_HOME)/bin:$(PATH)

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
		curl -s https://raw.githubusercontent.com/nodesource/distributions/master/scripts/nsolid_setup_deb.sh | sh -s "18"; \
		sudo apt update; \
		sudo apt install -y axel libssl-dev nsolid postgresql tmux git build-essential pkg-config cmake clang lldb lld; \
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
	cargo install sqlx-cli --version 0.5.13;
	@if [ "$(OS)" = "Linux" ]; then \
		sudo service postgresql stop; \
	fi
	rm -rf zksync-era; \
	git clone -b boojum-integration https://github.com/matter-labs/zksync-era; \
	rm -rf block-explorer;
	git clone https://github.com/matter-labs/block-explorer; \
	cd ${ZKSYNC_HOME}; \
	npm i -g npm@9; \
	npm install --global yarn; \
	yarn policies set-version 1.22.19; \
	. $(HOME)/.cargo/env; \
	zk; \
	zk init; \
	git remote add lambdaclass https://github.com/lambdaclass/zksync-era; \
	git fetch lambdaclass; \
	git checkout lambdaclass/improve-prover-setup; \
	prover/setup.sh; \
	prover/witness_generator/src/main.rs; \
	rustup install nightly-2023-07-21; \

run:
	. $(HOME)/.cargo/env; \
	tmux kill-session -t zksync-server; \
	
	cd ${ZKSYNC_HOME}; \
	./prover/setup.sh; \

	tmux new -d -s zksync-server; \
	tmux send-keys -t zksync-server "cd ${ZKSYNC_HOME}" Enter; \
	tmux send-keys -t zksync-server "./bin/zk up" Enter; \
	tmux send-keys -t zksync-server "./bin/zk server --components=api,eth,tree,state_keeper,housekeeper,proof_data_handler" Enter; \
		
	tmux new -d -s zksync-prover; \
	tmux send-keys -t zksync-prover "cd ${ZKSYNC_HOME}" Enter; \
	tmux send-keys -t zksync-prover "./bin/zk f cargo run --release --bin zksync_prover_fri_gateway" Enter; \

	tmux new -d -s zksync-witness-generator; \
	tmux send-keys -t zksync-witness-generator "cd ${ZKSYNC_HOME}" Enter; \
	tmux send-keys -t zksync-witness-generator "API_PROMETHEUS_LISTENER_PORT=3116 ./bin/zk f cargo run --release --bin zksync_witness_generator -- --all_rounds" Enter; \

	tmux new -d -s zksync-prover; \
	tmux send-keys -t zksync-prover "cd ${ZKSYNC_HOME}" Enter; \
	tmux send-keys -t zksync-prover "./bin/zk f cargo run --release --bin zksync_prover_fri" Enter; \

	tmux new -d -s zksync-block-compressor; \
	tmux send-keys -t zksync-block-compressor "cd ${ZKSYNC_HOME}" Enter; \
	tmux send-keys -t zksync-block-compressor "./bin/zk f cargo run --release --bin zksync_prover_fri" Enter; \

	docker-compose up -d; \
	tmux a -t zksync-server; \

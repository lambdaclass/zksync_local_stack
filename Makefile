OS := $(shell uname -s)
VALIDIUM ?= false
ZKSOLC_VERSION ?= v1.3.22
SOLC_VERSION ?= v0.8.24
export ZKSYNC_HOME=$(shell pwd)/zksync-era
export PATH:=$(ZKSYNC_HOME)/bin:$(PATH)

compilers_dir_name := eth-compilers

deps:
	@if [ "$(OS)" = "Darwin" ]; then \
		brew install axel openssl postgresql tmux node@18; \
		brew link node@18 --overwrite; \
		curl -L https://github.com/matter-labs/zksolc-bin/releases/download/$(ZKSOLC_VERSION)/zksolc-macosx-arm64-$(ZKSOLC_VERSION) --output zksolc; \
		chmod a+x zksolc; \
		curl -L https://github.com/ethereum/solidity/releases/download/$(SOLC_VERSION)/solc-macos --output solc; \
		chmod a+x solc; \
		mkdir -p $(HOME)/Library/Application\ Support/$(compilers_dir_name); \
		mv solc $(HOME)/Library/Application\ Support/$(compilers_dir_name); \
		mv zksolc $(HOME)/Library/Application\ Support/$(compilers_dir_name); \
	else \
		curl -s https://raw.githubusercontent.com/nodesource/distributions/master/scripts/nsolid_setup_deb.sh | sudo sh -s "18"; \
		sudo apt update; \
		sudo apt install -y axel libssl-dev nsolid postgresql tmux git build-essential pkg-config cmake clang lldb lld; \
		curl -fsSL https://get.docker.com | sh; \
		curl -SL https://github.com/docker/compose/releases/download/v2.23.0/docker-compose-linux-x86_64 -o /usr/local/bin/docker-compose; \
		curl -L https://github.com/matter-labs/zksolc-bin/releases/download/$(ZKSOLC_VERSION)/zksolc-linux-amd64-musl-$(ZKSOLC_VERSION) --output zksolc; \
		curl -L https://github.com/ethereum/solidity/releases/download/$(SOLC_VERSION)/solc-static-linux --output solc; \
		chmod a+x solc; \
		chmod a+x /usr/local/bin/docker-compose; \
		chmod a+x zksolc; \
		mkdir -p $(HOME)/.config/$(compilers_dir_name); \
		mv solc $(HOME)/.config/$(compilers_dir_name); \
		mv zksolc $(HOME)/.config/$(compilers_dir_name); \
		npm i -g npm@9; \
		npm install --global yarn; \
	fi
	@if [ ! -n "$(shell which cargo)" ]; then \
		curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y; \
	fi
	. $(HOME)/.cargo/env; \
	cargo install sqlx-cli --version 0.5.13;
	@if [ "$(OS)" = "Linux" ]; then \
		sudo service postgresql stop; \
	fi
	git clone https://github.com/matter-labs/zksync-era; \
	git clone https://github.com/matter-labs/block-explorer; \
	cd ${ZKSYNC_HOME}; \
	git remote add lambdaclass https://github.com/lambdaclass/zksync-era; \
	git fetch lambdaclass;
	@if [ "$(VALIDIUM)" = "true" ]; then \
		git checkout lambdaclass/validium_mode_new_fee_model_final; \
	fi
	yarn policies set-version 1.22.19; \
	. $(HOME)/.cargo/env; \
	zk;
	@if [ "$(VALIDIUM)" = "true" ]; then \
		zk init --validium-mode; \
	else \
		zk init; \
	fi
	git checkout lambdaclass/fix_witness_generator_for_boojum prover/setup.sh prover/witness_generator/src/main.rs; \
	rustup install nightly-2024-01-21; \

terra-init:
	terraform -chdir=infrastructure/terraform init

terra-plan:
	terraform -chdir=infrastructure/terraform plan

terra-apply:
	terraform -chdir=infrastructure/terraform apply 

terra-destroy:
	terraform -chdir=infrastructure/terraform destroy 

run:
	. $(HOME)/.cargo/env; \
	tmux kill-session -t zksync-server; \
	tmux new -d -s zksync-server; \
	tmux send-keys -t zksync-server "cd ${ZKSYNC_HOME} && export ZKSYNC_HOME=${ZKSYNC_HOME}" Enter; \
	tmux send-keys -t zksync-server "./bin/zk up" Enter; \
	@if [ "$(VALIDIUM)" = "true" ]; then \
		tmux send-keys -t zksync-server "VALIDIUM_MODE=true ./bin/zk server --components=api,eth,tree,state_keeper,housekeeper,proof_data_handler" Enter
	else \
		tmux send-keys -t zksync-server "./bin/zk server --components=api,eth,tree,state_keeper,housekeeper,proof_data_handler" Enter; \
	fi
	@if [ "$(PROVER)" = "cpu" ]; then \
		cd ${ZKSYNC_HOME}/prover; \
		./setup.sh; \
		tmux kill-session -t zksync-witness-generator; \
		tmux new -d -s zksync-witness-generator; \
		tmux send-keys -t zksync-witness-generator "cd ${ZKSYNC_HOME}/prover && export ZKSYNC_HOME=${ZKSYNC_HOME}" Enter; \
		tmux send-keys -t zksync-witness-generator "API_PROMETHEUS_LISTENER_PORT=3116 ../bin/zk f cargo run --release --bin zksync_witness_generator -- --all_rounds" Enter; \
		tmux kill-session -t zksync-prover; \
		tmux new -d -s zksync-prover; \
		tmux send-keys -t zksync-prover "cd ${ZKSYNC_HOME}/prover && export ZKSYNC_HOME=${ZKSYNC_HOME}" Enter; \
		tmux send-keys -t zksync-prover "../bin/zk f cargo run --release --bin zksync_prover_fri" Enter; \
		tmux kill-session -t zksync-proof-compressor; \
		tmux new -d -s zksync-proof-compressor; \
		tmux send-keys -t zksync-proof-compressor "cd ${ZKSYNC_HOME}/prover && export ZKSYNC_HOME=${ZKSYNC_HOME}" Enter; \
		tmux send-keys -t zksync-proof-compressor "../bin/zk f cargo run --release --bin zksync_proof_fri_compressor" Enter; \
		tmux kill-session -t zksync-prover-gateway; \
		tmux new -d -s zksync-prover-gateway; \
		tmux send-keys -t zksync-prover-gateway "cd ${ZKSYNC_HOME}/prover && export ZKSYNC_HOME=${ZKSYNC_HOME}" Enter; \
		tmux send-keys -t zksync-prover-gateway "../bin/zk f cargo run --release --bin zksync_prover_fri_gateway" Enter; \
	fi
	tmux kill-session -t zksync-explorer; \
	tmux new -d -s zksync-explorer; \
	tmux send-keys -t zksync-explorer "cd ${ZKSYNC_HOME}/../block-explorer && export ZKSYNC_HOME=${ZKSYNC_HOME}" Enter; \
	tmux send-keys -t zksync-explorer "npm install" Enter; \
	tmux send-keys -t zksync-explorer "echo dev | npm run hyperchain:configure" Enter; \
	tmux send-keys -t zksync-explorer "npm run db:create" Enter; \
	tmux send-keys -t zksync-explorer "npm run dev" Enter; \
	tmux a -t zksync-server; \
	docker-compose up -d; \

prover_status:
	ZKSYNC_HOME=$(shell pwd)/zksync-era && zk status prover

down:
	-tmux kill-server || exit 0

clean:
	rm -rf zksync-era
	rm -rf block-explorer
	tmux kill-server || (echo "No tmux sessions"; exit 0)
	./scripts/delete_containers.sh


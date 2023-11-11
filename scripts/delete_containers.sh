if [ "$(docker ps -a | grep -c "grafana")" -gt 0 ]; then
    docker stop grafana && docker rm grafana
fi
if [ "$(docker ps -a | grep -c "postgres-1")" -gt 0 ]; then
	docker stop zksync-era-postgres-1 && docker rm zksync-era-postgres-1
fi
if [ "$(docker ps -a | grep -c "prometheus")" -gt 0 ]; then
	docker stop prometheus && docker rm prometheus
fi
if [ "$(docker ps -a | grep -c "geth-1")" -gt 0 ]; then
	docker stop zksync-era-geth-1 && docker rm zksync-era-geth-1
fi


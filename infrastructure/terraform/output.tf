output "server_ips" {
 value = hcloud_server.server.ipv4_address
}

output "explorer_ips" {
 value = hcloud_server.explorer.ipv4_address
}

output "prometheus_grafana" {
 value = hcloud_server.prometheus_grafana.ipv4_address
}

resource "hcloud_server" "server" {
  name        = "zksync-server"
  image       = var.os_type
  server_type = var.server_type
  location    = var.location
  ssh_keys    = [hcloud_ssh_key.default.id]
  labels = {
    type = "web"
  }
  user_data = file("server.yml")
}

resource "hcloud_server" "explorer" {
  name        = "zksync-explorer"
  image       = var.os_type
  server_type = var.server_type
  location    = var.location
  ssh_keys    = [hcloud_ssh_key.default.id]
  labels = {
    type = "web"
  }
  user_data = file("explorer.yml")
}

resource "hcloud_server" "prometheus_grafana" {
  name        = "zksync-prometheus"
  image       = var.os_type
  server_type = var.server_type
  location    = var.location
  ssh_keys    = [hcloud_ssh_key.default.id]
  labels = {
    type = "web"
  }
  user_data = file("prometheus_grafana.yml")
}

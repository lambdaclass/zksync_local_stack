resource "hcloud_server" "web" {
  count       = var.instances
  name        = "zksync-server-${count.index}"
  image       = var.os_type
  server_type = var.server_type
  location    = var.location
  ssh_keys    = [hcloud_ssh_key.default.id]
  labels = {
    type = "web"
  }
  user_data = file("server.yml")
}

resource "hcloud_server" "web" {
  count       = var.instances
  name        = "zksync-explorer-${count.index}"
  image       = var.os_type
  server_type = var.server_type
  location    = var.location
  ssh_keys    = [hcloud_ssh_key.default.id]
  labels = {
    type = "web"
  }
  user_data = file("explorer.yml")
}

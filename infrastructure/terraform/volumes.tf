resource "hcloud_volume" "server_volume" {
  name     = "zk-server-volume"
  size     = var.disk_size
  location = var.location
  format   = "xfs"
}

resource "hcloud_volume" "explorer_volume" {
  name     = "zk-explorer-volume"
  size     = var.disk_size
  location = var.location
  format   = "xfs"
}

resource "hcloud_volume_attachment" "server_vol_attachment" {
  volume_id = hcloud_volume.server_volume.id
  server_id = hcloud_server.server.id
  automount = true
}

resource "hcloud_volume_attachment" "explorer_vol_attachment" {
  volume_id = hcloud_volume.explorer_volume.id
  server_id = hcloud_server.explorer.id
  automount = true
}

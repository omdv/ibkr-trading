resource "google_compute_network" "default" {
  name                    = var.network
  routing_mode            = "REGIONAL"
  auto_create_subnetworks = false
  mtu                     = 1500

  depends_on = [
    google_project_service.run,
    google_project_service.registry,
  ]
}

resource "google_compute_subnetwork" "default" {
  name                     = var.subnetwork
  ip_cidr_range            = var.subnet_cidr
  private_ip_google_access = true
  region                   = var.region
  network                  = var.network

  depends_on = [
    google_compute_network.default,
  ]
}

# resource "google_compute_firewall" "allow-ssh" {
#   name      = "${var.network}-ssh"
#   network   = var.network
#   direction = "INGRESS"

#   allow {
#     protocol = "tcp"
#     ports    = ["22"]
#   }

#   target_tags = [var.project_id]

#   depends_on = [
#     google_compute_network.default,
#   ]
# }

resource "google_compute_firewall" "allow-api" {
  name    = "${var.network}-api"
  network = var.network

  allow {
    protocol = "tcp"
    ports    = ["4041", "4042"]
  }

  source_tags = [var.app_vm_name]
  target_tags = [var.gateway_vm_name]

  depends_on = [
    google_compute_network.default,
  ]
}

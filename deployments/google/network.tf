resource "google_compute_network" "default" {
  project                 = google_project.project.project_id
  name                    = var.network
  routing_mode            = "REGIONAL"
  auto_create_subnetworks = false
  mtu                     = 1500

  depends_on = [
    google_project_service.gcp_services,
  ]
}

resource "google_compute_subnetwork" "default" {
  project                  = google_project.project.project_id
  name                     = var.subnetwork
  ip_cidr_range            = var.subnet_cidr
  private_ip_google_access = true
  region                   = var.region
  network                  = var.network

  depends_on = [
    google_compute_network.default,
  ]
}

resource "google_compute_firewall" "allow-ssh" {
  project   = google_project.project.project_id
  name      = "${var.network}-ssh"
  network   = var.network
  direction = "INGRESS"

  allow {
    protocol = "tcp"
    ports    = ["22"]
  }

  target_tags = [var.project_name]

  depends_on = [
    google_compute_network.default,
  ]
}

resource "google_compute_firewall" "allow-api" {
  project = google_project.project.project_id
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

module "ib-gateway" {
  source  = "terraform-google-modules/container-vm/google"
  version = "~> 2.0"

  container = {
    image = var.gateway_image
    tty   = true
    env = [
      {
        name  = "TRADING_MODE"
        value = var.TRADING_MODE
      },
      {
        name  = "TWSPASSWORD"
        value = var.TWS_PASSWORD
      },
      {
        name  = "TWSUSERID"
        value = var.TWS_USER_ID
      }
    ]
  }
  restart_policy = "Always"
}

resource "google_compute_address" "ib-gateway-internal-ip" {
  project      = google_project.project.project_id
  name         = "ib-gateway-internal-address"
  subnetwork   = var.subnetwork
  address_type = "INTERNAL"
  address      = var.ib_gateway_internal_ip
  region       = var.region
  purpose      = "GCE_ENDPOINT"
  depends_on = [
    google_compute_subnetwork.default,
  ]
}

resource "google_compute_instance" "ib-gateway" {
  project                   = google_project.project.project_id
  machine_type              = var.gateway_machine_type
  zone                      = var.zone
  name                      = var.gateway_vm_name
  allow_stopping_for_update = true

  boot_disk {
    initialize_params {
      image = module.ib-gateway.source_image
    }
  }

  network_interface {
    network    = google_compute_network.default.id
    subnetwork = google_compute_subnetwork.default.id
    network_ip = var.ib_gateway_internal_ip
    access_config {}
  }

  metadata = {
    gce-container-declaration = module.ib-gateway.metadata_value
    google-logging-enabled    = var.gateway_logging_enabled
    google-monitoring-enabled = var.gateway_monitoring_enabled
  }

  labels = {
    container-vm = module.ib-gateway.vm_container_label
  }

  tags = [var.project_name, var.gateway_vm_name]

  service_account {
    scopes = [
      "https://www.googleapis.com/auth/compute",
      "https://www.googleapis.com/auth/devstorage.read_write",
      "logging-write",
      "monitoring-write"
    ]
  }

  depends_on = [
    google_compute_address.ib-gateway-internal-ip,
  ]
}



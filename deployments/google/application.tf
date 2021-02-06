module "ib-app" {
  source  = "terraform-google-modules/container-vm/google"
  version = "~> 2.0"

  container = {
    image = var.app_image
    tty   = true
    env = [
      {
        name  = "IB_GATEWAY_HOST"
        value = var.ib-gateway-internal-ip
      },
      {
        name  = "IB_GATEWAY_PORT"
        value = var.ib-gateway-port
      }
    ]
  }
  restart_policy = "Always"
}

resource "google_compute_instance" "ib-app" {
  project                   = var.project_id
  machine_type              = var.app_machine_type
  zone                      = var.zone
  name                      = var.app_vm_name
  allow_stopping_for_update = true

  boot_disk {
    initialize_params {
      image = module.ib-app.source_image
    }
  }

  network_interface {
    network    = var.network
    subnetwork = var.subnetwork
    access_config {}
  }

  metadata = {
    gce-container-declaration = module.ib-app.metadata_value
    google-logging-enabled    = var.app_logging_enabled
    google-monitoring-enabled = var.app_monitoring_enabled
  }

  labels = {
    container-vm = module.ib-app.vm_container_label
  }

  tags = [var.project_id, var.app_vm_name]

  service_account {
    scopes = [
      "https://www.googleapis.com/auth/compute",
      "https://www.googleapis.com/auth/devstorage.read_write",
      "https://www.googleapis.com/auth/datastore",
      "logging-write",
      "monitoring-write"
    ]
  }

  depends_on = [
    google_compute_subnetwork.default,
  ]
}

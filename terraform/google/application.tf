module "ib-app" {
  source  = "terraform-google-modules/container-vm/google"
  version = "~> 2.0"

  container = {
    image = var.app_image
    tty   = true
    env = [
      {
        name  = "IB_GATEWAY_HOST"
        value = var.ib_gateway_internal_ip
      },
      {
        name  = "IB_GATEWAY_PORT"
        value = var.ib_gateway_port
      },
      {
        name  = "GCS_BUCKET_NAME"
        value = google_storage_bucket.data.name
      },
      {
        name = "STORAGE_BACKEND"
        value = "gcs"
      }
    ]
  }
  restart_policy = "Always"
}

resource "google_compute_instance" "ib-app" {
  project                   = google_project.project.project_id
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
    network    = google_compute_network.default.id
    subnetwork = google_compute_subnetwork.default.id
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

  tags = [var.project_name, var.app_vm_name]

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

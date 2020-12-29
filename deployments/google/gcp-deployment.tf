// Configure the Google Cloud provider
provider "google" {
  project = "ibkr-trading"
  region  = "us-central1"
  zone    = "us-central1-c"
}

resource "google_compute_instance" "default" {
  name         = "ib-gateway"
  machine_type = "e2-micro"

  boot_disk {
    initialize_params {
      image = "cos-cloud/cos-stable"
    }
  }

  metadata = {
    google-logging-enabled = "true"
    # gce-container-declaration = "spec:\n  containers:\n    - name: ib-gateway\n      image: 'docker.io/omdv/ib-gateway:978'\n      stdin: false\n      tty: true\n  restartPolicy: Always\n"
  }

  # metadata_startup_script = "docker run -d"

  network_interface {
    network = "default"
    access_config {
    }
  }

  service_account {
    scopes = [
      "userinfo-email",
      "compute-ro"
    ]
  }

}

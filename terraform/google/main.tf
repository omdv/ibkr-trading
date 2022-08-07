provider "google" {
  zone    = var.zone
}

data "google_billing_account" "account" {
  display_name = "My Billing Account"
  open         = true
}

# Generate a random string to append to resource names.
resource "random_string" "random" {
  length  = 6
  upper   = false
  special = false
}

resource "google_project" "project" {
  name            = var.project_name
  project_id      = "${var.project_name}-${random_string.random.result}"
  billing_account = data.google_billing_account.account.id
  auto_create_network = false
  labels          = var.labels
}

resource "google_project_service" "gcp_services" {
  count   = length(var.gcp_service_list)
  project = google_project.project.project_id
  service = var.gcp_service_list[count.index]
  disable_dependent_services = true
}

# Creates a GCS bucket to store tfstate.
resource "google_storage_bucket" "tfstate" {
  name     = "${google_project.project.project_id}-tfstate"
  location = var.region
  project  = google_project.project.project_id
}

# Creates a GCS bucket to store data.
resource "google_storage_bucket" "data" {
  name     = "${google_project.project.project_id}-data"
  location = var.region
  project  = google_project.project.project_id
}

# resource "google_app_engine_application" "app" {
#   project     = var.project_id
#   location_id = var.app-engine-location
# }

# resource "google_project_iam_binding" "project" {
#   role = "roles/viewer"

#   members = [
#     "serviceAccount:${google_project.project.number}@cloudbuild.gserviceaccount.com"
#   ]

#   depends_on = [
#     google_project.project
#   ]
# }

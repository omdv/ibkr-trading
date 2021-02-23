provider "google" {
  project = var.project_id
  zone    = var.zone
}

data "google_billing_account" "acct" {
  display_name = "My Billing Account"
  open         = true
}

resource "google_project" "project" {
  name                = var.project_id
  project_id          = var.project_id
  auto_create_network = false
  billing_account     = data.google_billing_account.acct.id
}

resource "google_project_service" "run" {
  service = "run.googleapis.com"
}

resource "google_project_service" "registry" {
  service = "containerregistry.googleapis.com"
}

resource "google_app_engine_application" "app" {
  project     = var.project_id
  location_id = var.app-engine-location
}

resource "google_project_iam_binding" "project" {
  role = "roles/viewer"

  members = [
    "serviceAccount:${google_project.project.number}@cloudbuild.gserviceaccount.com"
  ]
}

variable "TWS_USER_ID" {
  description = "TWS user login"
  type        = string
}

variable "TWS_PASSWORD" {
  description = "TWS user password"
  type        = string
}

variable "VNC_PASSWORD" {
  description = "VNC password"
  type        = string
  default     = ""
}

variable "TRADING_MODE" {
  description = "Trading mode - live or paper"
  type        = string
}

variable "project_name" {
  description = "GCP project name"
  type        = string
}

variable "region" {
  description = "The GCP region to deploy to"
  type        = string
  default     = "us-central1"
}

variable "zone" {
  description = "The GCP zone to deploy to"
  type        = string
  default     = "us-central1-c"
}

variable "app_engine_location" {
  description = "Location for App Engine to serve from"
  type        = string
  default     = "us-central"
}

variable "gateway_vm_name" {
  description = "Instance name for gateway"
  type        = string
  default     = "ib-gateway"
}

variable "app_vm_name" {
  description = "Instance name for app"
  type        = string
  default     = "ib-app"
}

variable "gateway_machine_type" {
  description = "GCE machine type for gateway"
  type        = string
  default     = "e2-small"
}

variable "app_machine_type" {
  description = "GCE machine type for application"
  type        = string
  default     = "e2-small"
}

variable "gateway_image" {
  description = "Link to gateway docker image"
  type        = string
}

variable "app_image" {
  description = "Link to app docker image"
  type        = string
}

variable "network" {
  description = "GCP network name"
  type        = string
  default     = "ib-net"
}

variable "subnetwork" {
  description = "GCP subnetwork name"
  type        = string
  default     = "ib-subnet"
}

variable "subnet_cidr" {
  description = "Subnetwork CIDR"
  type        = string
  default     = "10.0.0.0/25"
}

variable "ib_gateway_internal_ip" {
  description = "Fixed internal IP of ib-gateway"
  type        = string
  default     = "10.0.0.10"
}

variable "ib_gateway_port" {
  description = "Gateway API port: 4041 (live) or 4042 (paper)"
  type        = number
}

variable "gateway_logging_enabled" {
  description = "If true need at least e2-small instance"
  type        = string
  default     = "false"
}

variable "gateway_monitoring_enabled" {
  description = "If true need at least e2-small instance"
  type        = string
  default     = "false"
}

variable "app_logging_enabled" {
  description = "If true need at least e2-small instance"
  type        = string
  default     = "false"
}

variable "app_monitoring_enabled" {
  description = "If true need at least e2-small instance"
  type        = string
  default     = "false"
}

variable "gcp_service_list" {
  type = list
  default = [
    # "run.googleapis.com",
    "containerregistry.googleapis.com", # Container registry
    "cloudapis.googleapis.com",         # Google Cloud APIs
    "compute.googleapis.com",           # Compute Engine API
    "iam.googleapis.com",               # Identity and Access Management (IAM) API
    "iamcredentials.googleapis.com",    # IAM Service Account Credentials API
    "servicemanagement.googleapis.com", # Service Management API
    "serviceusage.googleapis.com",      # Service Usage API
    "sourcerepo.googleapis.com",        # Cloud Source Repositories API
    "storage-api.googleapis.com",       # Google Cloud Storage JSON API
    "storage-component.googleapis.com", # Cloud Storage
  ]
}

variable "labels" {
  type = map
  default = {
    "environment" = "prod"
  }
}
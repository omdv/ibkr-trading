output "project_name" {
  description = "Project name"
  value = var.project_name
}

output "project_id" {
  description = "Project ID"
  value = google_project.project.project_id
}

output "gateway_name" {
  description = "Gateway instance name"
  value       = var.gateway_vm_name
}

output "app_name" {
  description = "App instance name"
  value       = var.app_vm_name
}

output "gateway-internal-ip" {
  description = "Internal IP of gateway"
  value       = google_compute_address.ib-gateway-internal-ip.address
}

output "gateway-external-ip" {
  description = "External IP of gateway"
  value       = google_compute_instance.ib-gateway.network_interface.0.access_config.0.nat_ip
}

output "app-internal-ip" {
  description = "Internal IP of gateway"
  value       = google_compute_instance.ib-app.network_interface.0.network_ip
}

output "app-external-ip" {
  description = "External IP of gateway"
  value       = google_compute_instance.ib-app.network_interface.0.access_config.0.nat_ip
}

output "app-container" {
  description = "The container metadata provided to the module"
  value       = module.ib-app.container
}

output "gateway-container" {
  description = "The container metadata provided to the module"
  value       = module.ib-gateway.container
}

output "app-machine-type" {
  value = var.app_machine_type
}

output "gateway-machine-type" {
  value = var.gateway_machine_type
}

output "gateway-label" {
  description = "The instance label containing container configuration"
  value       = module.ib-gateway.vm_container_label
}

output "app-label" {
  description = "The instance label containing container configuration"
  value       = module.ib-app.vm_container_label
}

output "network" {
  description = "GCP network"
  value       = var.network
}

output "subnetwork" {
  description = "GCP subnetwork"
  value       = var.subnetwork
}

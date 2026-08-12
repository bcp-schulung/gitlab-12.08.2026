output "server_ipv4" {
  description = "Public IPv4 address of the server."
  value       = hcloud_server.vm.ipv4_address
}

output "server_ipv6" {
  description = "Public IPv6 address of the server."
  value       = hcloud_server.vm.ipv6_address
}

output "private_key_path" {
  description = "Local path to the generated SSH private key."
  value       = local_sensitive_file.private_key.filename
}

output "ssh_command" {
  description = "Ready-to-use SSH command for connecting to the server as root."
  value       = "ssh -i ${local_sensitive_file.private_key.filename} root@${hcloud_server.vm.ipv4_address}"
}

variable "server_name" {
  description = "Name of the Hetzner Cloud server."
  type        = string
  default     = "student-vm"
}

variable "server_type" {
  description = "Hetzner Cloud server type."
  type        = string
  default     = "cpx22"
}

variable "location" {
  description = "Hetzner Cloud datacenter location."
  type        = string
  default     = "nbg1"
}

variable "image" {
  description = "Hetzner Cloud image to boot the server with."
  type        = string
  default     = "ubuntu-24.04"
}

variable "ssh_key_name" {
  description = "Name used for the generated SSH key in Hetzner Cloud and for the local key files."
  type        = string
  default     = "student-vm-key"
}

# Generates a single ED25519 keypair for the VM. The public half is
# registered with Hetzner Cloud so it gets installed on the server; both
# halves are also written to ./generated so they can be handed out to
# students. That folder is gitignored - distribute the key files
# out-of-band, do not commit them.

resource "tls_private_key" "student" {
  algorithm = "ED25519"
}

resource "hcloud_ssh_key" "student" {
  name       = var.ssh_key_name
  public_key = tls_private_key.student.public_key_openssh
}

resource "local_sensitive_file" "private_key" {
  content         = tls_private_key.student.private_key_openssh
  filename        = "${path.module}/generated/${var.ssh_key_name}"
  file_permission = "0600"
}

resource "local_file" "public_key" {
  content  = tls_private_key.student.public_key_openssh
  filename = "${path.module}/generated/${var.ssh_key_name}.pub"
}

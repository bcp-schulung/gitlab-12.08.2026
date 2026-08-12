# The hcloud provider reads the API token automatically from the HCLOUD_TOKEN
# environment variable, so no token attribute is set here and the secret never
# becomes a Terraform variable or gets written into state.
#
# Populate terraform/.env with HCLOUD_TOKEN=<your real token> (never commit
# it - only .env.example is tracked in git), then export it into your shell
# before running any terraform command, e.g.:
#
#   set -a && source .env && set +a && terraform plan
#
provider "hcloud" {}

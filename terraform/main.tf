terraform {
  required_version = ">= 1.0"
  required_providers {
    # Uncomment for AWS:
    # aws = {
    #   source  = "hashicorp/aws"
    #   version = "~> 5.0"
    # }
    local = {
      source  = "hashicorp/local"
      version = "~> 2.4"
    }
    null = {
      source  = "hashicorp/null"
      version = "~> 3.2"
    }
  }
}

#Variables
variable "environment" {
  description = "Environment name"
  type        = string
  default     = "production"
}

variable "app_name" {
  description = "Application name"
  type        = string
  default     = "sre-app"
}

variable "vm_count" {
  description = "Number of worker nodes"
  type        = number
  default     = 2
}

# Local: simulate VM provisioning 
# (Replace this section with AWS/GCP/Azure provider for cloud)

resource "local_file" "inventory" {
  content = templatefile("${path.module}/templates/inventory.tpl", {
    app_name    = var.app_name
    environment = var.environment
    vm_count    = var.vm_count
  })
  filename = "${path.module}/../ansible/inventory.ini"
}

resource "local_file" "env_config" {
  content = jsonencode({
    environment = var.environment
    app_name    = var.app_name
    vm_count    = var.vm_count
    db_host     = "postgres"
    redis_host  = "redis"
    created_at  = timestamp()
  })
  filename = "${path.module}/../ansible/vars/terraform_output.json"
}

resource "null_resource" "provision_note" {
  triggers = {
    always_run = timestamp()
  }

  provisioner "local-exec" {
    command = "echo 'Infrastructure provisioned: ${var.vm_count} nodes for ${var.environment}'"
  }
}

# Outputs 
output "environment" {
  value = var.environment
}

output "vm_count" {
  value = var.vm_count
}

output "ansible_inventory_path" {
  value = local_file.inventory.filename
}

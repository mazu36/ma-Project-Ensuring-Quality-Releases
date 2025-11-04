# VM
variable "location" {}
variable "resource_group_name" {}
variable "application_type" {}
variable "resource_type" {}

# IP config
variable "subnet_id" {}
variable "public_ip_address_id" {} 

# Custom image
variable "gallery_name" {}
variable "custom_image_name" {} 
variable "custom_image_resource_name" {}

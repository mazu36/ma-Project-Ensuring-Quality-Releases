provider "azurerm" {
  tenant_id       = "${var.tenant_id}"
  subscription_id = "${var.subscription_id}"
  client_id       = "${var.client_id}"
  client_secret   = "${var.client_secret}"
  features {}
}
terraform {
  backend "azurerm" {
    storage_account_name = "tfstate1727326673"
    container_name       = "tfstate"
    key                  = "test.terraform.tfstate"
    access_key           = "N0TUACzxo1sfBJ+k7/VnPaHIO99aZNquo1cVVMYjjquHJvAjnJlCcSj1IPSM6zhCvFxlfXgebOMH+ASt3uAM6g=="
  }
}
module "resource_group" {
  source               = "../../modules/resource_group"
  resource_group       = "${var.resource_group}"
  location             = "${var.location}"
}
module "network" {
  source               = "../../modules/network"
  address_space        = "${var.address_space}"
  location             = "${var.location}"
  virtual_network_name = "${var.virtual_network_name}"
  application_type     = "${var.application_type}"
  resource_type        = "NET"
  resource_group       = "${module.resource_group.resource_group_name}"
  address_prefix_test  = "${var.address_prefix_test}"
}

module "nsg-test" {
  source           = "../../modules/networksecuritygroup"
  location         = "${var.location}"
  application_type = "${var.application_type}"
  resource_type    = "NSG"
  resource_group   = "${module.resource_group.resource_group_name}"
  subnet_id        = "${module.network.subnet_id_test}"
  address_prefix_test = "${var.address_prefix_test}"
}
module "appservice" {
  source           = "../../modules/appservice"
  location         = "${var.location}"
  application_type = "${var.application_type}"
  resource_type    = "AppService"
  resource_group   = "${module.resource_group.resource_group_name}"
}
module "publicip" {
  source           = "../../modules/publicip"
  location         = "${var.location}"
  application_type = "${var.application_type}"
  resource_type    = "publicip"
  resource_group   = "${module.resource_group.resource_group_name}"
}
module "vm" {
  source                      = "../../modules/vm"
  location                    = "${var.location}"
  resource_group_name         = "${module.resource_group.resource_group_name}"
  application_type            = "${var.application_type}"
  resource_type               = "vm"
  subnet_id                   = "${module.network.subnet_id_test}"
  public_ip_address_id        = "${module.publicip.public_ip_address_id}"
  gallery_name                = "${var.gallery_name}"
  custom_image_name           = "${var.custom_image_name}"
  custom_image_resource_name  = "${var.custom_image_resource_name}"
}
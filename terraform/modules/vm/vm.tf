data "azurerm_shared_image" "test" {
  name                = "testImageVM"
  gallery_name        = "testGallery"
  resource_group_name = "Azuredevops"
  location    = "France Central"
  os_type             = "Linux"

  identifier {
    publisher = "canonical"
    offer     = "0001-com-ubuntu-server-jammy"
    sku       = "22_04-lts-gen2"
  }

  #/subscriptions/80ae9245-22ea-4f16-a42f-d5cebd7aac99/resourcegroups/azuredevops/providers/microsoft.compute/galleries/testgallery/images/testimagevm/versions/0.0.1
}


resource "azurerm_network_interface" "test" {
  name                = "${var.application_type}-${var.resource_type}-nic"
  location            = "${var.location}"
  resource_group_name = "${var.resource_group_name}"

  ip_configuration {
    name                          = "internal"
    subnet_id                     = "${var.subnet_id}"
    private_ip_address_allocation = "Dynamic"
    public_ip_address_id          = "${var.public_ip_address_id}"
  }
}

resource "azurerm_linux_virtual_machine" "test" {
  name                = "${var.application_type}-${var.resource_type}"
  location            = "${var.location}"
  resource_group_name = "${var.resource_group_name}"
  size                = "Standard_DS2_v2"
  admin_username      = "admin_user"
  network_interface_ids = [ "${azurerm_network_interface.test.id}"]
  admin_ssh_key {
    username   = "admin_user"
    #public_key = file("~/.ssh/id_rsa.pub")
    #public_key = file("~/Downloads/agent_id_rsa.pub")
    public_key = file("~/myagent/_work/_temp/id_rsa.pub")
  }
  os_disk {
    caching           = "ReadWrite"
    storage_account_type = "Standard_LRS"
  }
  # source_image_reference {
  #   publisher = "Canonical"
  #   offer     = "UbuntuServer"
  #   sku       = "18.04-LTS"
  #   version   = "latest"
  # }

  source_image_id = data.azurerm_shared_image.test.id
}

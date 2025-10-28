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
    public_key = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDtZe0vtxB8TIsHpsHrriLicXU0ukifSVDV/UsK4LvmKz2QdfrZTj2e4Ons0eWLn28kTIVbHEUlT/cwWoyLGo8DSo7uap8bahDP73ac6XtYAZfpoHiyMklQtv9ThiQuZxDBW3UfhQ4Ev88ilg7Ia77poz0j/YTlbEFGkQeVGpG/D/RrRtvmKft6gUpuOmAl+pLwqdH7Y+NVve3BT2CHlbmeKH2iaHYgcdQ+kh3GX345DnGBtDutRSTUpSSGPboTlIbt+tAvj+RokYx66/0fKePiNStoCKWPDBQLawS44Js1pCSgwrvvOQNuTQS3vBS2hhxTTzdJ6UtTuaBMGJEHiTWg/+y9tQfCn2IE53WpYVtDLfAMQWvnZW2OwfI9k7a3xjvxMa8aeoVzub5ubBvMtDGFL6RmNQvtpnh86lOFfIHz9QBAYSsX12jFLRlombMKcyYuUrRe9tbg5MQpt4JPh8SkVRmlGWcL1GiZcS4o2vtHfR0oCVdOEd+dYIMkKL7tl5c= maria@anous-MACHC-WAX9"
  }
  os_disk {
    caching           = "ReadWrite"
    storage_account_type = "Standard_LRS"
  }
  source_image_reference {
    publisher = "Canonical"
    offer     = "UbuntuServer"
    sku       = "18.04-LTS"
    version   = "latest"
  }
}

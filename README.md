# Project Ensuring Quality Releases (Quality Assurance) 


### Introduction
With this project, we will create a disposable test environment in the Cloud Azure containing several test tools: 
+ __Postman__ for integration tests
+ __Selenium__ for UI test
+ __JMeter__ for performance test.

Cloud Azure environment will be supplied by __Terraform__ scripts.
Virtual Machine image will be created by the __Packer__ tool.
CI/CD pipeline will be set up using __Azure Pipeline__ build server.


### Getting Started
1. Clone the starter repository https://github.com/udacity/cd1807-Project-Ensuring-Quality-Releases
2. **terraform** folder: you find here the starter infrastructure as code scripts that you need to update
3. **automatedtesting/postman** folder: you find here StarterAPIs.json file as an integration test example
4. **automatedtesting/selenium** folder: you find here login.py file as a functional test example
5. **automatedtesting/jmeter** folder: you find here StarterAPIs.json file as a performance test example
6. **azure-pipelines.yml** file: a starter version of the configuration file to realize the build and deployment of the CICD pipeline


### Dependencies
1. Create an [Azure Account](https://portal.azure.com) 
2. Install the [Azure CLI command line interface](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli?view=azure-cli-latest)
3. Create an [Azure DevOPs Account](https://azure.microsoft.com/en-us/pricing/details/devops/azure-devops-services/)
4. Install [VS Code](https://code.visualstudio.com/Download)
5. Install [Python](https://www.python.org/downloads/)
3. Install [Packer](https://www.packer.io/downloads)
4. Install [Terraform](https://www.terraform.io/downloads.html)
5. Install [Postman](https://www.postman.com/downloads/)
6. Install [Selenium](https://sites.google.com/a/chromium.org/chromedriver/getting-started)
7. Install [JMeter](https://jmeter.apache.org/download_jmeter.cgi)


# IMPORTANT Informations
Important: When you will deploy using the CI/CD pipeline, 
the resource_group_name must be an empty Resource Group. 
Ensure to delete all resources in the Resource Group before you trigger the CI/CD pipeline, 
otherwise the pipeline execution will fail.

# Log in 
https://portal.azure.com/  using the Azure credentials provided by the Udacity cloud lab environment 
https://dev.azure.com/     using the same Azure account


# [A] Instructions for Setting environment by Terraform


1. Fork [the Starter repository](https://github.com/udacity/cd1807-Project-Ensuring-Quality-Releases)
2. Clone the forked repository into your local environment.
3. Generate an SSH key pair in your local/AZ Cloud shell. 
4. Put ssh keys into Azure DevOps Library
    [Use secure file feature in the pipeline library UI to save the "id_rsa" file](https://learn.microsoft.com/en-us/azure/devops/pipelines/library/secure-files?view=azure-devops#add-a-secure-file)
    1. Upload a secure file
        Azure DevOps: <project> / "Project Settings" >> Pipelines >> Library >> "Secure Files"
        ==> upload a file
        ==> "OK"
    2. Set permissions for a secure file
        Azure DevOps: <project> / "Project Settings" >> Pipelines >> Library >> "Security"
        select <secure file> 
            => Security / "Pipeline permissions" / "Approvals and checks"
        Security            : to set users and security roles that can access the file
        Pipeline permissions: to select YAML pipelines that can access the file
        Approvals and checks: to set approvers and other checks for using the file
42. 

+ Secret variable
+ Secure File

We recommend that you don't pass in your public key as plain text to the task configuration. 
Instead, set a **secret variable** in your pipeline for the contents of your mykey.pub file. 

To set secrets in the web interface, follow these steps:

Go to the Pipelines page, select the appropriate pipeline, and then select Edit.
Locate the Variables for this pipeline.
Add or update the variable.
Select the option to Keep this value secret to store the variable in an encrypted manner.
Save the pipeline.


Then, call the variable in your pipeline definition as $(myPubKey). 
For the secret part of your key, use the **Secure File library** in Azure Pipelines.


### Secret variable in the UI
To set secrets in the web interface, follow these steps:

Go to the Pipelines page, select the appropriate pipeline, and then select Edit.
Locate the Variables for this pipeline.
Add or update the variable.
Select the option to **Keep this value secret** to store the variable in an encrypted manner.
Save the pipeline.
Secret variables are encrypted at rest with a 2048-bit RSA key. Secrets are available on the agent for tasks and scripts to use. 



3. Terraform scripts updates: terraform.tfvars
    + **terraform/environments/test/terraform.tfvars**
        update informations relative to your Azure account:
        service principal, subscription informations, etc

        subscription_id =  
        client_id = 
        client_secret =  
        tenant_id =  

        location =  
        resource_group_name = "Azuredevops"
        application_type =  
4. Terraform state backend
    Configure the Storage Account and State Backend
    + launch the script to create a storage account for terraform tfstate
        **terraform/environments/test/configure-tfstate-storage-account.sh**
     + update informations for terraform backend  
        (use informations provided by configure-tfstate-storage-account.sh)
        **terraform/environments/test/main.tf**
         terraform {
            backend "azurerm" {
                storage_account_name =  
                container_name       =  
                key                  =  
                access_key           =  
            }
            ...
         }
5. Terraform modules vm updates
    1. terraform/modules/vm/input.tf
    2. terraform/modules/vm/vm.tf
    3. Configuration to permit SSH log into VM 
        (connection SSH needed to be able to connect to VM and execute selenium UI tests)
        Either configure admin_user/admin_password in vm.tf
        either connfigure admin_ssh_key:
        1. Generate SSH key-pair: `ssh-keygen -t rsa`
        2. Update resource linux VM admin_ssh_key configuration
            either you use a reference for public key
                admin_ssh_key {
                    username   = "admin_user"
                    public_key =  "file("~/.ssh/id_rsa.pub")"
                }
            either you use the content for public key: `cat ~/.ssh/id_rsa.pub`
                admin_ssh_key {
                    username   = "admin_user"
                    public_key =  "<content public key>"
                }
6. Ensure the variables are correctly set in the terraform files
    Verify whether the variables in input.tf has values attributed (example: resource_group variable)
7. Launch terraform
    ```
    cd <path>.../terraform/environments/test  # go into test folder
    terraform init
    terraform show
    terraform plan
    terraform apply
    ```
    Verify the resources created using Azure Portal
    Where you finished your tests, destroy the resources:
    ```
    terraform destroy
    ```

# [B] Instructions for Setup Initial Pipeline
Set up a minimalistic DevOps pipeline to ensure the pipeline is set up correctly, before adding multiple stages to it.

## Prerequisites for Azure Pipeline: 
+ GiHub account: Plugin "Azure Pipeline" is installed and permission is set of our relevant repository.  

+ webapplication is up and running # MDE TODO

## Pipeline configuration
1. Azure DevOps: Create PAT Personal Access Token 
    the top-right user icon "**User settings**" / "Personal access tokens"
            Name : "myPAT"
            Scope: Full access

2. Azure DevOps: Create a new project
    name: <the name of the relevant repository>
3. <project_name>/"Project settings": "Service Connection" >> "New Service Connection" 
    name: "myServiceConnection"
    (this is the connection Devops account with Azure account)
    Service or connection type  : Azure Resource Manager
    Authentication method       : Service principal (manual)

    NOTE: 
    Choose the Service principal (automatic) option if you are using your personal Azure account. 
    Otherwise, choose the manual option, if you are using Udacity provided cloud account.

    Use the following values in the "New Azure service connection" wizard that will follow.

    **Field**	                    **Value to choose**
    + Service or connection type	**Azure Resource Manager**
    + Authentication method	        **Service principal (manual)**
    + Scope Level	                **Subscription**
    + Subscription Name	            It will auto populate after the authentication
    + Resource Group Name	        <your_resource_group_name>
    + Service Connection name	    **myServiceConnection**

    AUTHENTICATION
    + Service Principal ID        ... see in "Udacity Lab"/"Service principal Details" ... "Application ID" 
    + Service Principal key       ... see in "Udacity Lab"/"Service principal Details" ... "Secret Key" 

    ==> "VERIFY" authentication
    + Grant access permission to all pipelines?	**YES**
    ==> "Verify and Save" 

4. Azure DevOps:  "Project Settings" >> "Agent pools" >> "new agent pool"

        Pool type           : "Self-hosted"
        Name                :  myAgentPool
        Pipeline permissions:  Grant access permissions to all pipelines
    
5. Create a new VM manually [Azure Portal]
6. Configure the Agent (VM) - Install Docker [Azure Portal, Azure CLI]

    + Azure Portal: Copy the "Public IP address"
        
    + Azure CLI: 
    ```
    # login SSH into agent(VM) : ssh <VM_username>@<VM_public_ip_address>
    ssh devopsagent@<public_ip_address>  #... replace the IP address of your VM

    # install Docker 
    sudo snap install docker

    # Check Python version because this agent will build your code.
    `python3 --version`

    # Configure the devopsagent user to run Docker.
    sudo groupadd docker
    sudo usermod -aG docker $USER

    exit
    ```
    + Restart the Linux VM from Azure portal to apply changes made in previous steps. 
    Restarting the VM will log you out from the SSH log in. 
    You will have to log back in using the same SSH command. 
    Do note the new public IP, if it has been changed after the VM restart.


7. Configure the Agent (VM) - Install Agent Services  [Azure CLI, Azure DevOps]

    1. Get the commands to execute for installing agent services [Azure DevOps]
        Azure DevOps: 
            <project>: "Project settings" >> "Pipelines" >> "Agent pools" >> <agent_pool> >> "New agent" >> "Linux"

        You will see on the screen the commands to execute on the agent VM.
        The commands will be similar to the following:
        ```
            curl -O https://vstsagentpackage.azureedge.net/agent/2.202.1/vsts-agent-linux-x64-2.202.1.tar.gz
            mkdir myagent && cd myagent
            tar zxvf ~/vsts-agent-linux-x64-2.202.1.tar.gz
            ./config.sh
        ```
        Copy these commands to download, create and configure the Linux x64 agent.
        You will execute them on the agent VM after connecting there through SSH.


    2. Execute the commands to download, create and configure the Linux x64 agent. [Azure CLI]
        Azure CLI: execute the code provided with the new agent (see C.5.5.1 above)
        ```
            # replace the placeholders
            curl -O <code_agent_linux_tar_gz>>
            mkdir myagent && cd myagent
            tar zxvf ../<tar_gz>
            ./config.sh
        ```
        + During execution config.sh, you need interactively answer the questions:  
        **Prompt**	    **Response**
        + Accept the license agreement	**Y**
        + Server URL	Provide your Azure DevOps organization URL
                        For example, https://dev.azure.com/<organization-name>
                        Example:   **https://dev.azure.com/odluser193422**
                        (you can retrieve it from Azure Devops URL)
        + Authentication type	(press Enter for PAT) [Press enter]
        + Personal access token	**[Provide the PAT created in DevOps]**  ... <PAT secret>  created before
        + Agent pool (press enter for default)	**myAgentPool**   ... <agent_pool_name>  created before
        + Agent name	(press enter for myLinuxVM) [Press enter]     ... <VM_name>  created before
        + Work folder	(press enter for _work) [Press enter]

    3. Execute the commands svc.sh [Azure CLI]
        Azure CLI:  execute the commands to install and start agent service

        ```
        sudo ./svc.sh install
        sudo ./svc.sh start
        ```

        Azure DevOps: Verify whether the service is now up and running.
            Project Settings >> Pipelines >> Agent Pools >> myAgentPool >> "Agents"  (the green point confirm that the agent is running)

    4. Install additional packages for the Flask Application [Azure Cloud Shell]
        Following the needs of your project, 
        you need to install some specific packages into the agent VM.

        For our Flask application, we install the packages below:

        ```
        sudo apt-get update
        sudo apt update
        sudo apt install software-properties-common
        sudo add-apt-repository ppa:deadsnakes/ppa

        # Check if the VM has Python installed already. Otherwise, use these commands to install Python 3.7

        sudo apt install python3.7
        sudo apt-get install python3.7-venv
        sudo apt-get install python3-pip
        python3.7 --version
        pip --version  

        # Check if the VM has Python installed already. Otherwise, use these commands to install Python 3.9

        sudo apt install python3.9
        sudo apt-get install python3.9-venv
        sudo apt-get install python3-pip
        python3.9 --version
        # Python 3.9.24
        pip --version 


        # Install tools for the Pipeline build steps.

        #sudo apt-get install python3.7-distutils
        sudo apt-get install python3.9-distutils
        sudo apt-get -y install zip

        # In addition, pylint is know to need an additional step, 
        as mentioned in this [stackoverflow thread](https://stackoverflow.com/questions/48015106/pip-installed-pylint-cannot-be-found):

        pip install pylint==2.13.7
        pip show --files pylint
        echo $PATH
        Update the Path for Pylint.

        export PATH=$HOME/.local/bin:$PATH
        echo $PATH
        which pylint

        ```
8. Azure DevOps : Install extension for Terraform
    the top-right menu :   icon  Marketplace >> "Browse marketplace"


# [C] Instructions for Preparing a VM image

In this part, we 
1. Create a Linux VM manually, and 
2. navigate to the DevOps portal to register the VM as **the target environment for your pipeline**.
   For registration, a provided sh script need to be executed on the Linux VM.



In one of the pipeline tasks, you need 
    => to archive web packages (such as, FakeRestAPI) to a VM, and 
in another task, 
    => deploy the archived FakeRestAPI to the Azure Web App. 
    
Archiving a web package in the pipeline requires the configure a target environment of the VM type.



1. Azure Portal: Create manually a new Linux VM 
    VM name: linux-test
2. Azure DevOps: Configure the Test Linux VM 
    <project> >> "Project settings" >> Environment >> "Create environment"
        Name: test-vm
        Description:
        Resource: None/Kubernetes/VM 
        ==>  choose VM

        ==> VM config:
            Provider: Generic provider
            Os      : Linux
            1. Registration script: ... copy the provided script sh
                Message: Personal Access Token of the logged in user is pre-inserted by this script.
                        which expires 3 hours later making the coppied script unusable thereon.
                        Once VM is registered, it will start appearing as an environment resource.
            2. Azure Portal: ssh log into our VM to execute the provided sh script
                `ssh -i <key-name_path> <username>@<public_ip>`
                ```
                chmod 400 ~/.ssh/Downloads.pem
                ssh -i ~/.ssh/Downloads.pem azureuser@<public_ip>
                ```
                (you can find ssh command syntax using the path:
                    Azure Portal >> Virtuam Machine >> <my_vm> >> Connect >> SSH)
            3. Azure Devops: verify whether this registered VM is available as an environment resource
                <project> >> "Project settings" >> Environment >> <our_registered_vm>
3. Azure Portal: Create an image of a VM  
    Virtual machines >> <your-vm> >> Capture (in the top menu)

    We can then use this custom image of the VM in the terraform vm.tf script.

4. terraform: azurerm_linux_virtual_machine :
source_image_id 
    The ID of the Image which this Virtual Machine should be created from. 
    Possible Image ID types include Image IDs, Shared Image IDs, Shared Image Version IDs, Community Gallery Image IDs, Community Gallery Image Version IDs, Shared Gallery Image IDs and Shared Gallery Image Version IDs.

    One of either source_image_id or source_image_reference must be set.
    ==> remove source_image_reference
    ==> add source_image_id

5. azure-pipelines.yml: 
    ## Environment name
    environmentName: 'test-vm'

    stage deploy:
    environment: "$(environmentName)"

# [D] Instructions for Setup Final Pipeline

7.   Create an azure-pipelines.yml config file [Azure Devops, GitHub]
    + Azure Devops <project>/Pipelines/ "Create Pipeline"
            Connect - Github 
            Select  - Select the Github repository containing your application code.
            Configure - Choose existing azure-pipelines-minimal.yml file

            your Azure subscription => "Continue"
            your Azure Web App      => "Validate and configure"
            => Azure Pipelines creates an azure-pipelines.yml file and displays it in the YAML pipeline editor.

    [YAML schema reference](https://learn.microsoft.com/en-us/azure/devops/pipelines/yaml-schema/pipeline) 
    + Run the pipeline




8. Run the pipeline [Azure devOps]
    + In the pipeline YAML editor: 
        Set/verify the specific values for the 3 parameters of your pipeline:
        pool: myAgentPool
        azureServiceConnectionId: myServiceConnection
        webAppName: mywebapp<xxxxxx>
    "Save and Run" button >> "add a commit message" >> "Save and Run"
    + Pipeline "Summary" page: you can follow here the execution of the pipeline
    + "Edit pipeline" option
    You can return to the YAML editor 
        by selecting the vertical dots at the upper right on the Summary page 
        and selecting "Edit pipeline".
    + From the deploy job logs,  get the public URL of the deployed Web App
    and verify whether Web App is working correctly.

    + Azure Portal: <mywebbappxxxxxx> >> "Activity Log" >> Refresh
        We can see the log about the deployment : "Update web site ..."




AAAA
Configurations


JMeter
Install JMeter(opens in a new tab).

Use JMeter to open the /automatedtesting/jmeter/Starter.jmx file.

Replace the APPSERVICEURL with the URL of your AppService once it's deployed.

Later in the project, the /automatedtesting/jmeter/ folder will contain the Endurance, Performance, and Stress test suites.

Postman
Install Postman(opens in a new tab).

To verify the Postman, import the automatedtesting/postman/StarterAPIs.json collection into Postman.

Later in the project, the /automatedtesting/postman/ folder will contain the Data validation and Regression test suites.

ZZZZ


# Instructions

## Install Selenium

1. [Download the latest Chrome driver](https://sites.google.com/chromium.org/driver/).
2. Install Selenium

```
pip install -U selenium
sudo apt-get install -y chromium-browser

chromedriver -v
google-chrome --version
which chromedriver
```

3. Make sure this is added to PATH environment variable
5. Include into **/automatedtesting/selenium/login.py** file the Functional UI tests.
4. Execute the  **/automatedtesting/selenium/login.py** file to open the demo site.

### Note:  Synchronisation issue
By default, the Selenium is waiting the web page loading.
But, Selenium is not waiting when we click the button on the loaded page.

To fix this, several tests done with the different wait values. 
The actual wait setting works:
```
driver.implicitly_wait(20)
time.sleep(40)  # Wait for 40 seconds
```
To confirm whether these waiting values set can fix the observed random behavior
which can be explained by the network performance on my web connection.


### Notes ChromeDriver, WebDriver 
**ChromeDriver** is a standalone server that implements the W3C WebDriver standard. 
ChromeDriver is available for Chrome on Android and Chrome on Desktop (Mac, Linux, Windows and ChromeOS). 
**WebDriver** is an open source tool for automated testing of webapps across many browsers. 
It provides capabilities for navigating to web pages, user input, JavaScript execution, and more. 


## Install JMeter

1. Navigate to the JMeter page and download https://dlcdn.apache.org//jmeter/binaries/apache-jmeter-5.6.3.zip
2. Verification of the integrity:sha512SUM <file>
        `sha512sum apache-jmeter-5.6.3.zip`
        and compare with file sha512 on the apache site
3. Extract the compressed file.
4. Then open apache-jmeter-5.6.3\apache-jmeter-5.6.3\bin\ApacheJMeter.jar
5. Launch JMeter: ApacheJMeter.jar ($HOME/bin/apache-jmeter-5.6.3/bin)
    Options >> "Zoom in"
6. Create Stress test
    in HTTP request, use the public URL of the deployed web service
    use max 2 users for your tests,
    use max 30 users for the final submission
    variables for http requests provided in the input_test_params.csv file 
    Export the results into the .jmeter_tests/stress_test.csv file

    Create a new Thread Group:
        Plan test    >> Add >>  Thread Group
    
    Add elements into the Thread Group:
        Thread Group >> Add >> Config >> HTTP Manager
        => Add: name = xxx  Value = yyy
        Thread Group >> Add >> Sample >> HTTP Request  
        Thread Group >> Add >> Listener >> View Results Tree         
        Thread Group >> Add >> Config >> User Defined Variable
        Thread Group >> Add >> Config >> CSV Data Set Config
        Thread Group >> Add >> Listener >> Simple Data Writer

7. Create Endurance test
    in HTTP request, use the public URL of the deployed web service
    use max 60 sec for the final submission
    variables for http requests provided in the input_test_params.csv file 
    Export the results into the .jmeter_tests/endurance_test.csv file
8. Export test plan into ./PerformanceTestSuite.jmx
9. Local Test of the PerformanceTestSuite.jmx in the shell session

    ```
    cd <jmeter folder>
    ./apache-jmeter-5.6.3/bin/jmeter -n -t PerformanceTestSuite.jmx -j jmeter.log -f
    cat jmeter.log     
    grep -ni summary jmeter.log
    grep -ni starting jmeter.log
    ```

10. The tasks outside CI/CD
    Generate HTML report using the export stress_test.csv file
    Generate HTML report using the export endurance_test.csv file

    Tools (top menu) / Generate HTML report
    ==> 3 parameters
    1. Result file (csv or jtl)
    2. user.properties file
    3. Output folder

    # paths with azureuser
    /home/azureuser/jmeter_tests/endurance_test.csv 
    /home/azureuser/bin/apache-jmeter-5.6.3/bin/user.properties
    /home/azureuser/jmeter_tests/endurance_report1


## Install Postman: API testing tools

**Postman** allows to test the APIs using simple Javascript code. 
You can evaluate your response body, headers, cookies, and more using the [ChaiJS BDD syntax](https://www.chaijs.com/api/bdd/)

**Newman** is a command-line tool for running Postman Collections. 
Use Newman to run and test collections from the command line instead of in the Postman app. 

1. Install Postman
    mkdir Postman && cd Postman
    [Download Postman zip for Linux x64](https://www.postman.com/downloads/).
    tar zxf <zip>
2. [Web version Postman: Create an account Postman](https://www.postman.com/downloads/)
3. launch Postman on your post: ~/Postman/app/postman
4. To verify the Postman, import the **automatedtesting/postman/StarterAPIs.json** collection into Postman.
5. Create Data validation test suite.
8. Create Regression test suite.
9. Test collection RUN 
    Collections <my_collection> >> ... "View more actions" >> Run >> "Run <my_collection>
10. Export the Data validation and Regression test suites in json format.
    Collections <my_collection> >> ... "View more actions" 
            >> More >> Export >> "Export JSON" 
            >> "Choose location <your repo>/automatedtesting/postman/" 
            >> "Save"
11. Install newman 
    `sudo npm install -g newman`
12. Run exported collections using newman CLI
    newman run TestSuite.Data-Validation.json -e Test.environment.json --reporters cli,junit --reporter-junit-export TEST-DataValidation.xml'
    newman run <your_collection>.json -e Test.environment.json --reporters cli,junit --reporter-junit-export TEST-DataValidation.xml'

The collection suites are exported and copied into 
 <your repo>/automatedtesting/postman/
    Integration MDE.postman_collection.json
    Regression MDE.postman_collection.json

TestSuite.Data-Validation.json
TestSuite.Regression.json


# Install Node & Newman

```
## Install Node
sudo apt update

# Installez maintenant l’environnement d’exécution avec le code suivant :
sudo apt install nodejs
 
# Node.js utilise le gestionnaire de paquets npm. Vous l’installez avec ce code :
sudo apt install npm
 
# Pour finir, vérifiez si votre version de Node.js est bien à jour :
node -v && npm --version


# Json with postman collection
/home/maria/Postman/postman_export/Integration MDE.postman_collection_v3.json



### LINKs : Documentation
[Work with API response data and cookies in Postman](https://learning.postman.com/docs/sending-requests/response-data/response-data/)
[Language Chains: ChaiJS BDD syntax](https://www.chaijs.com/api/bdd/)

[Capture a VM in the portal](https://learn.microsoft.com/en-us/azure/virtual-machines/capture-image-portal)
[How to Save JMeter Test Results as CSV and XML Files](https://qaautomation.expert/2025/05/06/how-to-save-jmeter-test-results-as-csv-and-xml-files/)

[Use secure file feature in the pipeline library UI to save the "id_rsa" file](https://learn.microsoft.com/en-us/azure/devops/pipelines/library/secure-files?view=azure-devops#add-a-secure-file)

[PublishTestResults@2 - Publish Test Results v2 task](https://learn.microsoft.com/en-us/azure/devops/pipelines/tasks/test/publish-test-results?view=azure-devops&tabs=trx%2Cyaml#yaml-snippet)

[DownloadSecureFile@1 - Download secure file v1 task](https://learn.microsoft.com/en-us/azure/devops/pipelines/tasks/reference/download-secure-file-v1?view=azure-pipelines&tabs=linux)

[Azure Pipelines task reference](https://learn.microsoft.com/fr-fr/azure/devops/pipelines/tasks/reference/?view=azure-pipelines#what-are-task-input-aliases)
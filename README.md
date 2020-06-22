# YC_Terraform_API

## Linux:
1) apt-get update
2) apt-get install python3
3) apt-get install python3-pip
4) pip3 install flask flask-wtf pyyaml
5) apt-get install git
6) sudo apt-get install unzip
7) git clone https://github.com/olevino/YC_Terraform_templates.git
8) git clone https://github.com/olevino/YC_Terraform_API.git
9) wget https://releases.hashicorp.com/terraform/0.12.18/terraform_0.12.18_linux_amd64.zip
10) unzip terraform_0.12.18_linux_amd64.zip
11) sudo mv terraform /usr/local/bin/
12) mkdir terraform_workdir; cd terraform_workdir
13) cp ~/YC_Terraform_templates/\*/terraform/\*.tf ~/terraform_workdir
14) terraform init

15) vim ~/YC_Terraform_API/constants.py
PATH_TO_TERRAFORM_DIRECTORY = "..." (п. 11)
PATH_TO_TEMPLATES_REPOSITORY = "..." (п. 6)

16) ~/YC_Terraform_API/run.py

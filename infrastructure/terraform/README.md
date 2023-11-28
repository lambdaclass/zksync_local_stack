# General structure 

The enviroment consist of three virtual machines which contain the server, the explorer and a prometheus-grafana server. Each machine has its own private and public IP. when the VMs are created the public IPs are going to be printed in the terminal and we can use them to log into the VMs with 'ssh', the users for all the VMs is 'root'. Each VM has its own volume that uses to store the data and are all connected throught their private IPs which they use to read data from each other (in the case of the explorer and the prometheus-grafana instance).

# Commands 

there are three commands that we can execute:

* 'make terra-plan': it runs 'terraform plan' that checks that everything is ok and shows how the final infraestructure will look, it does not charge any fee since it does not create any virtual machine in hetzner.

* 'make terra-apply': it runs 'terraform apply'. When this command is executed the setup is created in the hetzner cloud. It creates three virtual machines which contain the server, the explorer and a prometheus-grafana instance.

* 'make terra-destroy': it runs 'terraform destroy' it will simply delete all the virtual machines instances and setup that we have in hetzner.

# Usage

In order to use the terraform setup you need to have a hetzner cloud token and set the variable in the 'terraform.tvfars' file. We also need to create a ssh key for hetzner and store in a 'tf_hetzner.pub' file inside the '.ssh/' directory. Once everything is setted run 'make terra-plan' to check the environment and then run 'make terra-apply'.
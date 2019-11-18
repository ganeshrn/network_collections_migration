# network_collections_migration
Supported Ansible Network collections and migration scenarios

Running migration scenario
--------------------------

Step 1:
Install Ansible [collection_migration](https://github.com/ansible-community/collection_migration) tool

Step 2:
Run network collection migration scenario
```console
(.venv) collection_migration$ git clone git@github.com:ganeshrn/network_collections_migration.git ~/network_collections_migration
(.venv) collection_migration$ python3.7 -m migrate -s ~/network_collections_migration/scenarios/
```


Sample test
-----------
1) Install paramiko (runtime pre-requisite):
```console
$ pip install paramiko
```
2) Update inventory file [\~/network_collections_migration/inventory](https://github.com/ganeshrn/network_collections_migration/blob/master/inventory) as per your enviornment: 

4) Setup [Ansible devel env](https://docs.ansible.com/ansible/latest/dev_guide/developing_modules_general.html#common-environment-setup)

3) Run test playbook
```console
$ cd ~/network_collections_migration/
$ network_collections_migration$ ansible-playbook cli_test.yml
$ network_collections_migration$ ansible-playbook command_test.yml
```

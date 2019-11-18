# network_collections_migration
Supported Ansible Network collections and migration scenarios

Running migration scenario
--------------------------

Step 1:
Install Ansible collection_migration tool https://github.com/ansible-community/collection_migration

Step 2:
Run network collection migration scenario
```console
(.venv) collection_migration$ git clone git@github.com:ganeshrn/network_collections_migration.git ~/network_collections_migration
(.venv) collection_migration$ python3.7 -m migrate -s ~/network_collections_migration/scenarios/
```


Sample test
-----------
Runtime pre-requisites:

1) Install paramiko
```console
(.venv) collection_migration$ pip install paramiko
```
2) Update inventory file as per your enviornment https://github.com/ganeshrn/network_collections_migration/blob/master/inventory

3) Run test playbook
```console
(.venv) collection_migration$ source .cache/releases/devel.git/hacking/env-setup
(.venv) collection_migration$ cd ~/network_collections_migration/
(.venv) network_collections_migration$ ansible-playbook cli_test.yml
(.venv) network_collections_migration$ ansible-playbook command_test.yml
```

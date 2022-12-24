## On Data Node
- cd ~
- wget https://dev.mysql.com/get/Downloads/MySQL-Cluster-7.6/mysql-cluster-community-data-node_7.6.6-1ubuntu18.04_amd64.deb

- sudo apt update
- sudo apt install libclass-methodmaker-perl

- sudo dpkg -i mysql-cluster-community-data-node_7.6.6-1ubuntu18.04_amd64.deb

- sudo nano /etc/my.cnf
- Paste my.cnf file

- sudo mkdir -p /usr/local/mysql/data
- sudo ndbd

- sudo pkill -f ndbd

- sudo nano /etc/systemd/system/ndbd.service
- Paste ndbd.service file

- sudo systemctl daemon-reload
- sudo systemctl enable ndbd
- sudo systemctl start ndbd
- sudo systemctl status ndbd
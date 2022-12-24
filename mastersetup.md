## On Master Node

- cd ~
- wget https://dev.mysql.com/get/Downloads/MySQL-Cluster-7.6/mysql-cluster-community-management-server_7.6.6-1ubuntu18.04_amd64.deb
- sudo dpkg -i mysql-cluster-community-management-server_7.6.6-1ubuntu18.04_amd64.deb
- sudo mkdir /var/lib/mysql-cluster

- sudo nano /var/lib/mysql-cluster/config.ini
- Paste config.ini file

- sudo apt-get update
- sudo apt install libncurses5
- sudo apt --fix-broken install
- sudo ndb_mgmd -f /var/lib/mysql-cluster/config.ini
- sudo pkill -f ndb_mgmd

- sudo nano /etc/systemd/system/ndb_mgmd.service
- Paste ndb_mgmd.service file

- sudo systemctl daemon-reload
- sudo systemctl enable ndb_mgmd
- sudo systemctl start ndb_mgmd
- sudo systemctl status ndb_mgmd

- sudo ufw allow from ip-172-31-32-73.ec2.internal
- sudo ufw allow from ip-172-31-36-154.ec2.internal
- sudo ufw allow from ip-172-31-40-232.ec2.internal

## After setting up and configuring Slave nodes

- cd ~
- wget https://dev.mysql.com/get/Downloads/MySQL-Cluster-7.6/mysql-cluster_7.6.6-1ubuntu18.04_amd64.deb-bundle.tar
- mkdir install
- tar -xvf mysql-cluster_7.6.6-1ubuntu18.04_amd64.deb-bundle.tar -C install/
- cd install
- sudo apt update
- sudo apt install libaio1 libmecab2
- Password: root
- sudo dpkg -i mysql-common_7.6.6-1ubuntu18.04_amd64.deb
- sudo dpkg -i mysql-cluster-community-client_7.6.6-1ubuntu18.04_amd64.deb
- sudo dpkg -i mysql-client_7.6.6-1ubuntu18.04_amd64.deb
- sudo dpkg -i mysql-cluster-community-server_7.6.6-1ubuntu18.04_amd64.deb
- sudo dpkg -i mysql-server_7.6.6-1ubuntu18.04_amd64.deb

- sudo nano /etc/mysql/my.cnf
- Paste master-mb.cnf file

- sudo systemctl restart mysql
- sudo systemctl enable mysql

- mysql -u root -p
- SHOW ENGINE NDB STATUS \G
- exit

## Setup Sakila
- wget https://downloads.mysql.com/docs/sakila-db.tar.gz
- tar -xvzf sakila-db.tar.gz
- cp -r sakila-db /tmp/

- mysql -u root -p
- SOURCE /tmp/sakila-db/sakila-schema.sql;
- SOURCE /tmp/sakila-db/sakila-data.sql;
- USE sakila;
- SHOW FULL TABLES;
- SELECT COUNT(\*) FROM film;
- exit

## Benchmark
- sudo apt-get install sysbench

- sudo sysbench /usr/share/sysbench/oltp_read_write.lua --mysql-user=root --mysql-password='root' --mysql_storage_engine=ndbcluster --mysql-db=sakila --threads=6 --db-driver=mysql --tables=18 --table-size=10000 prepare

- sudo sysbench /usr/share/sysbench/oltp_read_write.lua --mysql-user=root --mysql-password='root' --mysql_storage_engine=ndbcluster --mysql-db=sakila --threads=6 --db-driver=mysql --tables=18 --table-size=10000 run

- sudo sysbench /usr/share/sysbench/oltp_read_write.lua --mysql-user=root --mysql-password='root' --mysql_storage_engine=ndbcluster --mysql-db=sakila --threads=6 --db-driver=mysql --tables=18 --table-size=10000 cleanup

- sudo sysbench /usr/share/sysbench/oltp_write_only.lua --mysql-user=root --mysql-password='root' --mysql_storage_engine=ndbcluster --mysql-db=sakila --threads=6 --db-driver=mysql --table-size=100000 prepare

- sudo sysbench /usr/share/sysbench/oltp_write_only.lua --mysql-user=root --mysql-password='root' --mysql_storage_engine=ndbcluster --mysql-db=sakila --threads=6 --db-driver=mysql --table-size=100000 run

- sudo sysbench /usr/share/sysbench/oltp_write_only.lua --mysql-user=root --mysql-password='root' --mysql_storage_engine=ndbcluster --mysql-db=sakila --threads=6 --db-driver=mysql --table-size=100000 cleanup

- sudo sysbench /usr/share/sysbench/oltp_read_only.lua --mysql-user=root --mysql-password='root' --mysql_storage_engine=ndbcluster --mysql-db=sakila --threads=6 --db-driver=mysql --table-size=100000 prepare

- sudo sysbench /usr/share/sysbench/oltp_read_only.lua --mysql-user=root --mysql-password='root' --mysql_storage_engine=ndbcluster --mysql-db=sakila --threads=6 --db-driver=mysql --table-size=100000 run

- sudo sysbench /usr/share/sysbench/oltp_read_only.lua --mysql-user=root --mysql-password='root' --mysql_storage_engine=ndbcluster --mysql-db=sakila --threads=6 --db-driver=mysql --table-size=100000 cleanup

- sudo sysbench /usr/share/sysbench/oltp_point_select.lua --mysql-user=root --mysql-password='root' --mysql_storage_engine=ndbcluster --mysql-db=sakila --threads=6 --db-driver=mysql --table-size=100000 prepare

- sudo sysbench /usr/share/sysbench/oltp_point_select.lua --mysql-user=root --mysql-password='root' --mysql_storage_engine=ndbcluster --mysql-db=sakila --threads=6 --db-driver=mysql --table-size=100000 run

- sudo sysbench /usr/share/sysbench/oltp_point_select.lua --mysql-user=root --mysql-password='root' --mysql_storage_engine=ndbcluster --mysql-db=sakila --threads=6 --db-driver=mysql --table-size=100000 cleanup
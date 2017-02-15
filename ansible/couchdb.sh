IP=$(hostname -I)
sudo apt-get install couchdb -y
# allow remote access.
sudo sed -i "s/bind_address = .*/bind_address = $IP/g" /etc/couchdb/default.ini
#allow cos domain
sudo sed -i "s/;enable_cos = .*/enable_cos = true$IP/g" /etc/couchdb/default.ini
# Restarts couchDB
sudo service couchdb restart

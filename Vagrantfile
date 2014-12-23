# -*- mode: ruby -*-
# vi: set ft=ruby :

VAGRANTFILE_API_VERSION = "2"

$provisioning_script = <<EOF
	# install required packages
	sudo apt-get update
	sudo apt-get -y install python-numpy python-pandas build-essential unzip gzip bzip2 xz-utils p7zip-full lzop plzip

	# build zpaq
	cd /tmp
	wget http://mattmahoney.net/dc/zpaq660.zip
	unzip zpaq660.zip
	make
EOF

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
	config.vm.box = "ubuntu/trusty64"
	config.vm.provider "virtualbox" do |v|
	  v.memory = 4096
	  v.cpus = 8
	end
	# config.vm.network "forwarded_port", guest: 80, host: 8080

	config.vm.provision "shell", inline: $provisioning_script
end

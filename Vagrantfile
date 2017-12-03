# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|
  config.vm.box = "ubuntu/xenial64"
  
  # set up network ip and port forwarding
  config.vm.network "private_network", ip: "192.168.33.10"

  # Windows users need to change the permissions explicitly so that Windows doesn't
  # set the execute bit on all of your files which messes with GitHub users on Mac and Linux
  config.vm.synced_folder "./", "/vagrant", owner: "ubuntu", mount_options: ["dmode=755,fmode=644"]

  config.vm.provider "virtualbox" do |vb|
    # Customize the amount of memory on the VM:
    vb.memory = "1024"
    vb.cpus = 1
  end

  # Copy your .gitconfig file so that your git credentials are correct
  if File.exists?(File.expand_path("~/.gitconfig"))
    config.vm.provision "file", source: "~/.gitconfig", destination: "~/.gitconfig"
  end

  # Copy your ssh keys for github so that your git credentials work
  if File.exists?(File.expand_path("~/.ssh/id_rsa"))
    config.vm.provision "file", source: "~/.ssh/id_rsa", destination: "~/.ssh/id_rsa"
  end

  # Enable provisioning with a shell script. Additional provisioners such as
  # Puppet, Chef, Ansible, Salt, and Docker are also available. Please see the
  # documentation for more information about their specific syntax and use.
  config.vm.provision "shell", inline: <<-SHELL
    apt-get update
    apt-get install -y git python-pip python-dev build-essential sqlite3 libsqlite3-dev
    pip install --upgrade pip
    apt-get -y autoremove
    # Install app dependencies
    cd /vagrant
    pip install -r requirements.txt
    pip install reprozip
    # Make vi look nice
    sudo -H -u ubuntu echo "colorscheme desert" > ~/.vimrc
  SHELL

end

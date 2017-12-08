# Replicated Concurrency Control and Recovery Database Project
###### Implement a distributed database using multi-version concurrency control, deadlock detection, replication, and failure recovery

## Getting Started
This application can be rebuilt and re-run using either [Reprozip](https://pypi.python.org/pypi/reprozip/0.2.1) or [Vagrant](https://www.vagrantup.com)

###### Using Reprozip
Make sure to have reprounzip installed before you begin.
Download the distributed_db.rpz file from the root directory and from a command line use the following:

TODO: Setup howto for reprounzip

###### Using Vagrant
Make sure to have Vagrant installed before you begin. For install instructions visit: [Vagrant Getting Started](https://www.vagrantup.com/intro/getting-started/)
Clone this repository locally and cd into `distributed_db`.
From a command-line execute `vagrant up` once the virtual machine has been created execute `vagrant ssh`.
Once logged into the virtual machine, cd into `/vagrant/src` and execute the following command:

```bash
python main.py <input_file> [-v]
```

> The -v is an optional argument to set the Verbose flag to True, which will output log messages to stdout
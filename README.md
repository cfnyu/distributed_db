# Replicated Concurrency Control and Recovery Database Project
###### Implement a distributed database using multi-version concurrency control, deadlock detection, replication, and failure recovery

## Getting Started
This application can be rebuilt and re-run using either [Reprozip](https://pypi.python.org/pypi/reprozip/0.2.1) or [Vagrant](https://www.vagrantup.com)

###### Using Reprozip
If you'd prefer to use Reprozip our reprozip package is in the root directory called `distributed_db.rpz`

###### Using Vagrant
Make sure to have Vagrant installed before you begin. For install instructions visit: [Vagrant Getting Started](https://www.vagrantup.com/intro/getting-started/)

After Vagrant has been setup, execute the following commands:
```bash
git clone https://github.com/cfnyu/distributed_db.git
cd distributed_db
```
> NOTE: Please copy the input files you intend to run inside the distributed_db folder. You can call it what ever you want

Copy your input files to a directory in the `distributed_db` folder and execute the following commands:

```bash
vagrant up
vagrant ssh
```

Once the virtual machine is up and you have ssh'd into the new box, run the following commands from inside the VM:

```bash
cd /vagrant
python main.py <input_file_path> [-v]
```

> The -v is an optional argument to set the Verbose flag to True, which will output log messages to stdout
> Note: Please have each test case in a separate file


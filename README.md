# ACI Modular L3Out

[![published](https://static.production.devnetcloud.com/codeexchange/assets/images/devnet-published.svg)](https://developer.cisco.com/codeexchange/github/repo/netcloudag/AciL3outModular)

Python Module for configuring ACI L3Outs on a Modular bases.
Currently Supported is Static- and BGP-Routing (inclusive Multicast). 
The Module Provide an abstraction Layer in Form of Python Objects and gives back 
the JSON which could be posted to the APIC.

## Getting Started

Install Module via pip install or git clone. Please see Section Installing below...

```
from L3Out import ModularL3Out
L3Out2Post = ModularL3Out.L3Out("L3Out-Name-xyz", "Tenant-Name-xyz")
etc...
print L3Out2Post.tostring()
```

### Prerequisites

What things you need to install the software and how to install them

```
Python 3.7.X
```

### Installing

```
pip install --upgrade git+https://github.com/netcloudag/AciL3outModular.git
```

Or

```
git clone https://github.com/netcloudag/AciL3outModular.git
cd AciL3outModular
pip install -r requirements.txt
```

## Running the tests

Simple UnitTest is under test Folder

## Contributing

Please read [CONTRIBUTING.md](https://github.com/netcloudag/AciL3outModular/blob/master/CONTRIBUTING.md) for details on our code 
of conduct, and the process for submitting pull requests to this project.

## Versioning

For the versions available, see the [tags on this repository](https://github.com/netcloudag/AciL3outModular/tags). 

## Authors

* ** Andreas Graber ** - *Initial work*

## License

Please - see the [LICENSE.md](https://github.com/netcloudag/AciL3outModular/blob/master/LICENSE.md) file for details. 


## Example with Sandbox https://sandboxapicdc.cisco.com

This example is done with the script examples/script_eBGP.py
APIC Access-Credential must be inserted in examples/settings.conf like:

```
[APIC]
ip = sandboxapicdc.cisco.com
user = admin
password = PwdOfSandboxApic
```

The APIC Tenant must be existing!

The Script can be tested on all Cisco ACI APICs including the Simulator. The Supported APIC Versions are 2, 3 and 4.

In the beginning the Sandbox APIC is configured without the L3Outs:

![Fabric Tenant](/docs/images/clean_fabric.jpg)

Then we run the script:

![Script Output](/docs/images/script_run.jpg)

The Result in the Sandbox APIC is:

![L3Out posted](/docs/images/after_post.jpg)





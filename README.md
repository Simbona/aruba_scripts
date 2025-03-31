# Aruba OS CX scripts

1. There are about 5 programmatic ways of interacting with Aruba CX 6000 switches. Such as:
2. REST APIs: Python libraries like PY-AOS-CX to make API calls.
3. Paramiko: Mostly for SSH-based interaction with switches, enabling CLI commands to be run.
4. Ansible: Well-crafted playbooks are handy for automating tasks.
5. PHP Libraries: Libraries like Aruba-SwitchAPI allow interaction with Aruba switches via their APIs, great for config and management

This repo makes an attempt on two:
1. The python Library pyaoscx >> needs to be imported into the environment
2. Netmiko and Paramiko. These are truly experimental and I am yet to use them on production devices

NB:

These are part of my collection of scripts that I use for day to day Network Ops. I cannot guarantee that they will 100% work out-of-the-box because of the variety of options and setting that need to be enabled/disabled on the switches.

Keep in mind that only Aruba 6000 switches with firmwave > v10.0 are supported

IMPORTANT: The command https-server vrf <VRF-NAME> need be run (enabled) to enable the functionalities for both flavors in the repo (at least, in my opinion)

                                !!!!!!!!!!!!!!HAPPY NETWORKING!!!!!!!!!!!
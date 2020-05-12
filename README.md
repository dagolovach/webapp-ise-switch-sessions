# WebApp to gather Access Sessions info and Set Endpoint Group in ISE

This Flask Web Application allows to do the following:
1. gather information about access-session on the switch.
- login to the switch
- collect all mac addresses from access-sessions
- check access-session for each mac address
- if there is FAIL in the dACL - collect info about this session:
    - interface
    - mac_address
    - ip_address
    - user_name
    - method (mab|dot1x)
    - vendor (for mab)
2. Put endpoint into the specific Endpoint Group in ISE

<!-- TABLE OF CONTENTS -->
## Table of Contents
* [About the Project](#about-the-project)
  * [Built With](#built-with)
* [Getting Started](#getting-started)
* [Usage](#usage)
* [Breakdown](#breakdown)
* [Contact](#contact)

<!-- ABOUT THE PROJECT -->
## About The Project
This project continues my previous script to collect access-session from switch with ISE in monitor mode:

* [Python and ISE monitor mode](https://dmitrygolovach.com/python-and-ise-monitor-mode/)

I decided to create a simple Web Application which allows gathering access-session information from the switch and to put into the specific Endpoint Group in ISE using Cisco ISE API.

### Built With
* Python3
* Flask
* Cisco ISE
* Cisco IOS Switch

<!-- GETTING STARTED -->
## Getting Started
> to run flask application

Windows CMD:
```sh
set FLASK_APP=application.py
flask run
```

Unix Bash (Linux, Mac, etc.):
```sh
export FLASK_APP=hello
flask run
```

> change local.py file with switch and ISE API credentials

<!-- USAGE EXAMPLES -->
## Usage
* collect sessions information from the switch
    * enter switch IP address
    * collect access-session information and show it in the table/json file
    * provide option to update group in the ISE for this MAC address
* work with just some MAC address
    * enter MAC address
    * update the group in ISE for provided MAC address

![image-37-1536x360](https://user-images.githubusercontent.com/39305133/81471719-aa931f80-91b8-11ea-9854-107b8824e1a3.png)

Adding MAC address into ISE Group:
![image-40](https://user-images.githubusercontent.com/39305133/81471736-cdbdcf00-91b8-11ea-9810-1225b0abf82f.png)


<!-- BREAKDOWN -->
## Breakdown
* Breakdown post [here](https://dmitrygolovach.com/webapp-ise-python-flask/)
* How it works [youtube](https://youtu.be/xbWCEKQG22c)

<!-- CONTACT -->
## Contact
* Created by Dmitry Golovach
* Web: [https://dagolovachgolovach.com](https://dmitrygolovach.com) 
* Twitter: [@dagolovach](https://twitter.com/dagolovach)
* LinkedIn: [@dmitrygolovach](https://www.linkedin.com/in/dmitrygolovach/)

- feel free to contact me!

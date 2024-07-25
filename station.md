# Pi Setup Guidelines

1. Configure a static connection
   - since the station will point to the database server, This is for the station pi in the department (Scanning)
   - ipv4 set to manual
   - ```bash
     address: 192.168.1.168 #your ip address
     Netmask: 255.255.255.0
     Gateway: 192.168.1.1
     ```
   -  
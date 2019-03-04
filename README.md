# CSSE333Project
## Architecture 
- mySQL
- Python Flask
- Static HTML  

This was my database system project. We chose to build and design a 3 tier web-based architecture for this project. Flask was used as the server router making and handling the paths to service the pages.

The interesting design choice was matching was made into a cron job. Like real recommendations engine, those take large amounts of computing power to perform. We were only given a VM with 2 GB of ram, so to combat this problem, we made this procedure into a batch query system. Where the matching would happen once a day. 

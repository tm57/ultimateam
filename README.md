
**Quick Setup**


 Install docker for your machine
 
 Inside of the root of this project run 
 
 `docker-compose up --force-recreate -V`
 
 After this point create a `/seeds/users.json` file based off of `/seeds/users.example.json`. 
 
 The codes are important if you're running the service for the first time.
 
 
 Once set, you can start the calls to the service by running
 
 `docker exec -it ultimateam-app python3 app.py --action=auto --strategy=gold300`
 
 Of course you can create aliases for these long commands ;)
  





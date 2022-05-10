# Docker workflow

## Docker running
1. `cd` into directory
2. `git pull` for the latest update
3. `sudo docker build --tag taghere .` to build the image
4. `sudo docker run -d --name NewYearResolutionBot --network="host" --env-file ./env.list taghere` to run the image

For the `docker run` command:  
`-d` runs in detached mode, meaning that the container will run after the terminal session is closed  
`--name` specifies the display name of the container  
`--network="host"` this is very important, it specifies that the  container uses the hosts's network, meaning that `localhost` for accessing the DB refers to the host's 'localhost', not the container's 'localhost'  
`--env-file` specifies the env list which should be named `env.list`. The env.list cannot contain parentheses or whitespace, an example is shown below:  
```
TOKEN=fdvbshafgv67a8ury
MYSQLWHATEVER=fsyguf
MYSQLPORT=678
ANOTHERENV=fsjvab
```
And yes, Vscode will give you errors for this file, just ignore them.  

## Docker DB Access
Setting up the DB and allowing access can be pretty hard, as a beginner I spent quite a few hours try to figure out how to access my DB remotely and then how to access my DB locally from a docker container. In your `env.list` make sure that your `MYSQLHOST=localhost`  
`mysql -u root -p`  
`use your_db_name;`  
`CREATE USER ’dbusername’@‘hostname(localhost or IP)' IDENTIFIED BY ’yourpasswdhere’;`  
`GRANT ALL ON dbusername.* to 'user'@'hostname' IDENTIFIED BY 'yourpasswdhere' WITH GRANT OPTION;`  
`FLUSH PRIVELEGES;`

## Useful Resources
[Remote access to DB](https://webdock.io/en/docs/how-guides/database-guides/how-enable-remote-access-your-mariadbmysql-database)  
[Local host access from docker](https://stackoverflow.com/questions/24319662/from-inside-of-a-docker-container-how-do-i-connect-to-the-localhost-of-the-mach)  
[`docker run` documentation](https://docs.docker.com/engine/reference/commandline/run/)  
[An `env.list` tutorial that saved me](https://www.youtube.com/watch?v=DeeEzir3rjY)
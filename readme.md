Simple Python Flask Dockerized Application

Build the image using the following command

```console
$ docker build -t stack-app:latest .
```
Run the Docker container using the command shown below.

```console
$ docker run -d -p 5000:5000 stack-app
``
The application will be accessible at http:127.0.0.1:5000 or if you are using boot2docker then first find ip address using $ boot2docker ip and the use the ip http://<host_ip>:5000


# Issues
(WIP) Home page shows all stack

Enable fulltext search
  - search for technology name
  - search for login of team member

Google Authentication: Login / Logout

Show team member's login and photo. 

Show google profile (name/photo) after login.

Infinite scroll for list of stack 
 -> avaliar https://material.angularjs.org/latest/demo/virtualRepeat or ngInfiniteScrool

Left slidebar that shows terms enable for filter
  - All contact
  - Top 10 technologies
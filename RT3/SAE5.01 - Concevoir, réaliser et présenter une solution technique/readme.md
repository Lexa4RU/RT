# SAE5.01

## What is this project? 
    This project serves to demonstrate the use of containers in a limited infrastructure, using a central server to which different users connect to launch their containers and work from their browser.

## How it works? 
    It works relatively simply. There is a Flask App (really fragile, but easy to develop and based on my very limited capacities in web application development, it's great) that creates different routes, all of them available through an Nginx server with Gunicorn workers to make the in-between. 

    And so, users connect and can open new containers based on the images that the administrators have already created and implemented in the database, and work directly from their browser.

    The administrators can create/delete users, images, and also containers.

## What about security?
    Security was my first objective, making it as bullet-proof as possible, and so instantly I built a Nginx Server with Gunicorn workers as I said earlier which makes possible the use of certificates for https. 

    Containers can't see the network, and so not others containers, they're working on a port in the localhost from which the Nginx server makes a reverse-proxy to a route called /container/<int:id> so the user can connect to it. 

    The Flask app knows which user created which container and so a user A can't use the container of a user B and vice verca, but any administrator can connect or kill any container.  
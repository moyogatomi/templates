### Websockets(Fastapi) + Frontend(Quasar) + Background tasks(Dramatiq)

![Alt Text](https://github.com/moyogatomi/templates/blob/main/websockets/resources/intro.gif)

##### Description
Demo template for websockets.  
Websocket loop consumes from rabbitmq queue. Consumer listens for topics containing user_id ('default').  

Websockets registers also browser tab_id (its a mock and generated as a random number on connection). This results in having multiple tabs with websockets receiving events from multiple queues and therefore push into each open browser tab same logs.

##### Architecture
Most parts async  

Browser <=== (websocket) ===> API server  
Browser === (http endpoint [create task]) ===> API server  

API server === (task publisher) ===> Rabbitmq queue <==== (consumer) === Dramatiq workers  
Dramatiq workers === (Log publisher) ===> Rabbitmq exchange[topic]   
API server (websocket loop) === (consumes topic from a queue binded to an exchange) ===> Rabbitmq exchange  

##### Run

``` 
docker-compose up -d
```



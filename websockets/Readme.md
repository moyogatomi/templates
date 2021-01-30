### Websockets(Fastapi) + Frontend(Quasar) + Background tasks(Dramatiq)

![Alt Text](https://github.com/moyogatomi/templates/blob/main/websockets/resources/intro.gif)

##### Description
Demo template for websockets.  
Websocket loop consumes from rabbitmq queue. Consumer listens for topics containing user_id ('default').  

Not implemented, but if websockets registers also browser tab_id, it could be possible to have multiple websockets connections in different tabs.  
At this moment multiple websockets connections will share a queue and therefore will not duplicate logs.  

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



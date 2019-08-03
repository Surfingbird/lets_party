# lets_party
![Gifts](https://media0.giphy.com/media/3oz8xBkRsgPTnbK1GM/giphy.gif) 

# Backend часть сервиса для подарков

## Быстрый старт

### Требования:
- python 3.7
- вот эта либа для jwt https://github.com/jpadilla/pyjwt/
- и остальные зависимости само собой


### Для старта сервиса необходимо выполнить:
- python3 -m venv venv
- source venv/bin/activate
- pip install -e.
- docker run -d -p 5672:5672 --name rabbitmq rabbitmq:3-management
- docker run -d -p 27017:27017 --name mongodb mongo:4.0.4
- docker run -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:7.3.0
- python3 polls/crawler_app/main.py
- python3 polls/main_api_app/main.py

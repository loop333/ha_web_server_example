### Home Assistant Custom Web Server Or API Example

install:  
```sh
cd ~/.homeassistant/custom_components
git clone https://github.com/loop333/ha_web_server_example my_api
```
configuration.yaml:  
```yaml
my_api:
```
Check result:  
```
http://<host>:8123/my_api/tvpassport/cnn/70
http://<host>:8123/my_api/news/cnn/cnn_latest.rss
http://<host>:8123/my_api/news/echo
http://<host>:8123/my_api/youtube?p=PLHFlHpPjgk72jb60xIb7Jrx4sG06os6bx&f=18&s=1&n=10
```
Youtube url format:  
```
USER: /my_api/youtube?u=<id>&f=18&s=1&n=10
CHANNEL: /my_api/youtube?c=<id>&f=18&s=1&n=10
PLAYLIST: /my_api/youtube?p=<id>&f=18&s=1&n=10
VIDEO: /my_api/youtube?v=<id>&f=18

where:
f - format id, default 18
s - playlist start position, default 1
n - playlist items count from start position, default 10
```

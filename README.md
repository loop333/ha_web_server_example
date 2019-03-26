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
http://<host>:8123/my_api/youtube/PLHFlHpPjgk72jb60xIb7Jrx4sG06os6bx
```

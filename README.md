# Automation test website [moodle](http://localhost/)
## Prequisites
Already installed Docker + Docker Engine

## 📦 Installation

```
pip3 install selenium
pip3 install webdriver-manager
docker-compose -f docker-compose.yaml up -d
```

## 🚀 Usage

1. Run and wait 3 minutes till the moodle installation finished.

2. Check the installation status with 
```sh
docker logs moodle
```

3. The website is available at `http://localhost`, log in with username `user` and password `bitnami`

4. Run tests
```sh
pytest UploadFileTest.py
```
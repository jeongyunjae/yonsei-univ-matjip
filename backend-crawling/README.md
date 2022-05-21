# 서울권 대학 주변 맛집 지도 🗺 (크롤링 서버)

- 초기 환경 설정

1. 파이썬 설치 확인

```
python -v
```

저는 현재 파이썬 3.9.0 버전을 사용하고 있습니다.

2. 파이썬 가상환경 설치 및 구축

내 PC전체가 아닌, 프로젝트에 필요한 파이썬 라이브러리만을 가질 수 있게 환경을 구성해야하기 때문에 가상환경을 구축합니다.

```
pip3 install virtualenv //설치
virtualenv flask-venv //가상환경 구축
source flask-venv/bin/activate //가상환경 접속
```

3. 필요한 라이브러리 설치

아래 명령어로 현재 디렉토리 아래에 있는 requirements.txt 파일에 있는 라이브러리 리스트를 설치합니다.

```
pip install -r requirements.txt
```

4. 크롤링 서버 실행

```
python app.py
```

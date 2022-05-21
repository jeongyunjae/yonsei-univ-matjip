
import argparse
from flask import Flask

# 실행 환경변수 설정
parser = argparse.ArgumentParser()
parser.add_argument('--env',required=False, default='development')
args = parser.parse_args()

# flask app 생성
app = Flask(__name__)

if __name__ == '__main__':
  app.run(host='0.0.0.0', port='3060', debug=True, use_reloader=True)
  
  


# 설명
임의의 텍스트에서 대한민국학교이름을 찾아주는 프로그램입니다.

## 요구조건
```shell
$ apt-get install g++ openjdk-7-jdk python-dev
```

## 개발환경
|종류|설명|
|----|---|
|OS|Ubuntu 16.04|
|Python|2.7.12|
|Docker|17.06.1|

## 실행
```shell
$ git clone https://github.com/odg0318/shool-name-searcher
$ cd school-name-searcher
$ pip install -r requirements.txt
$ python main.py --csvfile=[path/to/csvfile]
```
 
## 실행 with Docker
```shell
$ git clone https://github.com/odg0318/shool-name-searcher
$ cd school-name-searcher
$ make docker-build
$ docker run --rm -v [path/to/csv]:/application/comments.csv school-parser:latest --csvfile=comments.csv

```
  
## 테스트
```
$ python test_school.py
```

## 실행옵션
```
usage: main.py [-h] --csvfile CSVFILE [--verbose] [--no-skip]

A program to parse schools from comments.

optional arguments:
  -h, --help         show this help message and exit
  --csvfile CSVFILE  CSV file to parse.
  --verbose          Show all logs.
  --no-skip          Debug line by line.
```

## 참고
1. http://konlpy-ko.readthedocs.io/ko/v0.4.3/
2. https://github.com/python-excel/xlrd
3. http://www.schoolinfo.go.kr/ng/pnnggo_a01_l0.do

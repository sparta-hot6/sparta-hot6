# 스파르타 내일배움캠프 A반 6조 hot6 mini project
## 자신의 브랜치 만들기
다른 사람들의 코드와 꼬이지 않도록 자신의 브랜치를 만듭니다.

위에서 파일 목록 위에 있는 branch를 클릭하여 들어간 후 new branch 생성.

이름은 자유롭게.

## 로컬로 가져오기
http 사용시
``` bash
git clone https://github.com/sparta-hot6/sparta-hot6.git
```
ssh
``` bash
git clone git@github.com:sparta-hot6/sparta-hot6.git
```

## 작업하기
``` bash
git checkout <mybranch-name>
```

## 작업 후 github에 올리기

``` bash
# 최신화(master branch의 내용을 받아옴)
git pull origin master
# 자기 브랜치에 올리기
git push origin <mybranch-name>
```

## 자신의 브랜치에서 master로 병합 요청
깃허브의 pull request에서 자신 브랜치 => master 브랜치로 병합요청
한 번에 많이 하기보다는 자주 하면 좋습니다.
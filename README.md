# README.md

# Project ANGRY CAT

## 소개

Introducing "Angry Cat" – the purrfect service that unleashes hilariously vengeful feline fury! With this cat-image synthesizing & text generating  service, witness adorable yet annoying cats attacking randomly in pictures, providing a humorous twist to any moment.

Angry Cat은 갖가지 같잖은 이유로 당신의 얼굴에 냥냥펀치를 날리는 고양이 이미지 합성 및 텍스트 생성 기반 커뮤니티 서비스입니다. 귀여우면서도 짜증나는 고양이가 무작위로 사진에서 나타나며, 어떤 순간에도 유머 감각을 더해줍니다!

This project is Toy Project for DRF and ML mudule application. Please enjoy!

이 프로젝트는 DRF와 머신러닝 모듈의 활용을 위한 토이 프로젝트입니다.

## 기능(23.05.23)

### 유저 - 회원가입 기능

- 시리얼라이저를 사용하여 view를 간결하게 작성했습니다.
- 시리얼라이저에서 password validation을 처리합니다.
- 정규표현식으로 username과 password 규칙을 정의했습니다.
- 위반한 규칙을 특정하여 에러 메세지를 반환합니다.

### 유저 - 토큰 로그인, refresh, verify 기능

- simple JWT 제공 view사용하여 간결하게 구현하였습니다.

### 유저 - 회원탈퇴 기능

- 회원 정보를 삭제하지 않고 계정을 불활성화하여 회원 탈퇴를 구현합니다.
- 다른 사용자가 정보를 조회하지 못하게 하여
- 유저의 올바른 비밀번호 입력을 필요로 합니다.

### 유저 - 회원조회 기능

- 각 회원이 작성한 글, 작성한 글 수, 작성한 댓글 수, 자기소개문의 정보를 조회가능합니다.
- 회원 기능을 하나의 뷰로 묶으며, get, 회원가입 허용을 위한 커스텀 퍼미션을 작성했습니다.

### 유저 - 회원수정 기능

- 현 패스워드 validation이후 입력된 데이터에 대하여 정보를 수정합니다.
- 패스워드 변경의 경우 password2를 입력받습니다.

## 참여자

- 최창수(97ckdtn@gmail.com)
- 정현균(wjdgusrbs5@gmail.com)
- 장한울(haracejang@gmail.com)
- 정찬호(zmxndk1@gmail.com)
- 박종원(jongwonparkk@gmail.com)
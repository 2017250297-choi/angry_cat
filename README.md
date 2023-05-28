# README.md

# Project ANGRY CAT

![소개 이미지]()

## 소개 Introduction

Introducing "Angry Cat" – the purrfect service that unleashes hilariously vengeful feline fury! With this cat-image synthesizing & text generating service, witness adorable yet annoying cats show his/her anger randomly in pictures, providing a humorous twist to any moment.

Angry Cat은 갖가지 같잖은 이유로 당신에게 화가난 고양이 이미지 합성 및 텍스트 생성 기반 커뮤니티 서비스입니다. 귀여우면서도 짜증나는 고양이가 무작위로 사진에서 나타나며, 어떤 순간에도 유머 감각을 더해줍니다!

This project is Toy Project for DRF and ML mudule application. Please enjoy!

이 프로젝트는 DRF와 머신러닝 모듈의 활용을 위한 토이 프로젝트입니다.

## SA of this Project

[링크-SA](https://www.notion.so/SA-88793d5b1de84fa88bdf42ab530a5b83)

## 변경점1(23.05.23)

### 유저 - 회원가입 기능 (Sign Up)

- 시리얼라이저를 사용하여 view를 간결하게 작성했습니다.
- 시리얼라이저에서 password validation을 처리합니다.
- 정규표현식으로 username과 password 규칙을 정의했습니다.
- 위반한 규칙을 특정하여 에러 메세지를 반환합니다.

### 유저 - 토큰 로그인, refresh, verify 기능 (Token Authentication)

- simple JWT 제공 view사용하여 간결하게 구현하였습니다.

### 유저 - 회원탈퇴 기능 (Un-register Account)

- 회원 정보를 삭제하지 않고 계정을 불활성화하여 회원 탈퇴를 구현합니다.
- 탈퇴한 회원은 다른 사용자가 정보를 조회할수 없도록 했습니다.
- 유저의 올바른 비밀번호 입력을 필요로 합니다.

### 유저 - 회원조회 기능 (Get User’s Data, User’s Articles)

- 각 회원이 작성한 글, 작성한 글 수, 작성한 댓글 수, 자기소개문의 정보를 조회가능합니다.
- 회원 기능을 하나의 뷰로 묶으며, get, 회원가입 허용을 위한 커스텀 퍼미션을 작성했습니다.

### 유저 - 회원수정 기능(Edit PW, Bio)

- 현 패스워드 validation이후 입력된 데이터에 대하여 정보를 수정합니다.
- 패스워드 변경의 경우 password2를 입력받습니다.

## 변경점2(23.05.24)

### 유저 - 테스트 코드 (Test Code about Account CRUD)

- 테스트 코드로 어느 때나 유저기능을 점검할수 있습니다.

### 게시글 - CRUD (Article CRUD)

- 게시글을 단일-상세조회 / 목록조회가 가능합니다.
- 목록 조회 시: 최신순으로 정렬, 3일이내 좋아요 순으로 정렬, 북마크 한 글만 보기(로그인 회원 전용), 특정 사용자가 작성한 글만 보기를 선택할 수 있습니다.
- 목록 조회 시: 페이지네이션이 적용됩니다.
- 로그인한 유저는 제목, 설명, 이미지 파일, 재치있는 GPT의 코멘트를 포함한 글을 작성할 수 있습니다.
- 자신이 작성한 글의 설명, 제목을 수정할 수 있고 설명의 변경에 맞춰 GPT의 코멘트도 새롭게 받아와 수정할 수 있습니다.
- 자신이 작성한 글을 삭제할 수 있습니다.

### 게시글 - 댓글 CRUD (Comment CRUD)

- 게시글에 댓글을 입력하고, 수정, 삭제 할수 있습니다.
- 댓글 조회에 페이지네이션을 적용하여 50개씩 한페이지로 리스팅됩니다.

## 변경점3(23.05.25)

### 게시글 - 테스트 코드 ( Test Code about Article CRUD)

- 테스트 코드로 언제나 게시글 기능들을 점검할수 있습니다.

### AI처리 - ChatGPT 멘트생성 (Using GPT to Generate Random Text)

- openai api를 통하여 ChatGPT 3.5 turbo모델을 활용합니다.
- 사진 설명을 입력하면, 설명을 기반으로 고양이가 화난 이유를 생성합니다.

## 변경점4(23.05.26)

### 유저 - 소셜 로그인 (OAuth)

- 구글 Oauth2 API를 이용해 간편하고 안전하게 회원가입 및 로그인을 할 수 있습니다.

## 변경점5(23.05.27-28)

### AI처리 - OpenCV, dlib 이미지생성 (Image Processing)

- OpenCV와 dlib라이브러리, dlib모델을 활용하여 입력된 사진에서 사람 얼굴을 인식하고 그 주변에 화가난 고양이를 붙인 사진을 생성합니다.
- 사람 얼굴 사방으로 가장 넓은 공간을 고르고, 전체 사진에서 사람얼굴의 크기를 참고하여 고양이 크기를 조정합니다.
- 고양이 사진이 적절한 가로세로 비율을 유지합니다.
- 사진 생성기능을 하나로 모듈화하여 처리합니다.

## 변경점6(23.05.28-29)

### 프론트 엔드와의 최종연결 및 AWS를 통한 배포 (Deploy)

- HTML, JS를 이용해 작성한 프론트엔드와 API를 연결하였습니다.
- AWS EC2, route53, S3, CloudFront를 이용한 웹앱 배포를 시도하였습니다.(29일 14시 이후부터는 요금 청구 문제로 서비스 일시정지 예정)(링크: [https://barryjung.com/](https://barryjung.com/))

## 참여자

- 최창수(97ckdtn@gmail.com)
- 정현균(wjdgusrbs5@gmail.com)
- 장한울(haracejang@gmail.com)
- 정찬호(zmxndk1@gmail.com)
- 박종원(jongwonparkk@gmail.com)

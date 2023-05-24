from django.urls import reverse
from rest_framework.test import APITestCase
from user.models import User


"""테스트 요약

총 28개 테스트
1. 회원가입
2. 회원가입-에러:패스워드불일치
3. 회원가입-에러:패스워드규칙위반
4. 회원가입-에러: 유저네임 규칙위반

5. 회원탈퇴
6. 회원탈퇴-에러: 패스워드 틀림
7. 회원탈퇴-에러: 비로그인 접근
8. 회원탈퇴-에러: 토큰 유효하지 않음

9. 회원정보수정-자기소개 수정
10. 회원정보수정-패스워드 변경
11. 회원정보수정-아무것도 수정안함
12. 회원정보수정-에러: 현재 패스워드 틀림
13. 회원정보수정-에러: 변경 패스워드2 입력 안함
14. 회원정보수정-에러: 변경 패스워드 불일치
15. 회원정보수정-에러: 비로그인 접근
16. 회원정보수정-에러: 토큰 유효하지 않음

17. 회원정보조회
18. 회원정보조회-에러: 비로그인 접근
19. 회원정보조회-에러: 토큰 유효하지 않음
20. 회원정보조회(ID)
21. 회원정보조회(ID)-에러: 존재하지 않는 회원조회

22. 토큰 login
23. 토큰 login-에러: 유저네임 틀림
24. 토큰 login-에러: 패스워드 틀림
25. 토큰 refresh
26. 토큰 refresh-에러: 잘못된 refresh토큰
27. 토큰 verify
28. 토큰 verify-에러: 잘못된 access토큰
"""

class UserBaseTestCase(APITestCase):
    """유저기능 테스트 준비
    
    유저기능 테스트를 위한 부모 클래스입니다.
    """

    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = User.objects.create_user(
            username="testuser1",
            email="testuser1@gmail.com",
            password="qhdks111!",
        )
        cls.user_signup_data = {
            "username": "testuser2",
            "password": "qhdks111!",
            "password2": "qhdks111!",
            "email": "testuser2@gmail.com"
        }
        cls.user_edit_data = {"current_password": "qhdks111!"}
        cls.user_login_data = {"username": "testuser1", "password": "qhdks111!"}

    def setUp(self) -> None:
        login_user = self.client.post(reverse("token"), self.user_login_data).data
        self.access = login_user["access"]
        self.refresh = login_user["refresh"]


class UserSignUpTestCase(UserBaseTestCase):
    """회원가입 테스트
        
    회원가입을 테스트합니다.
    """
    def test_signup(self):
        """정상: 회원가입
        
        정상적인 회원가입입니다.
        """
        url = reverse("sign")
        data = self.user_signup_data
        response = self.client.post(
            path=url,
            data=data,
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data, {'message': '회원가입성공'})
        
        test_signuped_user = User.objects.get(username=data["username"])
        self.assertEqual(test_signuped_user.username, data["username"])
        
    def test_signup_password_not_same(self):
        """에러: 패스워드 불일치
        
        패스워드 불일치의 경우입니다.
        """
        url = reverse("sign")
        data = self.user_signup_data
        data["password2"] = "qhdks222!"
        response = self.client.post(
            path=url,
            data=data,
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["password"][0], "두 비밀번호가 일치하지 않습니다.")
        
    def test_signup_password_rule(self):
        """에러: 패스워드 규칙위반
        
        패스워드 규칙을 틀린 경우입니다.
        """
        url = reverse("sign")
        data = self.user_signup_data
        data["password"], data["password2"] = "qhdks", "qhdks"
        response = self.client.post(
            path=url,
            data=data,
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["password"][0], "비밀번호는 8자리~32자리, 한개 이상의 숫자/알파벳/특수문자(@,$,!,%,*,#,?,&)로 이루어져야합니다.")
        
    def test_signup_username_rule(self):
        """에러: 유저네임 규칙위반
        
        유저네임 규칙을 틀린 경우입니다.
        """
        url = reverse("sign")
        data = self.user_signup_data
        data["username"] = "user1"
        response = self.client.post(
            path=url,
            data=data,
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["username"][0], "길이 6자리 ~32자리, 알파벳으로 시작하고 알파벳 대소문자와 숫자, 특수기호 -,_,@ 로 이루어져야합니다.")
    


class UserSignOutTestCase(UserBaseTestCase):
    """회원탈퇴 테스트
    
    회원탈퇴를 테스트합니다.
    """

    def test_signout(self):
        """정상: 회원탈퇴
        
        정상적인 회원탈퇴입니다.
        """
        url = reverse("sign")
        data = self.user_login_data
        response = self.client.put(
            path=url,
            HTTP_AUTHORIZATION=f"Bearer {self.access}",
            data=data,
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {'message': '회원탈퇴성공'})
        
        test_signout_user = User.objects.get(username=data["username"])
        self.assertEqual(test_signout_user.is_active, False)

    def test_signout_wrong_password(self):
        """에러: 패스워드 틀림
        
        패스워드가 틀린 경우입니다.
        """
        url = reverse("sign")
        response = self.client.put(
            path=url,
            HTTP_AUTHORIZATION=f"Bearer {self.access}",
            data={"password": "asdf!!1234"},
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(str(response.data["password"][0]), "password wrong.")

    def test_signout_annon(self):
        """에러: 비로그인 접근
        
        비로그인 접근의 경우입니다.
        """
        url = reverse("sign")
        data = self.user_login_data
        response = self.client.put(
            path=url,
            data=data,
        )
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data["detail"], "자격 인증데이터(authentication credentials)가 제공되지 않았습니다.")

    def test_signout_wrong_token(self):
        """에러: 토큰 유효하지 않음
        
        잘못된 토큰을 보낸 경우입니다.
        """
        url = reverse("sign")
        data = self.user_login_data
        response = self.client.put(
            path=url,
            HTTP_AUTHORIZATION=f"Bearer {self.access[:-3]}123",
            data=data,
        )
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data["detail"], "이 토큰은 모든 타입의 토큰에 대해 유효하지 않습니다")


class UserEditTestCase(UserBaseTestCase):
    """회원정보수정 테스트
    
    회원정보 수정을 테스트합니다.
    """

    def test_useredit_bio(self):
        """정상: 자기소개 수정
        
        정상적인 자기소개 수정의 경우입니다.
        """
        url = reverse("sign")
        data = self.user_edit_data
        data["bio"] = "수정 테스트"
        response = self.client.patch(
            path=url,
            HTTP_AUTHORIZATION=f"Bearer {self.access}",
            data=data
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {'message': '회원수정성공'})
        
        test_edit_user = User.objects.get(username=self.user_login_data["username"])
        self.assertEqual(test_edit_user.bio, data["bio"])
        
    def test_useredit_password(self):
        """정상: 패스워드 변경
        
        정상적인 패스워드 변경의 경우입니다.
        """
        url = reverse("sign")
        data = self.user_edit_data
        data["password"] = "qhdks111!"
        data["password2"] = "qhdks111!"
        response = self.client.patch(
            path=url,
            HTTP_AUTHORIZATION=f"Bearer {self.access}",
            data=data
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {'message': '회원수정성공'})

    def test_useredit_nothing(self):
        """정상: 아무것도 수정안함
        
        아무것도 수정안한 경우입니다.
        """
        url = reverse("sign")
        data = self.user_edit_data
        response = self.client.patch(
            path=url,
            HTTP_AUTHORIZATION=f"Bearer {self.access}",
            data=data
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {'message': '회원수정성공'})

    def test_useredit_password_wrong(self):
        """에러: 현재 패스워드 틀림
        
        현재 패스워드를 틀린 경우입니다.
        """
        url = reverse("sign")
        data = self.user_edit_data
        data["current_password"] = "qhdks222!"
        response = self.client.patch(
            path=url,
            HTTP_AUTHORIZATION=f"Bearer {self.access}",
            data=data
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(str(response.data["current_password"][0]), "current password wrong.")

    def test_useredit_password2_miss(self):
        """에러: 변경 패스워드2 입력 안함
        
        변경할 패스워드2를 입력 안한 경우입니다.
        """
        url = reverse("sign")
        data = self.user_edit_data
        data["password"] = "qhdks222!"
        response = self.client.patch(
            path=url,
            HTTP_AUTHORIZATION=f"Bearer {self.access}",
            data=data
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["password"][0], "두 비밀번호가 일치하지 않습니다.")
              
    def test_user_edit_password_not_same(self):
        """에러: 변경 패스워드 불일치
        
        변경할 패스워드가 불일치한 경우입니다.
        """
        url = reverse("sign")
        data = self.user_edit_data
        data["password"] = "qhdks111!"
        data["password2"] = "qhdks222!"
        response = self.client.patch(
            path=url,
            HTTP_AUTHORIZATION=f"Bearer {self.access}",
            data=data
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["password"][0], "두 비밀번호가 일치하지 않습니다.")

    def test_annon(self):
        """에러: 비로그인 접근
        
        비로그인 접근의 경우입니다.
        """
        url = reverse("sign")
        data = self.user_edit_data
        response = self.client.patch(
            path=url,
            data=data,
        )
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data["detail"], "자격 인증데이터(authentication credentials)가 제공되지 않았습니다.")

    def test_wrong_token(self):
        """에러: 토큰 유효하지 않음
        
        잘못된 토큰을 보낸 경우입니다.
        """
        url = reverse("sign")
        data = self.user_edit_data
        response = self.client.patch(
            path=url,
            data=data,
            HTTP_AUTHORIZATION=f"Bearer {self.access[:-3]}123",
        )
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data["detail"], "이 토큰은 모든 타입의 토큰에 대해 유효하지 않습니다")


class UserGetTestCase(UserBaseTestCase):
    """회원정보조회 테스트
    
    회원 본인정보 조회를 테스트합니다.
    """
    
    def test_userget(self):
        """정상: 본인정보조회
        
        정상적인 본인정보조회입니다.
        """
        url = reverse("sign")
        response = self.client.get(
            path=url,
            HTTP_AUTHORIZATION=f"Bearer {self.access}"
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data)

    def test_userget_annon(self):
        """에러: 비로그인 접근
        
        비로그인 접근의 경우입니다.
        """
        url = reverse("sign")
        response = self.client.get(path=url)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data["detail"], "찾을 수 없습니다.")

    def test_userget_wrong_token(self):
        """에러: 토큰 유효하지 않음
        
        잘못된 토큰을 보낸 경우 입니다.
        """
        url = reverse("sign")
        response = self.client.get(
            path=url,
            HTTP_AUTHORIZATION=f"Bearer {self.access[:-3]}123",
        )
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data["detail"], "이 토큰은 모든 타입의 토큰에 대해 유효하지 않습니다")
        

class UserGetIdTestCase(UserBaseTestCase):
    """회원정보조회(ID) 테스트
    
    ID를 이용한 회원 정보 조회를 테스트합니다.
    """
    
    def test_userget_id(self):
        """정상: 정보조회
        
        ID를 이용한 본인정보조회입니다.
        """
        url = reverse("sign_id", kwargs={'user_id':self.user.id})
        response = self.client.get(
            path=url,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data)
    
    def test_userget_id_unexist_user(self):
        """에러: 존재하지 않는 회원조회
        
        존재하지 않는 회원 조회입니다.
        """
        url = reverse("sign_id", kwargs={'user_id':0})
        response = self.client.get(
            path=url,
        )
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data["detail"], "찾을 수 없습니다.")
        

class UserTokenTestCase(UserBaseTestCase):
    """토큰 로그인 및 갱신 테스트
        
    토큰 로그인 및 갱신을 테스트합니다.
    """
    def test_token_login(self):
        """정상: 토큰 login
        
        정상적인 토큰 login입니다.
        """
        url = reverse("token")
        data = self.user_login_data
        response = self.client.post(
            path=url,
            data=data,
        )
        self.assertEqual(response.status_code, 200)
    
    def test_token_login_wrong_username(self):
        """에러: 유저네임 틀림
        
        유저네임을 틀린 경우입니다.
        """
        url = reverse("token")
        data = self.user_login_data
        data["username"] = "testuser0"
        response = self.client.post(
            path=url,
            data=data,
        )
        self.assertEqual(response.status_code, 401)
    
    def test_token_login_wrong_password(self):
        """에러: 패스워드 틀림
        
        패스워트를 틀린 경우입니다.
        """
        url = reverse("token")
        data = self.user_login_data
        data["password"] = "qhdks222!"
        response = self.client.post(
            path=url,
            data=data,
        )
        self.assertEqual(response.status_code, 401)
        
    def test_token_refresh(self):
        """정상: 토큰 refresh
        
        정상적인 토큰 refresh입니다.
        """
        url = reverse("refresh")
        data = {}
        data["refresh"] = self.refresh
        response = self.client.post(
            path=url,
            data=data,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data["access"])
        
    def test_token_refresh_wrong_token(self):
        """에러: 잘못된 refresh토큰
        
        잘못된 refresh토큰을 보낸 경우입니다.
        """
        url = reverse("refresh")
        data = {}
        data["refresh"] = self.refresh[:-3]+"123"
        response = self.client.post(
            path=url,
            data=data,
        )
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data["detail"],"유효하지 않거나 만료된 토큰")

    def test_token_verify(self):
        """정상: 토큰 verify
        
        정상적인 토큰 verify입니다.
        """
        url = reverse("verify")
        data = {}
        data["token"] = self.access
        response = self.client.post(
            path=url,
            data=data,
        )
        self.assertEqual(response.status_code, 200)

    def test_token_verify_wrong_token(self):
        """에러: 잘못된 access토큰
        
        잘못된 access토큰을 보낸 경우입니다.
        """
        url = reverse("verify")
        data = {}
        data["token"] = self.access[:-3]+"123"
        response = self.client.post(
            path=url,
            data=data,
        )
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data["detail"],"유효하지 않거나 만료된 토큰")
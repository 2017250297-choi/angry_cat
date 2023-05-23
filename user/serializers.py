from rest_framework import serializers
from user.models import User
import re

PASSWORD_REGEX = "^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,32}$"
USERNAME_REGEX = "^[A-Za-z\d]+[A-Za-z\d_\-@]{5,31}$"


def password_validation(password, password2):
    """패스워드 검증 함수

    회원가입 시, 비밀번호와 비밀번호 확인 입력을 검증하기 위한 함수입니다.
    둘의 일치를 먼저 확인하고 입력값 자체가 유효한지 regex를 이용해 확인합니다.
    
    Args:
        password (str): 비밀번호 1입니다.
        password2 (str): 비밀번호 2입니다.
        
    Returns:
        없음

    Raises:
        validationError: 두 비밀번호가 일치하지 않습니다.
        validationError: 비밀번호가 형식에 맞지 않습니다.
    """
    if password != password2:
        raise serializers.ValidationError({"password": "두 비밀번호가 일치하지 않습니다."})

    if password != None and not re.match(PASSWORD_REGEX, password):
        raise serializers.ValidationError(
            {
                "password": "비밀번호는 8자리~32자리, 한개 이상의 숫자/알파벳/특수문자(@,$,!,%,*,#,?,&)로 이루어져야합니다."
            }
        )


class UserSerializer(serializers.ModelSerializer):
    """유저 시리얼라이저

    회원가입에 사용되는 serializer입니다.
    """

    # 입력할 때만 쓰이는 password2 시리얼라이저필드 새로 정의
    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True)

    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs = {
            # write_only : 해당 필드를 쓰기 전용으로 만들어 준다.
            # 쓰기 전용으로 설정 된 필드는 직렬화 된 데이터에서 보여지지 않는다.
            "password": {"write_only": True},  # default : False
        }

    def create(self, validated_data):
        """생성 메소드

        부모 클래스의 create를 오버라이딩합니다.
        검증이후 실행됩니다.
        """
        # 저장할 때는 모델에 password2 필드가 없으므로 제거
        del validated_data["password2"]
        user = super().create(validated_data)
        user.set_password(validated_data["password"])  # 비밀번호 저장(해쉬)
        user.save()
        return user

    def validate(self, attrs):
        """검증 메소드

        부모 클래스의 validate 오버라이딩합니다.
        passwor와 password2가 일치하는지 확인합니다.
        이외 나머지 검증은 부모 클래스의 validate에 맡깁니다.
        """
        password_validation(attrs.get("password"), attrs.get("password2"))
        if not re.match(USERNAME_REGEX, attrs.get("username")):
            raise serializers.ValidationError(
                {
                    "username": "길이 6자리 ~32자리, 알파벳으로 시작하고 알파벳 대소문자와 숫자, 특수기호 -,_,@ 로 이루어져야합니다."
                }
            )
        return super().validate(attrs)


class UserSignOutSerializer(serializers.ModelSerializer):
    """유저 탈퇴 시리얼라이저
    
    회원 탈퇴에 사용되는 serializer입니다.
    """

    class Meta:
        model = User
        fields = ("password",)
        extra_kwargs = {
            # write_only : 해당 필드를 쓰기 전용으로 만들어 준다.
            "password": {"write_only": True},
        }

    def validate(self, attrs):
        if not self.instance.check_password(attrs.get("password")):
            raise serializers.ValidationError({"password": "password wrong."})
        return super().validate(attrs)
    

class UserEditSerializer(serializers.ModelSerializer):
    """유저 수정 시리얼라이저
    
    회원정보 수정에 사용되는 serializer입니다.
    비밀번호 변경을 원할 수 있기 때문에 passoword2 필드가 추가됩니다.
    보안을 위해 현재 비밀번호(current_password)를 입력해 검증 시 확인합니다.
    """

    current_password = serializers.CharField(
        style={"input_type": "password"}, write_only=True
    )
    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True)

    class Meta:
        model = User
        exclude = (
            "email",
            "username",
        )

    def update(self, instance, validated_data):
        """수정 메소드
        
        오버라이딩 하였습니다.
        불필요한 데이터를 제거해 오류를 제거한 뒤 비밀번호 부터 지정 하고 저장을 계속합니다.
        """
        validated_data.pop("password2", None)
        validated_data.pop("current_password", None)
        if validated_data.get("password"):
            instance.set_password(validated_data["password"])
            validated_data.pop("password", None)
        user = super().update(instance, validated_data)
        return user

    def validate(self, attrs):
        """검증 메소드
        
        입력된 현재 비밀번호의 유효성부터 검사합니다.
        """
        if not self.instance.check_password(attrs.get("current_password")):
            raise serializers.ValidationError(
                {"current_password": "current password wrong."}
            )
        password_validation(attrs.get("password"), attrs.get("password2"))
        return super().validate(attrs)
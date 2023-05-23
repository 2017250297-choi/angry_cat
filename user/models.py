from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


class UserManager(BaseUserManager):
    """유저 모델 매니저

    유저와 어드민유저 생성을 커스텀 할수있는 객체입니다.
    """

    def create_user(self, username=None, email=None, password=None, **kwargs):
        if not username:
            raise ValueError("Users must have username")
        if not email:
            raise ValueError("Users must have an email address")
        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **kwargs):
        user = self.create_user(username, email, password=password, **kwargs)
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    """유저 모델

    기본 유저 모델을 커스텀한 유저 모델입니다.

    Attributes:
        username : 아이디, 유니크
        email : 이메일, 필수, 유니크
        password : 패스워드
        is_active (bool): 활성 여부
        is_admin (bool): 관리자 여부
        bio : 소개
        created_at : 가입시간
        updated_at : 수정시간
    """

    username = models.CharField(
        max_length=32,
        unique=True,
    )
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    bio = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = [
        "email",
    ]

    def __str__(self):
        return f"{self.username}"

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

from rest_framework import serializers
from .models import OAUser, UserStatus, OADepartment

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, error_messages={'required': 'Email is required'})
    password = serializers.CharField(max_length=20)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = OAUser.objects.filter(email=email).first()
            if not user:
                raise serializers.ValidationError('请输入正确的邮箱和密码')
            if not user.check_password(password):
                raise serializers.ValidationError('请输入正确的邮箱和密码')

            if user.status == UserStatus.UNACTIVATED:
                raise serializers.ValidationError('该用户未激活')
            elif user.status == UserStatus.LOCKED:
                raise serializers.ValidationError('该用户已锁定')
            attrs['user'] = user
        else:
            raise serializers.ValidationError('请传入邮箱和密码')
        return attrs

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = OADepartment
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer()
    class Meta:
        model = OAUser
        exclude = ('password', 'groups', 'user_permissions')


from employee_management.models import UserInfo, PrettyNum
from django import forms
from django.core.exceptions import ValidationError
from employee_management.utils.modelform import BootStrapModelForm


class UserModelFrom(BootStrapModelForm):
    name = forms.CharField(min_length=2, label="用户名")

    class Meta:
        model = UserInfo
        fields = ["name", "password", "age", "account", "create_time", "gender", "depart"]


class PrettyModelForm(BootStrapModelForm):
    # 数据校验
    """mobile = forms.CharField(
        label='手机号',
        validators=[RegexValidator(r'^1[3-9]\d{9}$', '手机号格式错误')]
    )"""

    # 钩子方法
    def clean_mobile(self):
        txt_mobile = self.cleaned_data['mobile']

        if len(txt_mobile) != 11:
            # 验证不通过
            raise ValidationError('格式错误')

        exist_data = PrettyNum.objects.filter(mobile=txt_mobile).exists()
        if exist_data:
            raise ValidationError('手机号已存在')

        # 验证通过
        return txt_mobile

    class Meta:
        model = PrettyNum
        # fields = '__all__'  # 表示取表中所有内容
        fields = ['mobile', 'price', 'level', 'status']


class PrettyEditModelForm(BootStrapModelForm):
    # 数据校验
    """mobile = forms.CharField(
        label='手机号',
        validators=[RegexValidator(r'^1[3-9]\d{9}$', '手机号格式错误')]
    )"""
    mobile = forms.CharField(disabled=True, label='手机号')

    # 钩子方法
    def clean_mobile(self):
        txt_mobile = self.cleaned_data['mobile']

        if len(txt_mobile) != 11:
            # 验证不通过
            raise ValidationError('格式错误')
        # 验证通过
        return txt_mobile

    class Meta:
        model = PrettyNum
        # fields = '__all__'  # 表示取表中所有内容
        fields = ['mobile', 'price', 'level', 'status']

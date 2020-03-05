from django import forms
from django.core.exceptions import ValidationError
import re
from score.models import UserProfile, ScoreRank
from django.db import models

class Base(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})


class RegForm(Base):
    password = forms.CharField(
        label='密码',
        widget=forms.widgets.PasswordInput(),
        min_length=6,
        max_length=12,
        error_messages={
            'min_length': '密码位数不能低于6位',
            'required': '密码不能为空',
            'max_length': '密码最长不能超过12位',
        },
    )

    re_password = forms.CharField(
        label='确认密码',
        widget=forms.widgets.PasswordInput(),
        min_length=6,
        max_length=12,
        error_messages={
            'required': '确认密码不能为空',
            'max_length': '',
            'min_length': '',
        }
    )

    class Meta:
        model = UserProfile
        fields = ['username', 'name', 'password', 're_password']
        labels = {
            'username': '账号',
        }
        error_messages = {
            'username': {
                'required': '用户名不能为空',
                'invalid': '请填写有效的邮箱地址',
            },
            'name': {
                'required': '名字不能为空',
            },

        }

    def clean(self):

        pwd = self.cleaned_data.get('password')
        re_pwd = self.cleaned_data.get('re_password')
        if pwd == re_pwd:
            return self.cleaned_data
        self.add_error('re_password', '两次密码不一致')
        raise ValidationError('两次密码不一致')


class ScoreRankForm(Base):
    class Meta:
        model = ScoreRank
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['customer'].widget.choices = [(self.instance.customer_id, self.instance.customer)]

    def clean(self):
        score = self.cleaned_data.get('score')
        if 1000000 >= score >= 1:
            return self.cleaned_data
        self.add_error('score', '分数超出范围')
        raise ValidationError('分数超出范围')


class Query(models.Model):
    query = models.CharField(max_length=32)


class QueryForm(forms.ModelForm):
    query = forms.CharField(max_length=32)

    class Meta:
        model = Query
        fields = ['query']

    def clean_query(self):

        query = self.cleaned_data.get('query')







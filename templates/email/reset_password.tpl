{% extends "mail_templated/base.tpl" %}

{% block subject %}
Reset password Account
{% endblock %}

{% block body %}
This is Reset Paaword Part
{% endblock %}

{% block html %}
This is Reset Password Link: 

<a href="http://127.0.0.1:8000/accounts/api/v1/reset-password-confirm/{{token}}/">تغییر رمزعبور</a>

{% endblock %}
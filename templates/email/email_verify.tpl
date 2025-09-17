{% extends "mail_templated/base.tpl" %}

{% block subject %}
Verify Account
{% endblock %}

{% block body %}
This is Verify Part
{% endblock %}

{% block html %}
This is verification Link: 

<a href="http://127.0.0.1:8000/accounts/api/v1/activation/confirm/{{token}}/">تایید حساب</a>

{% endblock %}
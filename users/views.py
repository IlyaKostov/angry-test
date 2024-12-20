import json
import os

from django.contrib.auth import login
from django.contrib.sessions.backends.db import SessionStore
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, View

from .models import User, TelegramToken


class HomePageView(TemplateView):
    """Домашняя страница"""
    template_name = "users/index.html"


class LoginWithTelegramView(View):
    """Формирование ссылки на телеграм"""
    def get(self, request, *args, **kwargs):
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        token = TelegramToken.objects.create(session_key=session_key)
        telegram_url = f"https://t.me/{os.getenv('TG_BOT_NAME')}?start={token.token}"
        return JsonResponse({'url': telegram_url})


class AuthenticateTelegramView(View):
    """Аутентификация пользователя"""
    http_method_names = ['post']

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def _get_or_create_user(self, data):
        """Получает или создает пользователя и обновляет данные"""
        user, created = User.objects.get_or_create(
            is_active=True,
            defaults=data,
        )
        if not created:
            for key, value in data.items():
                setattr(user, key, value)
            user.save()
        return user

    def _link_session_to_user(self, session_key, user):
        """Привязывает пользователя к сессии"""
        session = SessionStore(session_key=session_key)
        session['_auth_user_id'] = str(user.pk)
        session['_auth_user_backend'] = "django.contrib.auth.backends.ModelBackend"
        session['_auth_user_hash'] = user.get_session_auth_hash()
        session.save()
        return session

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            token_value = data.pop('token')
            token = TelegramToken.objects.get(token=token_value)
        except (json.JSONDecodeError, KeyError, TelegramToken.DoesNotExist):
            return JsonResponse({"error": "Invalid token or data"}, status=400)

        user = self._get_or_create_user(data)
        request.session = self._link_session_to_user(token.session_key, user)

        login(request, user)
        token.delete()
        return JsonResponse({'status': 'ok'})


class CheckAuthView(View):
    """Проверка авторизации"""
    def get(self, request, *args, **kwargs):
        return JsonResponse({"authenticated": request.user.is_authenticated})

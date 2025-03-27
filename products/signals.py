import asyncio
import os
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import ProductReview
from dotenv import load_dotenv
from utils.mistral_utils import MistralAI


# Загружаем переменные окружения из .env
load_dotenv()
# Токен вашего бота
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
# ID чата, куда отправлять уведомления
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
# API ключ для Mistral
MISTRAL_API_KEY = os.getenv('MISTRAL_API_KEY')
# Модель Mistral для использования
MISTRAL_MODEL = os.getenv('MISTRAL_MODEL')

# TODO: Необходимо реализовать RQ для отложенной отправки уведомлений
@receiver(post_save, sender=ProductReview)
def notify_admin_about_new_review(sender, instance, created, **kwargs):
    if created:
        message = f'Получен новый отзыв от {instance.author} о товаре {instance.product.model.name}.\nТекст: {instance.text}\nОценка: {instance.rating}'
        print(f"Сообщение из сигнала {message}")
        mistral_ai = MistralAI(MISTRAL_API_KEY, MISTRAL_MODEL)
        is_approved = asyncio.run(mistral_ai.check_for_profanity(instance.text))
        instance.is_approved = is_approved
        instance.save()


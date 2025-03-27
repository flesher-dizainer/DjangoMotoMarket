import asyncio
import os
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_q.tasks import async_task
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

        # Добавляем задачу в очередь Django Q
        async_task(check_review_for_profanity, instance.id)


# Функция для проверки отзыва на нецензурную лексику, рекламу и спам
def check_review_for_profanity(review_id):
    try:
        review = ProductReview.objects.get(pk=review_id)
        mistral_ai = MistralAI(MISTRAL_API_KEY, MISTRAL_MODEL)
        is_approved = asyncio.run(mistral_ai.check_for_profanity(review.text))
        review.is_approved = is_approved
        review.save()
    except ProductReview.DoesNotExist:
        print(f"Отзыв с ID {review_id} не найден.")
    except Exception as e:
        print(f"Ошибка при проверке отзыва {review_id}: {e}")

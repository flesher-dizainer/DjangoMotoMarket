from mistralai import Mistral
import json

class MistralAI:
    """
    Класс для взаимодействия с API Mistral.
    """

    def __init__(self, mistral_api_key: str, model: str):
        self.client = Mistral(api_key=mistral_api_key)
        self.model = model

    async def chat(self, message: str) -> str:
        """
        Выполняет чат с заданным сообщением.
        :param message:  Сообщение для чата.
        :return: Ответ от модели.
        """
        messages = [
            {"role": "user", "content": message},
            {"role": "system", "content": f"Верни ответ в Json формате.\n"
                                          f"В ответе должно быть два ключа 'result' и 'message'.\n"
                                          f" Если есть оскорбления и нецензурные слова, то верни 'result': 'False с причиной, иначе  'result': 'True' и 'message': 'Текст сообщения'\n"
                                          f"Если есть реклама то верни 'result': 'False с причиной, иначе  'result': 'True' и 'message': 'Текст сообщения'"}
        ]
        try:
            response = await self.client.chat.complete_async(model=self.model, messages=messages)
            return response.choices[0].message.content
        except Exception as e:
            return ''

    async def check_for_profanity(self, text: str) -> bool:
        """
        MistralAI модерирует отзыв. Разрешает или запрещает размещение отзыва.
        :param text:
        :return:
        """
        try:
            response = await self.chat(text)
            if not response:
                return False
            start = response.index('{')
            end = response.index('}', start)+1
            response = response[start:end]
            response_json = json.loads(response)
            return response_json.get("result") == "True"
        except Exception as e:
            return False


import requests

API_TOKEN = 'trnsl.1.1.20200516T191312Z.45f057adbe94cb3d.5ce5541e7e16f49c075b6cc95683b410654fa288'
URL = 'https://translate.yandex.net/api/v1.5/tr.json/translate'
CODES = {
    401: 'Неправильный API-ключ',
    402: 'API-ключ заблокирован',
    404: 'Превышено суточное ограничение на объем переведенного текста',
    413: 'Превышен максимально допустимый размер текста',
    422: 'Текст не может быть переведен',
    501: 'Заданное направление перевода не поддерживается'
}


def translate(text: str):
    params = {
        'key': API_TOKEN,
        'text': text,
        'lang': 'ru'
    }
    try:
        response = requests.get(url=URL, params=params, timeout=5)
    except requests.exceptions.Timeout:
        return {
            'error': 'Таймоут'
        }
    if response.status_code == 200:
        return {
            'in': text,
            'out': response.json()['text'][0]
        }
    else:
        return {
            'error': CODES.get(response.status_code) or 'Что-то пошло не так'
        }
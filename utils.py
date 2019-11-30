import functools
import re

import pymorphy2
from transliterate import translit
from transliterate.base import registry
from transliterate.contrib.languages.ru.translit_language_pack import RussianLanguagePack


class CustomRussianLanguagePack(RussianLanguagePack):
    def __init__(self):
        super().__init__()
        self.pre_processor_mapping.update({
            u'ya': u'я',
            u'ck': u'к',
            u'ph': u'ф',
            u'w': u'в',
        })


registry.register(CustomRussianLanguagePack, force=True)

_morpher = pymorphy2.MorphAnalyzer()


def sanitize(text: str) -> str:
    text = text.lower()
    text = re.sub('[^a-zа-яё0-9]+', ' ', text)
    text = text.replace('ё', 'е')
    text = re.sub(r"([a-zа-я])(\d)", r'\1 \2', text)
    text = re.sub(r"(\d)([a-zа-я])", r'\1 \2', text)
    text = text.strip()
    return text


def normalize(text: str) -> str:
    normalized = []
    for word in text.split(' '):
        normal_form = _normalize_with_pymorphy(word)

        if re.match('[a-z]+', normal_form) is not None:
            normal_form = translit(normal_form, 'ru')

        normalized.append(normal_form)
    return ' '.join(normalized)


@functools.lru_cache(maxsize=1000)
def _normalize_with_pymorphy(word: str) -> str:
    return _morpher.parse(word)[0].normal_form

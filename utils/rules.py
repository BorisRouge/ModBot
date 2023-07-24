""" Модуль с правилами можно выгружать через команду админа /get,
 редактировать и обновлять в работающем боте через команду /set.
Для правильной работы контроллера правил требуется, чтобы новое правило
принимало в качестве аргументов `text`, `result`, `checklist`
и имело метод `apply`, возвращающий `result` и `checklist`."""

import re
import requests
from urllib.parse import urlparse
from aiogram.types import Message
to_be_used = []


class Rule:

    def __init__(self, name):
        self.name = name
        to_be_used.append(self)

    def apply(self):
        raise NotImplementedError("'apply' method must be defined!")


class KeywordRule(Rule):
    """Правило, работающее по ключевым словам."""

    def __init__(self, name, keywords):
        super(self.__class__, self).__init__(name)
        self.keywords = keywords

    def apply(self, text: str, checklist: list, result: bool, **kwargs) -> (bool, list):
        not_found = True
        for kw in self.keywords:
            if kw in text.lower():
                checklist.append((self.name, True))
                not_found = False
                break
        if not_found:
            checklist.append((self.name, False))
            result = False
        return result, checklist


class ForkRule(Rule):
    """Условное правило, срабатывает только
    при удовлетворенном правиле 'Вознаграждение'."""

    def __init__(self, name):
        super(self.__class__, self).__init__(name)

    def apply(self, text: str, checklist: list, result: bool, **kwargs) -> (bool, list):
        for item in checklist:
            
            if item == ('Вознаграждение', True):
                # Находим все числа, похожие на суммы.
                amounts = re.findall(r'(\d{1,3}[.,\s]\d{3}|\d{3,})', text)
                print(amounts)
                
                if len(amounts) >= 2:  # Ищем суммы, похожие на вилку.
                    if text.index(amounts[1]) - text.index(amounts[0]) <= 30:
                        if not self._check_fork(amounts):
                            checklist.append((self.name, False))
                            result = False
                            
        return result, checklist

    def _clean(self, amount) -> int:
        """Очистка суммы от разделителей."""
        for separator in (" ", ",", "."):
            amount = amount.replace(separator, "")
        print(amount[:2])
        return int(amount[:2])
        
    def _check_fork(self, amounts) -> bool:
        """Проверка предполагаемой вилки на установленный разброс."""
        FORK_COEFF = 10
        #difference = FORK_COEFF * 10**(len(str(self._clean(amounts[0]))) - 2
                                         #Устаревшее
        
        return self._clean(amounts[1]) - self._clean(amounts[0]) <= FORK_COEFF


class LinkRule(Rule):
    """Ищет url через встроенные message.entities телеграмма."""
    def apply(self, text: str, checklist: list, result: bool, **kwargs) -> (bool, list):
        message: Message = kwargs.get('message')
        urls = self._get_urls(message)

        if urls:
            if self._ping(urls[0]):
                checklist.append((self.name, True))
            else:
                checklist.append((self.name, False))
                result = False
        else:
            checklist.append((self.name, False))
            result = False
            
        return result, checklist
        
    def _is_valid_url(self, url):
        parsed_url = urlparse(url)
        return bool(parsed_url.netloc)

    def _find_urls(self, text):
        words = text.split() 
        urls = []
        
        for word in words:
            parsed = urlparse(word)
            if parsed.scheme and parsed.netloc:
                urls.append(word)
        return urls

    def _get_urls(self, message):
        urls = []
        for e in message.entities:
            if e.type == 'url':
                urls.append(e.get_text(message.text))
            if e.type == 'text_link':
                if not e.url.startswith('tg://'):
                    urls.append(e.url)
        return urls
    #TODO: wrap get in try/except
    def _ping(self, url):
        try:
            if url.startswith('http'):
                r = requests.get(url)
                return r.ok
            else:
                http = 'http://' + url
                https = 'https://' + url
                r = requests.get(https)
                
                if r.ok:
                    return r.ok
                else:
                    r = requests.get(http)
                    return r.ok
        except:
            #log.info(f'URL: {url} is unreachable')
            return False

# Below are the initialized rules 


"""KeywordRules"""
format = KeywordRule(
    name='Формат работы',
    keywords={'формат', 'удален', 'офис', 'гибрид'})

schedule = KeywordRule(
    name='Занятость',
    keywords={
        'полн', 'частичн', 'проект', 'занятост', 'график', 'фулл-тайм', 'фулл',
        'парт', 'full time', 'full-time', 'fulltime', 'part',
    })

name = KeywordRule(
    name='Название', 
    keywords={
        'компан', 'назван', 'работодат', 'aгент', 'aгентство', 
    })

income = KeywordRule(
    name='Вознаграждение',
    keywords={
        'зп', 'оклад', 'вилка', 'заработн', 'вознагражд',
        'зарплат', 'з//п', 'з\\п', 'оплат'
    })

employment = KeywordRule(
    name='Варианты найма',
    keywords={
        'трудоустройств', 'официальн', 'самозанятост', 'ИП', 'ООО', 'СЗ',
    })


"""ConditionalRules"""
fork = ForkRule('Вилка')
link = LinkRule('Ссылка')


# Тэг, на который срабатывает проверка.
vacancy = {'#вакансия', '# вакансия', }  #'#vacancy', '# vacancy'
cv = {'#резюме', '# резюме', '#cv', '# cv', '#resume', '# resume',}
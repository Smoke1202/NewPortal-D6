from django import template

register = template.Library()


STRONG_WORDS = ["Аниме", "сериал", "News"]


@register.filter(name='filtercen')
def censor(value):
   if not isinstance(value, str):
       raise ValueError('Нельзя цензурировать не строку')

   for word in STRONG_WORDS:
       value = value.replace(word[1:], '*' * (len(word)-1))

   return value



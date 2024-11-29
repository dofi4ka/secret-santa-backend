import jinja2
environment = jinja2.Environment(autoescape=True)


START_USER_FOUND = environment.from_string("""
✅ Telegram ID найден в базе под именем <b>{{ name }}</b>

<i>Если вы видите это сообщение вам больше не нужно ничего предпринимать, \
рассылка с адресатом подарка пройдёт автоматически, \
не блокируйте бота чтобы сообщение дошло без проблем</i>
""")

START_USER_NOT_FOUND = environment.from_string("""
❌ Telegram ID не найден в базе, скорее всего вас спросить забыли

<i>Если вы считаете, что произошла ошибка, обратитесь к администратору</i>
""".strip())

BROADCAST = environment.from_string("""
📣 Рассылка адресата подарка

Здесь какойто официальный текст типо про удачу шансы хз теорию вероятности

<b>Ваш адресат</b>: <span class="tg-spoiler">{{ recepient }}</span>

<i>⚠️ Никому не пересылайте это сообщение</i>
""".strip())
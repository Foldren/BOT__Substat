import redis
from pathlib import Path
from os import environ

# Конфигурация Redis --------------------------------------------------------------------------------------------------
## Бд с сабами и chat_id пользователей в формате: chat_id_admin -> chat_id: sub_id

# Дополнительная конфигурация -----------------------------------------------------------------------------------------
IS_THIS_LOCAL = "Pycharm" in str(Path.cwd())
PARSER_URL = 'https://api-cpacash.affise.com/3.0/stats/custom'

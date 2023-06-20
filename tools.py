import datetime
from datetime import date, timedelta, datetime
from httpx import AsyncClient
from config import API_KEY, PARSER_URL, db_analysts_cid_redis, db_admins_cid_redis
from numpy import array

class SubStatTools:
    __slots__ = ()

    async def convert_dict_bytes_to_list_str(self, dict_obj, prefix_p1: str, prefix_p2: str):
        list_vals = list(dict_obj.values())
        list_keys = list(dict_obj.keys())
        result = list()
        for i in range(len(list_vals)):
            rfrmt_byte_val = await self.reformat_byte_to_str(str(list_vals[i]))
            rfrmt_byte_key = await self.reformat_byte_to_str(str(list_keys[i]))
            paramas_val = rfrmt_byte_val.split(":")
            result.append(prefix_p1 + rfrmt_byte_key + ": " + paramas_val[0] + f" {prefix_p2}: " + paramas_val[2])
        return result

    @staticmethod
    async def parse_stats(geo: str, sub_number: str, sub_ids: list[str], master_id: str, date_range: str,
                          timezone: str):
        date_from_dt_dict = {
            'day': timedelta(hours=datetime.now().hour),
            'quarter': timedelta(days=date.today().weekday()),
            'month': timedelta(days=date.today().day - 1),
        }
        async with AsyncClient(verify=False) as client:
            p_get_stat_rq = {
                'slice[]': [date_range, f'sub{sub_number}', 'country'],
                'filter[date_from]': str(date.today() - date_from_dt_dict[date_range]),
                'filter[date_to]': str(date.today()),
                'fields[]': ['clicks', 'conversions'],
                'filter[partner][]': master_id,
                'filter[sub1][]': sub_ids,
                'conversionTypes[]': ['confirmed', 'pending'],
                'timezone': timezone,
                'filter[country][]': geo,
                'api-key': API_KEY,
            }

            r_stats = await client.get(url=PARSER_URL, params=p_get_stat_rq, timeout=10.0)
            response = r_stats.json()

            return {
                'clicks': response['stats'][0]['traffic']['raw'] if response['stats'] else 0,
                'registrations': response['stats'][0]['actions']['confirmed']['count'] if response['stats'] else 0,
                'deposits': response['stats'][0]['actions']['pending']['count'] if response['stats'] else 0,
            }

    @staticmethod
    async def get_stats_msg_from_callback(callback_data, stats):
        return f"Sub_number: {callback_data.split(':')[1][3:]}\n" \
               f"Клики: {stats['clicks']}\n" \
               f"Регистрации: {stats['registrations']}\n" \
               f"Депозиты: {stats['deposits']}"

    @staticmethod
    async def get_list_users_keys(db_obj, admin: bool = True):
        chat_ids_list: list
        if db_obj is not None:
            chat_ids_list = list(db_obj.keys())
            if admin: chat_ids_list.pop(0)
        else:
            chat_ids_list = list()
        return chat_ids_list

    # Списки admin для доступа к боту
    @staticmethod
    async def get_list_admins():
        return array(db_admins_cid_redis.keys()).astype("int64")

    # Списки analysts для доступа к боту
    @staticmethod
    async def get_list_analysts():
        return array(db_analysts_cid_redis.keys()).astype("int64")

    @staticmethod
    async def get_strip_sub_id(answer: str):
        result: list = []
        list_answer = answer.split("\n")
        for i in range(len(list_answer)):
            result.append(list_answer[i].strip())
        return result

    @staticmethod
    async def reformat_byte_to_str(str_b) -> str:
        return str_b.replace("'", "").replace("b", "", 1)

    @staticmethod
    async def get_list_sub_id(str_sub_ids: str) -> list:
        return str_sub_ids.split(",") if "," in str_sub_ids else [str_sub_ids]

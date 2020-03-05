from django.conf import settings
from collections import OrderedDict
from utils.redis_pool import POOL
import redis

CONN = redis.Redis(connection_pool=POOL)

def query_dill(query):
    query_list = query.split('-')
    print(query_list)
    return int(query_list[0]), int(query_list[1])


def score_rank_c(request, start=0, end=CONN.zcard(settings.SCORE_KEY)):
    score_dict = {}
    score_dict_s = OrderedDict()
    curr_rank = CONN.zrevrank(settings.SCORE_KEY, request.user.name)
    all_score = CONN.zrevrange(settings.SCORE_KEY, start, end - 1, True)
    for rank, values in enumerate(all_score):
        score_dict_s[rank + 1 + start] = {'name': values[0]}
        score_dict_s[rank + 1 + start]['score'] = values[1]
    if not curr_rank == None:
        user = request.user.scorerank_set.all().first()
        score_dict['curr'] = {'rank': curr_rank + 1, 'name': request.user.name, 'score': user.score}
    score_dict['all_score'] = score_dict_s
    return score_dict


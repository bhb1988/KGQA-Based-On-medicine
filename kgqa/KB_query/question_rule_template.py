"""
@desc: 为每个问题设定语义模板
"""
from refo import finditer, Predicate, Star, Any, Disjunction
import re
import random


# TODO SPARQL前缀和模板
SPARQL_PREXIX = u"""
PREFIX : <http://www.kgdrug.com#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
"""
# SPARQL_SELECT_TEM = u"{prefix}\n" + \
#              u"SELECT DISTINCT {select} WHERE {{\n" + \
#              u"{expression}\n" + \
#              u"}}\n"

SPARQL_SELECT_TEM = u"SELECT DISTINCT {select} WHERE {{\n" + \
                    u"{expression}\n" + \
                    u"}}\n"

class W(Predicate):
    def __init__(self, token=".*", pos=".*"):
        # 正则表达式
        self.token = re.compile(token + "$")
        self.pos = re.compile(pos + "$")
        super(W, self).__init__(self.match)

    def match(self, word):
        m1 = self.token.match(word.token.decode('utf-8'))
        m2 = self.pos.match(word.pos)
        return m1 and m2


class Rule(object):
    def __init__(self, condition_num, condition=None, action=None):
        assert condition and action
        self.condition = condition
        self.action = action
        self.condition_num = random.random()

    def apply(self, sentence):
        matches = []
        for m in finditer(self.condition, sentence):
            i, j = m.span()
            matches.extend(sentence[i:j])

        return self.action(matches), self.condition_num


class QuestionSet:
    def __init__(self):
        pass

    @staticmethod
    def has_production_to_person_question(word_objects):
        '''
        代表作
        :param word_objects:
        :return:
        '''
        select = u"?x"

        sparql = None
        for w in word_objects:
            if w.pos == pos_person:
                e = u"<'{person}'> <代表作品> ?x.".format(person=w.token.decode('utf-8'))

                sparql = SPARQL_SELECT_TEM.format(select=select,
                                                  expression=e)
                break
        return sparql


# TODO 代表作品
# 词性
pos_person = 'nr'
person_entity = (W(pos=pos_person) | W(pos='x'))
# 问题关键词
production_keyword = (W('代表作') | W('作品'))

# 规则合集
rules = [
    Rule(condition_num=2, condition=person_entity + Star(Any(),greedy=False) + production_keyword + Star(Any(),greedy=False), action=QuestionSet.has_production_to_person_question),

    ]

#!/usr/bin/python3
# -*- coding: utf-8 -*-
#########################################################################
# File Name: gstore_sparql_endpoint.py
# Author: baihongbo
# mail: bhbku@qq.com
# Created Time: 2018-05-24 17:38:27
#########################################################################

from urllib import request
from urllib import parse
from collections import OrderedDict
import json


class gStore:
    def __init__(self):
        self.base_url = self.get_base_url()

    def get_base_url(self):
        """
        基础url
        """
        base_url = 'http://pkubase.gstore-pku.com/'
        mid_url = parse.quote('?operation=query&format={form}&sparql='.format(form='json'))
        base_url = base_url + mid_url
        return base_url

    def get_sparql_result(self, query):
        """sparql查询"""
        encode_sparql_url = parse.quote(query)
        url = self.base_url + encode_sparql_url
        data = request.urlopen(url).read()
        data = data.decode("utf-8")
        data = json.loads(data)
        return data

    @staticmethod
    def parse_result(query_result):
        """
        解析返回的结果
        """
        try:
            query_head = query_result['head']['vars']
            query_results = list()
            for r in query_result['results']['bindings']:
                temp_dict = OrderedDict()
                for h in query_head:
                    temp_dict[h] = r[h]["value"]
                query_results.append(temp_dict)
            return query_head, query_results
        except KeyError:
            print("KeyError：}")
            return None, query_result

    def print_result_to_string(self, query_result):
        """
        直接打印结果，用于测试
        """
        pass

    def get_sparql_result_value(self, query_result):
        """
        用列表存储结果的值
        :param query_result:
        :param return:
        """
        query_head, query_result = self.parse_result(query_result)
        if query_result is None:
            return query_result
        else:
            values = list()
            for qr in query_result:
                for _, value in qr.items():
                    values.append(value)
            return values
                

if __name__ == "__main__":
    gs = gStore()
    my_query = """
        select ?y 
            where 
                { 
	           <北京大学1> <主要奖项1> ?y. 
                    }
    """
    result = gs.get_sparql_result(my_query)
    rs = gs.get_sparql_result_value(result)
    print(rs)

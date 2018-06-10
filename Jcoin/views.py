# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
from django.http import JsonResponse
from Jcoin.block_chain import BlockChain
from django.views.generic import View

block_chain = BlockChain()


class BaseView(View):

    @staticmethod
    def render_to_response(data, status=0, message='success'):

        response = {
            'status': status,
            'message': message,
            'data': data
        }

        return JsonResponse(response)

    @staticmethod
    def render_error_response(data, status=-1, message='failure'):
        response = {
            'status': status,
            'message': message,
            'data': data
        }

        return JsonResponse(response)


class GetChainList(BaseView):

    def get(self, request):
        return self.render_to_response(block_chain.get_chain())


class CreateBlock(BaseView):

    def get(self, request):
        previous_block = block_chain.last_block()
        block = block_chain.create_block(previous_block['hash'])
        return self.render_to_response(block)


class IsValidChain(BaseView):

    def get(self, request):
        is_valid_chain = block_chain.is_chain_valid()
        data = {'valid_chain': is_valid_chain}
        return self.render_to_response(data)

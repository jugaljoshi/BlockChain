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


class MineBlock(BaseView):

    def get(self, request):
        previous_block = block_chain.last_block()
        block = block_chain.mine_block(previous_block['hash'])
        return self.render_to_response(data=block)


class IsValidChain(BaseView):

    def get(self, request):
        is_valid_chain = block_chain.is_chain_valid()
        data = {'valid_chain': is_valid_chain}
        return self.render_to_response(data)


class NodeConnect(BaseView):

    def post(self, request):
        node_address_list = request.POST.get('nodes')

        if not node_address_list:
            return self.render_error_response({'message': 'Nodes are not provided'})
        node_added = block_chain.add_nodes(node_address_list)
        return self.render_error_response({'nodes': node_added})


class AddTransaction(BaseView):

    def post(self, request):
        params_needed = ['sender', 'receiver', 'amount']

        if not all(key in request.POST.keys() for key in params_needed):
            return self.render_to_response({'message': 'All params are not available for a transaction'})

        index = block_chain.add_transaction(request.POST.get('sender'),
                                            request.POST.get('receiver'),
                                            request.POST.get('amount'))

        return self.render_to_response({'message': f'This transaction is added to block {index}'})


class SyncChain(BaseView):

    def post(self, request):
        pass
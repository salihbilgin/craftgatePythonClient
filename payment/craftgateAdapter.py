import requests
import os
import uuid
import json
import hashlib
import hmac
import base64

from payment.craftgateOptions import *


class Guid:
    @staticmethod
    def generate():
        if hasattr(os, "urandom"):
            return str(uuid.UUID(bytes=os.urandom(16)))
        else:
            return str(uuid.uuid4())


def generate(options, path, random_string, request=None):
    hash_str = options.base_url + path + options.api_key + options.secret_key + random_string + (
        json.dumps(request) if request else '')
    hashed = hashlib.sha256(hash_str.encode('utf-8')).digest()
    result = base64.b64encode(hashed).decode('utf-8')
    return result


def generate_hash(hash_string):
    hashed = hashlib.sha256(hash_string.encode('utf-8')).hexdigest()
    return hashed


class BaseAdapterProd():
    def __init__(self):
        self.options = CraftgateOptionsProd()
        self.randomString = Guid.generate()

    def httpGet(self, path, headers=None):
        url = self.prepareUrl(path)
        headers = self.prepareHeaders(headers, path)
        response = requests.get(url, headers=headers)
        return response.json()

    def httpPost(self, path, request=None, headers=None):
        url = self.prepareUrl(path)
        headers = self.prepareHeaders(headers, path, request)
        response = requests.post(url, json=request, headers=headers)
        return response.json()

    def httpPut(self, path, request, headers=None):
        url = self.prepareUrl(path)
        headers = self.prepareHeaders(headers, path, request)
        response = requests.put(url, json=request, headers=headers)
        return response.json()

    def httpDelete(self, path, headers=None):
        url = self.prepareUrl(path)
        headers = self.prepareHeaders(headers, path)
        response = requests.delete(url, headers=headers)
        return response.json()

    def prepareHeaders(self, headers, path, request=None):
        if headers is None:
            headers = {'accept': 'application/json', 'content-type': 'application/json'}
        headers['x-api-key'] = self.options.get_api_key()
        headers['x-rnd-key'] = self.randomString
        headers['x-auth-version'] = 'v1'
        headers['x-client-version'] = 'craftgate-python-client:1.0.0'
        headers['x-signature'] = generate(self.options, path, self.randomString, request)
        return headers

    def prepareUrl(self, path):
        return self.options.get_base_url() + '/' + path.strip('/')


class BaseAdapterTest():
    def __init__(self):
        self.options = CraftgateOptionsTest()
        self.randomString = Guid.generate()

    def httpGet(self, path, headers=None):
        url = self.prepareUrl(path)
        headers = self.prepareHeaders(headers, path)
        response = requests.get(url, headers=headers)
        return response.json()

    def httpPost(self, path, request=None, headers=None):
        url = self.prepareUrl(path)
        headers = self.prepareHeaders(headers, path, request)
        response = requests.post(url, json=request, headers=headers)
        return response.json()

    def httpPut(self, path, request, headers=None):
        url = self.prepareUrl(path)
        headers = self.prepareHeaders(headers, path, request)
        response = requests.put(url, json=request, headers=headers)
        return response.json()

    def httpDelete(self, path, headers=None):
        url = self.prepareUrl(path)
        headers = self.prepareHeaders(headers, path)
        response = requests.delete(url, headers=headers)
        return response.json()

    def prepareHeaders(self, headers, path, request=None):
        if headers is None:
            headers = {'accept': 'application/json', 'content-type': 'application/json'}
        headers['x-api-key'] = self.options.get_api_key()
        headers['x-rnd-key'] = self.randomString
        headers['x-auth-version'] = 'v1'
        headers['x-client-version'] = 'craftgate-python-client:1.0.0'
        headers['x-signature'] = generate(self.options, path, self.randomString, request)

        return headers

    def prepareUrl(self, path):
        return self.options.get_base_url() + '/' + path.strip('/')

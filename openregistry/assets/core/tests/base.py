# -*- coding: utf-8 -*-
import json
import os
from uuid import uuid4
from copy import deepcopy
from urllib import urlencode
from base64 import b64encode
from datetime import datetime
from requests.models import Response
from webtest import TestApp

from openregistry.api.tests.base import BaseWebTest
from openregistry.api.utils import apply_data_patch
from openregistry.api.constants import SESSION


now = datetime.now()


class BaseAssetWebTest(BaseWebTest):
    initial_data = None
    initial_status = None
    docservice = False
    relative_to = os.path.dirname(__file__)

    def set_status(self, status, extra=None):
        data = {'status': status}
        if status == "pending":
            data['status'] = status

        if extra:
            data.update(extra)

        asset = self.db.get(self.asset_id)
        asset.update(apply_data_patch(asset, data))
        self.db.save(asset)

        response = self.app.get('/assets/{}'.format(self.asset_id))
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.content_type, 'application/json')
        asset = response.json['data']
        self.assertEqual(asset['status'], status)
        return asset

    def setUp(self):
        super(BaseAssetWebTest, self).setUp()
        if self.docservice:
            self.setUpDS()

    def setUpDS(self):
        self.app.app.registry.docservice_url = 'http://localhost'
        test = self
        def request(method, url, **kwargs):
            response = Response()
            if method == 'POST' and '/upload' in url:
                url = test.generate_docservice_url()
                response.status_code = 200
                response.encoding = 'application/json'
                response._content = '{{"data":{{"url":"{url}","hash":"md5:{md5}","format":"application/msword","title":"name.doc"}},"get_url":"{url}"}}'.format(url=url, md5='0'*32)
                response.reason = '200 OK'
            return response

        self._srequest = SESSION.request
        SESSION.request = request

    def setUpBadDS(self):
        self.app.app.registry.docservice_url = 'http://localhost'
        def request(method, url, **kwargs):
            response = Response()
            response.status_code = 403
            response.encoding = 'application/json'
            response._content = '"Unauthorized: upload_view failed permission check"'
            response.reason = '403 Forbidden'
            return response

        self._srequest = SESSION.request
        SESSION.request = request

    def generate_docservice_url(self):
        uuid = uuid4().hex
        key = self.app.app.registry.docservice_key
        keyid = key.hex_vk()[:8]
        signature = b64encode(key.signature("{}\0{}".format(uuid, '0' * 32)))
        query = {'Signature': signature, 'KeyID': keyid}
        return "http://localhost/get/{}?{}".format(uuid, urlencode(query))

    def create_asset(self, extra=None):
        data = deepcopy(self.initial_data)
        if extra:
            data.update(extra)
        response = self.app.post_json('/assets', {'data': data})
        asset = response.json['data']
        self.asset_token = response.json['access']['token']
        self.asset_id = asset['id']
        status = asset['status']
        if self.initial_status != status:
            asset = self.set_status(self.initial_status)
        return asset

    def tearDownDS(self):
        SESSION.request = self._srequest

    def tearDown(self):
        if self.docservice:
            self.tearDownDS()
        if hasattr(self, 'asset_id'): # XXX We have tests that create asset out of setUp method.
            del self.db[self.asset_id]
        super(BaseAssetWebTest, self).tearDown()


class DumpsTestAppwebtest(TestApp):
    hostname = "api-sandbox.openregistry.org"

    def do_request(self, req, status=None, expect_errors=None):
        req.headers.environ["HTTP_HOST"] = self.hostname
        if hasattr(self, 'file_obj') and not self.file_obj.closed:
            self.file_obj.write(req.as_bytes(True))
            self.file_obj.write("\n")
            if req.body:
                try:
                    self.file_obj.write(
                            'DATA:\n' + json.dumps(json.loads(req.body), indent=2, ensure_ascii=False).encode('utf8'))
                    self.file_obj.write("\n")
                except:
                    pass
            self.file_obj.write("\n")
        resp = super(DumpsTestAppwebtest, self).do_request(req, status=status, expect_errors=expect_errors)
        if hasattr(self, 'file_obj') and not self.file_obj.closed:
            headers = [(n.title(), v)
                       for n, v in resp.headerlist
                       if n.lower() != 'content-length']
            headers.sort()
            self.file_obj.write(str('Response: %s\n%s\n') % (
                resp.status,
                str('\n').join([str('%s: %s') % (n, v) for n, v in headers]),
            ))

            if resp.testbody:
                try:
                    self.file_obj.write(json.dumps(json.loads(resp.testbody), indent=2, ensure_ascii=False).encode('utf8'))
                except:
                    pass
            self.file_obj.write("\n\n")
        return resp

# -*- coding: utf-8 -*-

from uuid import uuid4
import unittest

from openprocurement.api.tests.base import create_blacklist
from openregistry.assets.core.constants import (
    STATUS_CHANGES,
    ASSET_STATUSES,
    SANDBOX_MODE,
    DEFAULT_ACCELERATION
)
from openregistry.assets.core.utils import calculate_business_date
# AssetResourceTest


@unittest.skipIf(not SANDBOX_MODE, 'If sandbox mode is disabled assetParameters has not procurementMethodDetails field')
def sandbox_parameter(self):
    response = self.app.post_json('/', {'data': self.initial_data})
    response_sandbox_parameters = response.json['data']['sandboxParameters']
    default_sandbox_parameters = "quick, accelerator={}".format(DEFAULT_ACCELERATION)
    self.assertEqual(response_sandbox_parameters, default_sandbox_parameters)


def patch_asset(self):
    response = self.app.get('/')
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(len(response.json['data']), 0)

    asset = self.create_resource()
    dateModified = asset.pop('dateModified')

    response = self.app.patch_json('/{}'.format(asset['id']),
                                   headers=self.access_header,
                                   params={'data': {'title': ' PATCHED'}})
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertNotEqual(response.json['data']['dateModified'], dateModified)

    asset = self.create_resource()
    self.set_status('draft')

    # Move status from Draft to Active
    response = self.app.patch_json('/{}'.format(asset['id']),
                                   headers=self.access_header,
                                   params={'data': {'status': 'active'}},
                                   status=403)
    self.assertEqual(response.status, '403 Forbidden')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['errors'][0]['name'], u'data')
    self.assertEqual(response.json['errors'][0]['location'], u'body')
    self.assertEqual(response.json['errors'][0]['description'], u"Can't update asset in current (draft) status")

    # Move status from Draft to Deleted
    response = self.app.patch_json('/{}'.format(asset['id']),
                                   headers=self.access_header,
                                   params={'data': {'status': 'deleted'}},
                                   status=403)
    self.assertEqual(response.status, '403 Forbidden')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['errors'][0]['name'], u'data')
    self.assertEqual(response.json['errors'][0]['location'], u'body')
    self.assertEqual(response.json['errors'][0]['description'], u"Can't update asset in current (draft) status")

    # Move status from Draft to Complete
    response = self.app.patch_json('/{}'.format(asset['id']),
                                   headers=self.access_header,
                                   params={'data': {'status': 'complete'}},
                                   status=403)
    self.assertEqual(response.status, '403 Forbidden')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['errors'][0]['name'], u'data')
    self.assertEqual(response.json['errors'][0]['location'], u'body')
    self.assertEqual(response.json['errors'][0]['description'], u"Can't update asset in current (draft) status")

    # Move status from Draft to Pending
    response = self.app.patch_json('/{}'.format(asset['id']),
                                   headers=self.access_header,
                                   params={'data': {'status': 'pending'}})
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['data']['status'], 'pending')

    # Move status from Pending to Draft
    response = self.app.patch_json('/{}'.format(asset['id']),
                                   headers=self.access_header,
                                   params={'data': {'status': 'draft'}},
                                   status=403)
    self.assertEqual(response.status, '403 Forbidden')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['errors'][0]['name'], u'data')
    self.assertEqual(response.json['errors'][0]['location'], u'body')
    self.assertEqual(response.json['errors'][0]['description'], u"Can't switch asset to draft status")

    # Move status from Pending to Active
    response = self.app.patch_json('/{}'.format(asset['id']),
                                   headers=self.access_header,
                                   params={'data': {'status': 'active'}},
                                   status=403)
    self.assertEqual(response.status, '403 Forbidden')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['errors'][0]['name'], u'data')
    self.assertEqual(response.json['errors'][0]['location'], u'body')
    self.assertEqual(response.json['errors'][0]['description'], u"Can't update asset in current (pending) status")

    # Move status from Pending to Complete
    response = self.app.patch_json('/{}'.format(asset['id']),
                                   headers=self.access_header,
                                   params={'data': {'status': 'complete'}},
                                   status=403)
    self.assertEqual(response.status, '403 Forbidden')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['errors'][0]['name'], u'data')
    self.assertEqual(response.json['errors'][0]['location'], u'body')
    self.assertEqual(response.json['errors'][0]['description'], u"Can't update asset in current (pending) status")

    # Move status from Pending to Deleted
    response = self.app.patch_json('/{}'.format(asset['id']),
                                   headers=self.access_header,
                                   params={'data': {'status': 'deleted'}})
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['data']['status'], 'deleted')

    # Move status from Deleted to Draft
    response = self.app.patch_json('/{}'.format(asset['id']),
                                   headers=self.access_header,
                                   params={'data': {'status': 'draft'}},
                                   status=403)
    self.assertEqual(response.status, '403 Forbidden')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['errors'][0]['name'], u'data')
    self.assertEqual(response.json['errors'][0]['location'], u'body')
    self.assertEqual(response.json['errors'][0]['description'], u"Can't update asset in current (deleted) status")

    # Move status from Deleted to Pending
    response = self.app.patch_json('/{}'.format(asset['id']),
                                   headers=self.access_header,
                                   params={'data': {'status': 'pending'}},
                                   status=403)
    self.assertEqual(response.status, '403 Forbidden')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['errors'][0]['name'], u'data')
    self.assertEqual(response.json['errors'][0]['location'], u'body')
    self.assertEqual(response.json['errors'][0]['description'], u"Can't update asset in current (deleted) status")

    # Move status from Deleted to Active
    response = self.app.patch_json('/{}'.format(asset['id']),
                                   headers=self.access_header,
                                   params={'data': {'status': 'active'}},
                                   status=403)
    self.assertEqual(response.status, '403 Forbidden')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['errors'][0]['name'], u'data')
    self.assertEqual(response.json['errors'][0]['location'], u'body')
    self.assertEqual(response.json['errors'][0]['description'], u"Can't update asset in current (deleted) status")

    # Move status from Deleted to Complete
    response = self.app.patch_json('/{}'.format(asset['id']),
                                   headers=self.access_header,
                                   params={'data': {'status': 'complete'}},
                                   status=403)
    self.assertEqual(response.status, '403 Forbidden')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['errors'][0]['name'], u'data')
    self.assertEqual(response.json['errors'][0]['location'], u'body')
    self.assertEqual(response.json['errors'][0]['description'], u"Can't update asset in current (deleted) status")


def asset_concierge_patch(self):
    asset = self.create_resource()

    response = self.app.get('/{}'.format(asset['id']))
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['data'], asset)

    # Move status from Draft to Pending
    response = self.app.patch_json('/{}'.format(asset['id']),
                                   headers=self.access_header,
                                   params={'data': {'status': 'pending'}})
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['data']['status'], 'pending')

    self.app.authorization = ('Basic', ('concierge', ''))

    # Move status from pending to verification
    response = self.app.patch_json('/{}'.format(
        asset['id']), {'data': {'status': 'verification'}})
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['data']['status'], 'verification')


    # Move status from verification to Pending
    response = self.app.patch_json('/{}'.format(
        asset['id']), {'data': {'status': 'pending'}})
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['data']['status'], 'pending')


    # Move status from pending to verification
    response = self.app.patch_json('/{}'.format(
        asset['id']), {'data': {'status': 'verification'}})
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['data']['status'], 'verification')

    # Move status from verification to Active withour relatedLot
    response = self.app.patch_json('/{}'.format(
        asset['id']), {'data': {'status': 'active'}}, status=422)
    self.assertEqual(response.status, '422 Unprocessable Entity')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['errors'][0]['description'][0], 'This field is required.')

    # Move status from verification to Active
    relatedLot = uuid4().hex
    response = self.app.patch_json('/{}'.format(
        asset['id']), {'data': {'status': 'active', 'relatedLot': relatedLot}})
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['data']['status'], 'active')
    self.assertEqual(response.json['data']['relatedLot'], relatedLot)

    # Move status from Active to Draft
    response = self.app.patch_json('/{}'.format(
        asset['id']), {'data': {'status': 'draft'}}, status=403)
    self.assertEqual(response.status, '403 Forbidden')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['errors'][0]['name'], u'data')
    self.assertEqual(response.json['errors'][0]['location'], u'body')
    self.assertEqual(response.json['errors'][0]['description'], u"Can't switch asset to draft status")

    # Move status from Active to Deleted
    response = self.app.patch_json('/{}'.format(
        asset['id']), {'data': {'status': 'deleted'}}, status=403)
    self.assertEqual(response.status, '403 Forbidden')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['errors'][0]['name'], u'data')
    self.assertEqual(response.json['errors'][0]['location'], u'body')
    self.assertEqual(response.json['errors'][0]['description'], u"Can't update asset in current (active) status")

    # Move status from Active to Pending
    response = self.app.patch_json('/{}'.format(
        asset['id']), {'data': {'status': 'pending'}})
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['data']['status'], 'pending')
    self.assertNotIn('relatedLot', response.json['data'])

    # Move status from Pending to Deleted
    response = self.app.patch_json('/{}'.format(
        asset['id']), {'data': {'status': 'deleted'}}, status=403)
    self.assertEqual(response.status, '403 Forbidden')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['errors'][0]['name'], u'data')
    self.assertEqual(response.json['errors'][0]['location'], u'body')
    self.assertEqual(response.json['errors'][0]['description'], u"Can't update asset in current (pending) status")

    # Move status from Pending to Draft
    response = self.app.patch_json('/{}'.format(
        asset['id']), {'data': {'status': 'draft'}}, status=403)
    self.assertEqual(response.status, '403 Forbidden')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['errors'][0]['name'], u'data')
    self.assertEqual(response.json['errors'][0]['location'], u'body')
    self.assertEqual(response.json['errors'][0]['description'], u"Can't switch asset to draft status")

    # Move status from Pending to Complete
    response = self.app.patch_json('/{}'.format(
        asset['id']), {'data': {'status': 'complete'}}, status=403)
    self.assertEqual(response.status, '403 Forbidden')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['errors'][0]['name'], u'data')
    self.assertEqual(response.json['errors'][0]['location'], u'body')
    self.assertEqual(response.json['errors'][0]['description'], u"Can't update asset in current (pending) status")


    # Move status from pending to verification
    response = self.app.patch_json('/{}'.format(asset['id']),
                                   headers=self.access_header,
                                   params={'data': {'status': 'verification'}})
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['data']['status'], 'verification')


    # Move status from verification to active
    relatedLot = uuid4().hex
    response = self.app.patch_json('/{}'.format(
        asset['id']), {'data': {'status': 'active', 'relatedLot': relatedLot}})
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['data']['status'], 'active')
    self.assertEqual(response.json['data']['relatedLot'], relatedLot)

    # Move status from Active to Complete
    response = self.app.patch_json('/{}'.format(
        asset['id']), {'data': {'status': 'complete'}})
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['data']['status'], 'complete')

    # Move status from Complete to Draft
    response = self.app.patch_json('/{}'.format(
        asset['id']), {'data': {'status': 'deleted'}}, status=403)
    self.assertEqual(response.status, '403 Forbidden')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['errors'][0]['name'], u'data')
    self.assertEqual(response.json['errors'][0]['location'], u'body')
    self.assertEqual(response.json['errors'][0]['description'], u"Can't update asset in current (complete) status")

    # Move status from Complete to Pending
    response = self.app.patch_json('/{}'.format(
        asset['id']), {'data': {'status': 'deleted'}}, status=403)
    self.assertEqual(response.status, '403 Forbidden')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['errors'][0]['name'], u'data')
    self.assertEqual(response.json['errors'][0]['location'], u'body')
    self.assertEqual(response.json['errors'][0]['description'], u"Can't update asset in current (complete) status")

    # Move status from Complete to Active
    response = self.app.patch_json('/{}'.format(
        asset['id']), {'data': {'status': 'deleted'}}, status=403)
    self.assertEqual(response.status, '403 Forbidden')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['errors'][0]['name'], u'data')
    self.assertEqual(response.json['errors'][0]['location'], u'body')
    self.assertEqual(response.json['errors'][0]['description'], u"Can't update asset in current (complete) status")

    # Move status from Complete to Deleted
    response = self.app.patch_json('/{}'.format(
        asset['id']), {'data': {'status': 'deleted'}}, status=403)
    self.assertEqual(response.status, '403 Forbidden')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['errors'][0]['name'], u'data')
    self.assertEqual(response.json['errors'][0]['location'], u'body')
    self.assertEqual(response.json['errors'][0]['description'], u"Can't update asset in current (complete) status")


def administrator_change_delete_status(self):
    response = self.app.get('/')
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(len(response.json['data']), 0)

    self.app.authorization = ('Basic', ('broker', ''))
    asset = self.create_resource()

    response = self.app.get('/{}'.format(asset['id']))
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['data'], asset)

    self.app.authorization = ('Basic', ('administrator', ''))

    response = self.app.patch_json(
        '/{}'.format(asset['id']),
        {'data': {'status': 'pending'}}
    )
    self.assertEqual(response.status, '200 OK')

    response = self.app.patch_json(
        '/{}'.format(asset['id']),
        {'data': {'status': 'deleted'}}
    )
    self.assertEqual(response.status, '200 OK')

    response = self.app.patch_json('/{}'.format(
        asset['id']), {'data': {'status': 'deleted'}}, status=403)
    self.assertEqual(response.status, '403 Forbidden')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['errors'][0]['name'], u'data')
    self.assertEqual(response.json['errors'][0]['location'], u'body')
    self.assertEqual(response.json['errors'][0]['description'], u"Can't update asset in current (deleted) status")


def administrator_change_complete_status(self):
    response = self.app.get('/')
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(len(response.json['data']), 0)

    self.app.authorization = ('Basic', ('broker', ''))
    asset = self.create_resource()

    response = self.app.get('/{}'.format(asset['id']))
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['data'], asset)

    self.app.authorization = ('Basic', ('administrator', ''))

    response = self.app.patch_json(
        '/{}'.format(asset['id']),
        {'data': {'status': 'pending'}}
    )
    self.assertEqual(response.status, '200 OK')

    response = self.app.patch_json(
        '/{}'.format(asset['id']),
        {'data': {'status': 'verification'}}
    )
    self.assertEqual(response.status, '200 OK')

    # XXX TODO Describe actives
    response = self.app.patch_json(
        '/{}'.format(asset['id']),
        {'data': {'status': 'pending'}}
    )
    self.assertEqual(response.status, '200 OK')

    response = self.app.patch_json(
        '/{}'.format(asset['id']),
        {'data': {'status': 'verification'}}
    )
    self.assertEqual(response.status, '200 OK')

    response = self.app.patch_json(
        '/{}'.format(asset['id']),
        {'data': {'status': 'active', 'relatedLot': uuid4().hex}}
    )
    self.assertEqual(response.status, '200 OK')

    response = self.app.patch_json(
        '/{}'.format(asset['id']),
        {'data': {'status': 'pending'}}
    )
    self.assertEqual(response.status, '200 OK')

    response = self.app.patch_json(
        '/{}'.format(asset['id']),
        {'data': {'status': 'verification'}}
    )
    self.assertEqual(response.status, '200 OK')

    response = self.app.patch_json(
        '/{}'.format(asset['id']),
        {'data': {'status': 'active', 'relatedLot': uuid4().hex}}
    )
    self.assertEqual(response.status, '200 OK')

    response = self.app.patch_json(
        '/{}'.format(asset['id']),
        {'data': {'status': 'complete'}}
    )
    self.assertEqual(response.status, '200 OK')

    response = self.app.patch_json('/{}'.format(
        asset['id']), {'data': {'status': 'deleted'}}, status=403)
    self.assertEqual(response.status, '403 Forbidden')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['errors'][0]['name'], u'data')
    self.assertEqual(response.json['errors'][0]['location'], u'body')
    self.assertEqual(response.json['errors'][0]['description'], u"Can't update asset in current (complete) status")

# AssetTest


def simple_add_asset(self):

    u = self.asset_model(self.initial_data)
    u.assetID = "UA-X"

    assert u.id is None
    assert u.rev is None

    u.store(self.db)

    assert u.id is not None
    assert u.rev is not None

    fromdb = self.db.get(u.id)

    assert u.assetID == fromdb['assetID']
    assert u.doc_type == "Asset"

    u.delete_instance(self.db)


# Asset workflow test
ROLES = ['asset_owner', 'Administrator', 'concierge', 'convoy']
STATUS_BLACKLIST = create_blacklist(STATUS_CHANGES, ASSET_STATUSES, ROLES)


def check_patch_status_200(self, asset_id, asset_status, headers=None, extra_data={}):
    patch_data = {'status': asset_status}
    patch_data = patch_data.update(extra_data) or patch_data
    response = self.app.patch_json(
        '/{}'.format(asset_id),
        params={'data': patch_data},
        headers=headers
    )
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['data']['status'], patch_data['status'])
    for field, value in extra_data.items():
        self.assertEqual(response.json['data'][field], value)
    return response


def check_patch_status_403(self, asset_id, asset_status, headers=None):
    response = self.app.patch_json(
        '/{}'.format(asset_id),
        params={'data': {'status': asset_status}},
        headers=headers,
        status=403
    )
    self.assertEqual(response.status, '403 Forbidden')
    self.assertEqual(response.content_type, 'application/json')
    return response


def change_draft_asset(self):
    self.initial_status = 'draft'
    response = self.app.get('/')
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(len(response.json['data']), 0)

    asset = self.create_resource()

    self.app.authorization = ('Basic', ('concierge', ''))

    # Move from 'draft' to one of blacklist status
    for status in STATUS_BLACKLIST['draft']['concierge']:
        check_patch_status_403(self, asset['id'], status)


    self.app.authorization = ('Basic', ('convoy', ''))

    # Move from 'draft' to one of blacklist status
    for status in STATUS_BLACKLIST['draft']['convoy']:
        check_patch_status_403(self, asset['id'], status)


    self.app.authorization = ('Basic', ('broker', ''))

    # Move from 'draft' to one of blacklist status
    for status in STATUS_BLACKLIST['draft']['asset_owner']:
        check_patch_status_403(self, asset['id'], status, self.access_header)

    # Move from 'draft' to 'draft' status
    check_patch_status_200(self, asset['id'], 'draft', self.access_header)

    # Move from 'draft' to 'pending' status
    check_patch_status_200(self, asset['id'], 'pending', self.access_header)

    asset = self.create_resource()


    self.app.authorization = ('Basic', ('administrator', ''))

    # Move from 'draft' to one of blacklist status
    for status in STATUS_BLACKLIST['draft']['Administrator']:
        check_patch_status_403(self, asset['id'], status)

    # Move from 'draft' to 'draft' status
    check_patch_status_200(self, asset['id'], 'draft', self.access_header)

    # Move from 'draft' to 'pending' status
    check_patch_status_200(self, asset['id'], 'pending', self.access_header)


def change_pending_asset(self):
    response = self.app.get('/')
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(len(response.json['data']), 0)

    asset = self.create_resource()


    self.app.authorization = ('Basic', ('convoy', ''))

    # Move from 'pending' to one of blacklist status
    for status in STATUS_BLACKLIST['pending']['convoy']:
        check_patch_status_403(self, asset['id'], status)


    self.app.authorization = ('Basic', ('broker', ''))

    # Move from 'pending' to one of blacklist status
    for status in STATUS_BLACKLIST['pending']['asset_owner']:
        check_patch_status_403(self, asset['id'], status, self.access_header)

    # Move from 'pending' to 'pending' status
    check_patch_status_200(self, asset['id'], 'pending', self.access_header)

    # Move from 'pending' to 'deleted' status
    check_patch_status_200(self, asset['id'], 'deleted', self.access_header)


    asset = self.create_resource()


    self.app.authorization = ('Basic', ('administrator', ''))

    # Move from 'pending' to one of blacklist status
    for status in STATUS_BLACKLIST['pending']['Administrator']:
        check_patch_status_403(self, asset['id'], status)

    # Move from 'pending' to 'pending' status
    check_patch_status_200(self, asset['id'], 'pending')

    # Move from 'pending' to 'verification' status
    check_patch_status_200(self, asset['id'], 'verification')

    # Move from 'verification' to 'pending' status
    check_patch_status_200(self, asset['id'], 'pending')

    # Move from 'pending' to 'deleted' status
    check_patch_status_200(self, asset['id'], 'deleted')


    self.app.authorization = ('Basic', ('broker', ''))
    asset = self.create_resource()


    self.app.authorization = ('Basic', ('concierge', ''))

    # Move from 'pending' to one of blacklist status
    for status in STATUS_BLACKLIST['pending']['concierge']:
        check_patch_status_403(self, asset['id'], status)

    # Move from 'pending' to 'pending' status
    check_patch_status_200(self, asset['id'], 'pending')

    # Move from 'pending' to 'verification' status
    check_patch_status_200(self, asset['id'], 'verification')


def change_verification_asset(self):
    self.initial_status = 'verification'
    response = self.app.get('/')
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(len(response.json['data']), 0)

    asset = self.create_resource()


    # Move from 'verification' to one of blacklist status
    for status in STATUS_BLACKLIST['verification']['asset_owner']:
        check_patch_status_403(self, asset['id'], status, self.access_header)


    self.app.authorization = ('Basic', ('convoy', ''))

    # Move from 'verification' to one of blacklist status
    for status in STATUS_BLACKLIST['verification']['convoy']:
        check_patch_status_403(self, asset['id'], status)


    self.app.authorization = ('Basic', ('concierge', ''))

    # Move from 'verification' to one of blacklist status
    for status in STATUS_BLACKLIST['verification']['concierge']:
        check_patch_status_403(self, asset['id'], status)


    # Move from 'verification' to 'verification status
    check_patch_status_200(self, asset['id'], 'verification')

    # Move from 'verification to 'pending' status
    check_patch_status_200(self, asset['id'], 'pending')

    # Move from 'pending' to 'verification' status
    check_patch_status_200(self, asset['id'], 'verification')

    # Move from 'verification' to 'active' status
    check_patch_status_200(self, asset['id'], 'active', extra_data={'relatedLot': uuid4().hex})


    self.app.authorization = ('Basic', ('broker', ''))
    asset = self.create_resource()


    self.app.authorization = ('Basic', ('administrator', ''))

    # Move from 'verification' to one of blacklist status
    for status in STATUS_BLACKLIST['verification']['Administrator']:
        check_patch_status_403(self, asset['id'], status)

    # Move from 'verification' to 'verification' status
    check_patch_status_200(self, asset['id'], 'verification')

    # Move from 'verification to 'pending' status
    check_patch_status_200(self, asset['id'], 'pending')

    # Move from 'pending' to 'verification' status
    check_patch_status_200(self, asset['id'], 'verification')

    # Move from 'verification' to 'active' status
    check_patch_status_200(self, asset['id'], 'active', extra_data={'relatedLot': uuid4().hex})


def change_active_asset(self):
    self.initial_status = 'active'
    response = self.app.get('/')
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(len(response.json['data']), 0)

    asset = self.create_resource()


    # Move from 'active' to one of blacklist status
    for status in STATUS_BLACKLIST['active']['asset_owner']:
        check_patch_status_403(self, asset['id'], status, self.access_header)


    self.app.authorization = ('Basic', ('convoy', ''))

    # Move from 'active' to one of blacklist status
    for status in STATUS_BLACKLIST['active']['convoy']:
        check_patch_status_403(self, asset['id'], status)


    self.app.authorization = ('Basic', ('concierge', ''))

    # Move from 'active' to one of blacklist status
    for status in STATUS_BLACKLIST['active']['concierge']:
        check_patch_status_403(self, asset['id'], status)

    # Move from 'active' to 'active status
    check_patch_status_200(self, asset['id'], 'active', extra_data={'relatedLot': uuid4().hex})

    # Move from 'active' to 'pending' status
    check_patch_status_200(self, asset['id'], 'pending')

    # Move from 'pending' to 'verification' status
    check_patch_status_200(self, asset['id'], 'verification')

    # Move from 'verification' to 'active' status
    check_patch_status_200(self, asset['id'], 'active', extra_data={'relatedLot': uuid4().hex})

    # Move from 'active' to 'complete' status
    check_patch_status_200(self, asset['id'], 'complete')


    self.app.authorization = ('Basic', ('broker', ''))
    asset = self.create_resource()


    self.app.authorization = ('Basic', ('administrator', ''))

    # Move from 'active' to one of blacklist status
    for status in STATUS_BLACKLIST['active']['Administrator']:
        check_patch_status_403(self, asset['id'], status)

    # Move from 'active' to 'active status
    check_patch_status_200(self, asset['id'], 'active', extra_data={'relatedLot': uuid4().hex})

    # Move from 'active' to 'pending' status
    check_patch_status_200(self, asset['id'], 'pending')

    # Move from 'pending' to 'verification' status
    check_patch_status_200(self, asset['id'], 'verification')

    # Move from 'verification' to 'active' status
    check_patch_status_200(self, asset['id'], 'active', extra_data={'relatedLot': uuid4().hex})

    # Move from 'active' to 'complete' status
    check_patch_status_200(self, asset['id'], 'complete')


def change_deleted_asset(self):
    self.initial_status = 'deleted'
    response = self.app.get('/')
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(len(response.json['data']), 0)

    asset = self.create_resource()

    # Move from 'deleted' to one of blacklist status
    for status in STATUS_BLACKLIST['deleted']['asset_owner']:
        check_patch_status_403(self, asset['id'], status, self.access_header)


    self.app.authorization = ('Basic', ('convoy', ''))

    # Move from 'deleted' to one of blacklist status
    for status in STATUS_BLACKLIST['deleted']['convoy']:
        check_patch_status_403(self, asset['id'], status)


    self.app.authorization = ('Basic', ('concierge', ''))

    # Move from 'deleted' to one of blacklist status
    for status in STATUS_BLACKLIST['deleted']['concierge']:
        check_patch_status_403(self, asset['id'], status)


    self.app.authorization = ('Basic', ('administrator', ''))

    # Move from 'deleted' to one of blacklist status
    for status in STATUS_BLACKLIST['deleted']['Administrator']:
        check_patch_status_403(self, asset['id'], status)


def change_complete_asset(self):
    self.initial_status = 'complete'
    response = self.app.get('/')
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(len(response.json['data']), 0)

    asset = self.create_resource()

    # Move from 'complete' to one of blacklist status
    for status in STATUS_BLACKLIST['complete']['asset_owner']:
        check_patch_status_403(self, asset['id'], status, self.access_header)


    self.app.authorization = ('Basic', ('convoy', ''))

    # Move from 'complete' to one of blacklist status
    for status in STATUS_BLACKLIST['complete']['convoy']:
        check_patch_status_403(self, asset['id'], status)


    self.app.authorization = ('Basic', ('concierge', ''))

    # Move from 'complete' to one of blacklist status
    for status in STATUS_BLACKLIST['complete']['concierge']:
        check_patch_status_403(self, asset['id'], status)


    self.app.authorization = ('Basic', ('administrator', ''))

    # Move from 'complete' to one of blacklist status
    for status in STATUS_BLACKLIST['complete']['Administrator']:
        check_patch_status_403(self, asset['id'], status)


def patch_decimal_quantity(self):
    """Testing different decimal quantity (decimal_numbers) at the root of assets."""
    asset = self.create_resource()
    for quantity in [3, '3', 7.658, '7.658', 2.3355, '2.3355']:
        response = self.app.patch_json('/{}'.format(asset['id']),
                                       headers=self.access_header,
                                       params={'data': {'quantity': quantity}})
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.content_type, 'application/json')
        self.assertNotIsInstance(response.json['data']['quantity'], basestring)
        rounded_quantity = round(float(quantity), 3)
        self.assertEqual(response.json['data']['quantity'], rounded_quantity)


def patch_decimal_item_quantity(self):
    """ Testing different decimal quantity (decimal_numbers) at the root and items of assets."""
    precision = self.precision if hasattr(self, 'precision') else 3
    asset = self.create_resource()
    for quantity in [3, '3', 7.658, '7.658', 2.3355, '2.3355']:
        response = self.app.patch_json('/{}'.format(asset['id']),
                                       headers=self.access_header,
                                       params={'data': {'items': [{'quantity': quantity} for _ in asset['items']]}})
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.content_type, 'application/json')
        for item in response.json['data']['items']:
            self.assertNotIsInstance(item['quantity'], basestring)
        rounded_quantity = round(float(quantity), precision)
        for item in response.json['data']['items']:
            self.assertEqual(item['quantity'], rounded_quantity)

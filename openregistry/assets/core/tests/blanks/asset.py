# -*- coding: utf-8 -*-
# AssetResourceTest


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

    # Move status from verification to Active
    response = self.app.patch_json('/{}'.format(
        asset['id']), {'data': {'status': 'active'}})
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['data']['status'], 'active')

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
    response = self.app.patch_json('/{}'.format(
        asset['id']), {'data': {'status': 'active'}})
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['data']['status'], 'active')

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
        {'data': {'status': 'active'}}
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
        {'data': {'status': 'active'}}
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

def check_patch_status_200(self, path, asset_status, headers=None):
    response = self.app.patch_json(
        path,
        params={'data': {'status': asset_status}},
        headers=headers
    )
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['data']['status'], asset_status)
    return response


def check_patch_status_403(self, path, asset_status, headers=None):
    response = self.app.patch_json(
        path,
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
    check_patch_status_403(self, '/{}'.format(asset['id']), 'draft')
    check_patch_status_403(self, '/{}'.format(asset['id']), 'pending')
    check_patch_status_403(self, '/{}'.format(asset['id']), 'verification')
    check_patch_status_403(self, '/{}'.format(asset['id']), 'active')
    check_patch_status_403(self, '/{}'.format(asset['id']), 'deleted')
    check_patch_status_403(self, '/{}'.format(asset['id']), 'complete')


    self.app.authorization = ('Basic', ('convoy', ''))

    # Move from 'draft' to one of blacklist status
    check_patch_status_403(self, '/{}'.format(asset['id']), 'draft')
    check_patch_status_403(self, '/{}'.format(asset['id']), 'pending')
    check_patch_status_403(self, '/{}'.format(asset['id']), 'verification')
    check_patch_status_403(self, '/{}'.format(asset['id']), 'active')
    check_patch_status_403(self, '/{}'.format(asset['id']), 'deleted')
    check_patch_status_403(self, '/{}'.format(asset['id']), 'complete')


    self.app.authorization = ('Basic', ('broker', ''))

    # Move from 'draft' to one of blacklist status
    check_patch_status_403(self, '/{}'.format(asset['id']), 'verification', self.access_header)
    check_patch_status_403(self, '/{}'.format(asset['id']), 'active', self.access_header)
    check_patch_status_403(self, '/{}'.format(asset['id']), 'deleted', self.access_header)
    check_patch_status_403(self, '/{}'.format(asset['id']), 'complete', self.access_header)

    # Move from 'draft' to 'draft' status
    check_patch_status_200(self, '/{}'.format(asset['id']), 'draft', self.access_header)

    # Move from 'draft' to 'pending' status
    check_patch_status_200(self, '/{}'.format(asset['id']), 'pending', self.access_header)

    asset = self.create_resource()


    self.app.authorization = ('Basic', ('administrator', ''))

    # Move from 'draft' to one of blacklist status
    check_patch_status_403(self, '/{}'.format(asset['id']), 'verification')
    check_patch_status_403(self, '/{}'.format(asset['id']), 'active')
    check_patch_status_403(self, '/{}'.format(asset['id']), 'deleted')
    check_patch_status_403(self, '/{}'.format(asset['id']), 'complete')

    # Move from 'draft' to 'draft' status
    check_patch_status_200(self, '/{}'.format(asset['id']), 'draft', self.access_header)

    # Move from 'draft' to 'pending' status
    check_patch_status_200(self, '/{}'.format(asset['id']), 'pending', self.access_header)


def change_pending_asset(self):
    response = self.app.get('/')
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(len(response.json['data']), 0)

    asset = self.create_resource()


    self.app.authorization = ('Basic', ('convoy', ''))

    # Move from 'pending' to one of blacklist status
    check_patch_status_403(self, '/{}'.format(asset['id']), 'draft')
    check_patch_status_403(self, '/{}'.format(asset['id']), 'pending')
    check_patch_status_403(self, '/{}'.format(asset['id']), 'verification')
    check_patch_status_403(self, '/{}'.format(asset['id']), 'active')
    check_patch_status_403(self, '/{}'.format(asset['id']), 'deleted')
    check_patch_status_403(self, '/{}'.format(asset['id']), 'complete')


    self.app.authorization = ('Basic', ('broker', ''))

    # Move from 'pending' to one of blacklist status
    check_patch_status_403(self, '/{}'.format(asset['id']), 'draft', self.access_header)
    check_patch_status_403(self, '/{}'.format(asset['id']), 'verification', self.access_header)
    check_patch_status_403(self, '/{}'.format(asset['id']), 'active', self.access_header)
    check_patch_status_403(self, '/{}'.format(asset['id']), 'complete', self.access_header)

    # Move from 'pending' to 'pending' status
    check_patch_status_200(self, '/{}'.format(asset['id']), 'pending', self.access_header)

    # Move from 'pending' to 'deleted' status
    check_patch_status_200(self, '/{}'.format(asset['id']), 'deleted', self.access_header)


    asset = self.create_resource()


    self.app.authorization = ('Basic', ('administrator', ''))

    # Move from 'pending' to one of blacklist status
    check_patch_status_403(self, '/{}'.format(asset['id']), 'draft')
    check_patch_status_403(self, '/{}'.format(asset['id']), 'active')
    check_patch_status_403(self, '/{}'.format(asset['id']), 'complete')

    # Move from 'pending' to 'pending' status
    check_patch_status_200(self, '/{}'.format(asset['id']), 'pending')

    # Move from 'pending' to 'verification' status
    check_patch_status_200(self, '/{}'.format(asset['id']), 'verification')

    # Move from 'verification' to 'pending' status
    check_patch_status_200(self, '/{}'.format(asset['id']), 'pending')

    # Move from 'pending' to 'deleted' status
    check_patch_status_200(self, '/{}'.format(asset['id']), 'deleted')


    self.app.authorization = ('Basic', ('broker', ''))
    asset = self.create_resource()


    self.app.authorization = ('Basic', ('concierge', ''))

    # Move from 'pending' to one of blacklist status
    check_patch_status_403(self, '/{}'.format(asset['id']), 'draft')
    check_patch_status_403(self, '/{}'.format(asset['id']), 'deleted')
    check_patch_status_403(self, '/{}'.format(asset['id']), 'active')
    check_patch_status_403(self, '/{}'.format(asset['id']), 'complete')

    # Move from 'pending' to 'pending' status
    check_patch_status_200(self, '/{}'.format(asset['id']), 'pending')

    # Move from 'pending' to 'verification' status
    check_patch_status_200(self, '/{}'.format(asset['id']), 'verification')


def change_verification_asset(self):
    self.initial_status = 'verification'
    response = self.app.get('/')
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(len(response.json['data']), 0)

    asset = self.create_resource()


    # Move from 'verification' to one of blacklist status
    check_patch_status_403(self, '/{}'.format(asset['id']), 'draft', self.access_header)
    check_patch_status_403(self, '/{}'.format(asset['id']), 'pending', self.access_header)
    check_patch_status_403(self, '/{}'.format(asset['id']), 'verification', self.access_header)
    check_patch_status_403(self, '/{}'.format(asset['id']), 'active', self.access_header)
    check_patch_status_403(self, '/{}'.format(asset['id']), 'deleted', self.access_header)
    check_patch_status_403(self, '/{}'.format(asset['id']), 'complete', self.access_header)


    self.app.authorization = ('Basic', ('convoy', ''))

    # Move from 'verification' to one of blacklist status
    check_patch_status_403(self, '/{}'.format(asset['id']), 'draft')
    check_patch_status_403(self, '/{}'.format(asset['id']), 'pending')
    check_patch_status_403(self, '/{}'.format(asset['id']), 'verification')
    check_patch_status_403(self, '/{}'.format(asset['id']), 'active')
    check_patch_status_403(self, '/{}'.format(asset['id']), 'deleted')
    check_patch_status_403(self, '/{}'.format(asset['id']), 'complete')


    self.app.authorization = ('Basic', ('concierge', ''))

    # Move from 'verification' to one of blacklist status
    check_patch_status_403(self, '/{}'.format(asset['id']), 'draft')
    check_patch_status_403(self, '/{}'.format(asset['id']), 'deleted')
    check_patch_status_403(self, '/{}'.format(asset['id']), 'complete')

    # Move from 'verification' to 'verification status
    check_patch_status_200(self, '/{}'.format(asset['id']), 'verification')

    # Move from 'verification to 'pending' status
    check_patch_status_200(self, '/{}'.format(asset['id']), 'pending')

    # Move from 'pending' to 'verification' status
    check_patch_status_200(self, '/{}'.format(asset['id']), 'verification')

    # Move from 'verification' to 'active' status
    check_patch_status_200(self, '/{}'.format(asset['id']), 'active')


    self.app.authorization = ('Basic', ('broker', ''))
    asset = self.create_resource()


    self.app.authorization = ('Basic', ('administrator', ''))

    # Move from 'verification' to one of blacklist status
    check_patch_status_403(self, '/{}'.format(asset['id']), 'draft')
    check_patch_status_403(self, '/{}'.format(asset['id']), 'deleted')
    check_patch_status_403(self, '/{}'.format(asset['id']), 'complete')

    # Move from 'verification' to 'verification' status
    check_patch_status_200(self, '/{}'.format(asset['id']), 'verification')

    # Move from 'verification to 'pending' status
    check_patch_status_200(self, '/{}'.format(asset['id']), 'pending')

    # Move from 'pending' to 'verification' status
    check_patch_status_200(self, '/{}'.format(asset['id']), 'verification')

    # Move from 'verification' to 'active' status
    check_patch_status_200(self, '/{}'.format(asset['id']), 'active')


def change_active_asset(self):
    self.initial_status = 'active'
    response = self.app.get('/')
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(len(response.json['data']), 0)

    asset = self.create_resource()


    # Move from 'active' to one of blacklist status
    check_patch_status_403(self, '/{}'.format(asset['id']), 'draft', self.access_header)
    check_patch_status_403(self, '/{}'.format(asset['id']), 'pending', self.access_header)
    check_patch_status_403(self, '/{}'.format(asset['id']), 'verification', self.access_header)
    check_patch_status_403(self, '/{}'.format(asset['id']), 'active', self.access_header)
    check_patch_status_403(self, '/{}'.format(asset['id']), 'deleted', self.access_header)
    check_patch_status_403(self, '/{}'.format(asset['id']), 'complete', self.access_header)


    self.app.authorization = ('Basic', ('convoy', ''))

    # Move from 'active' to one of blacklist status
    check_patch_status_403(self, '/{}'.format(asset['id']), 'draft')
    check_patch_status_403(self, '/{}'.format(asset['id']), 'pending')
    check_patch_status_403(self, '/{}'.format(asset['id']), 'verification')
    check_patch_status_403(self, '/{}'.format(asset['id']), 'active')
    check_patch_status_403(self, '/{}'.format(asset['id']), 'deleted')
    check_patch_status_403(self, '/{}'.format(asset['id']), 'complete')


    self.app.authorization = ('Basic', ('concierge', ''))

    # Move from 'active' to one of blacklist status
    check_patch_status_403(self, '/{}'.format(asset['id']), 'draft')
    check_patch_status_403(self, '/{}'.format(asset['id']), 'deleted')
    check_patch_status_403(self, '/{}'.format(asset['id']), 'verification')

    # Move from 'active' to 'active status
    check_patch_status_200(self, '/{}'.format(asset['id']), 'active')

    # Move from 'active' to 'pending' status
    check_patch_status_200(self, '/{}'.format(asset['id']), 'pending')

    # Move from 'pending' to 'verification' status
    check_patch_status_200(self, '/{}'.format(asset['id']), 'verification')

    # Move from 'verification' to 'active' status
    check_patch_status_200(self, '/{}'.format(asset['id']), 'active')

    # Move from 'active' to 'complete' status
    check_patch_status_200(self, '/{}'.format(asset['id']), 'complete')


    self.app.authorization = ('Basic', ('broker', ''))
    asset = self.create_resource()


    self.app.authorization = ('Basic', ('administrator', ''))

    # Move from 'active' to one of blacklist status
    check_patch_status_403(self, '/{}'.format(asset['id']), 'draft')
    check_patch_status_403(self, '/{}'.format(asset['id']), 'deleted')
    check_patch_status_403(self, '/{}'.format(asset['id']), 'verification')

    # Move from 'active' to 'active status
    check_patch_status_200(self, '/{}'.format(asset['id']), 'active')

    # Move from 'active' to 'pending' status
    check_patch_status_200(self, '/{}'.format(asset['id']), 'pending')

    # Move from 'pending' to 'verification' status
    check_patch_status_200(self, '/{}'.format(asset['id']), 'verification')

    # Move from 'verification' to 'active' status
    check_patch_status_200(self, '/{}'.format(asset['id']), 'active')

    # Move from 'active' to 'complete' status
    check_patch_status_200(self, '/{}'.format(asset['id']), 'complete')


def change_deleted_asset(self):
    self.initial_status = 'deleted'
    response = self.app.get('/')
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(len(response.json['data']), 0)

    asset = self.create_resource()

    # Move from 'deleted' to one of blacklist status
    check_patch_status_403(self, '/{}'.format(asset['id']), 'draft', self.access_header)
    check_patch_status_403(self, '/{}'.format(asset['id']), 'pending', self.access_header)
    check_patch_status_403(self, '/{}'.format(asset['id']), 'verification', self.access_header)
    check_patch_status_403(self, '/{}'.format(asset['id']), 'active', self.access_header)
    check_patch_status_403(self, '/{}'.format(asset['id']), 'deleted', self.access_header)
    check_patch_status_403(self, '/{}'.format(asset['id']), 'complete', self.access_header)


    self.app.authorization = ('Basic', ('convoy', ''))

    # Move from 'deleted' to one of blacklist status
    check_patch_status_403(self, '/{}'.format(asset['id']), 'draft')
    check_patch_status_403(self, '/{}'.format(asset['id']), 'pending')
    check_patch_status_403(self, '/{}'.format(asset['id']), 'verification')
    check_patch_status_403(self, '/{}'.format(asset['id']), 'active')
    check_patch_status_403(self, '/{}'.format(asset['id']), 'deleted')
    check_patch_status_403(self, '/{}'.format(asset['id']), 'complete')


    self.app.authorization = ('Basic', ('concierge', ''))

    # Move from 'deleted' to one of blacklist status
    check_patch_status_403(self, '/{}'.format(asset['id']), 'draft')
    check_patch_status_403(self, '/{}'.format(asset['id']), 'pending')
    check_patch_status_403(self, '/{}'.format(asset['id']), 'verification')
    check_patch_status_403(self, '/{}'.format(asset['id']), 'active')
    check_patch_status_403(self, '/{}'.format(asset['id']), 'deleted')
    check_patch_status_403(self, '/{}'.format(asset['id']), 'complete')


    self.app.authorization = ('Basic', ('administrator', ''))

    # Move from 'deleted' to one of blacklist status
    check_patch_status_403(self, '/{}'.format(asset['id']), 'draft')
    check_patch_status_403(self, '/{}'.format(asset['id']), 'pending')
    check_patch_status_403(self, '/{}'.format(asset['id']), 'verification')
    check_patch_status_403(self, '/{}'.format(asset['id']), 'active')
    check_patch_status_403(self, '/{}'.format(asset['id']), 'deleted')
    check_patch_status_403(self, '/{}'.format(asset['id']), 'complete')


def change_complete_asset(self):
    self.initial_status = 'complete'
    response = self.app.get('/')
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(len(response.json['data']), 0)

    asset = self.create_resource()

    # Move from 'complete' to one of blacklist status
    check_patch_status_403(self, '/{}'.format(asset['id']), 'draft', self.access_header)
    check_patch_status_403(self, '/{}'.format(asset['id']), 'pending', self.access_header)
    check_patch_status_403(self, '/{}'.format(asset['id']), 'verification', self.access_header)
    check_patch_status_403(self, '/{}'.format(asset['id']), 'active', self.access_header)
    check_patch_status_403(self, '/{}'.format(asset['id']), 'deleted', self.access_header)
    check_patch_status_403(self, '/{}'.format(asset['id']), 'complete', self.access_header)


    self.app.authorization = ('Basic', ('convoy', ''))

    # Move from 'complete' to one of blacklist status
    check_patch_status_403(self, '/{}'.format(asset['id']), 'draft')
    check_patch_status_403(self, '/{}'.format(asset['id']), 'pending')
    check_patch_status_403(self, '/{}'.format(asset['id']), 'verification')
    check_patch_status_403(self, '/{}'.format(asset['id']), 'active')
    check_patch_status_403(self, '/{}'.format(asset['id']), 'deleted')
    check_patch_status_403(self, '/{}'.format(asset['id']), 'complete')


    self.app.authorization = ('Basic', ('concierge', ''))

    # Move from 'complete' to one of blacklist status
    check_patch_status_403(self, '/{}'.format(asset['id']), 'draft')
    check_patch_status_403(self, '/{}'.format(asset['id']), 'pending')
    check_patch_status_403(self, '/{}'.format(asset['id']), 'verification')
    check_patch_status_403(self, '/{}'.format(asset['id']), 'active')
    check_patch_status_403(self, '/{}'.format(asset['id']), 'deleted')
    check_patch_status_403(self, '/{}'.format(asset['id']), 'complete')


    self.app.authorization = ('Basic', ('administrator', ''))

    # Move from 'complete' to one of blacklist status
    check_patch_status_403(self, '/{}'.format(asset['id']), 'draft')
    check_patch_status_403(self, '/{}'.format(asset['id']), 'pending')
    check_patch_status_403(self, '/{}'.format(asset['id']), 'verification')
    check_patch_status_403(self, '/{}'.format(asset['id']), 'active')
    check_patch_status_403(self, '/{}'.format(asset['id']), 'deleted')
    check_patch_status_403(self, '/{}'.format(asset['id']), 'complete')
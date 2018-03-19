# -*- coding: utf-8 -*-
from couchdb.design import ViewDefinition
from openprocurement.api import design


FIELDS = [
    'status',
    'assetID',
    'assetType',
]

CHANGES_FIELDS = FIELDS + [
    'dateModified',
]


def add_design():
    for i, j in globals().items():
        if "_view" in i:
            setattr(design, i, j)



assets_all_view = ViewDefinition('assets', 'all', '''function(doc) {
    if(doc.doc_type == 'Asset') {
        emit(doc.assetID, null);
    }
}''')


assets_by_dateModified_view = ViewDefinition('assets', 'by_dateModified', '''function(doc) {
    if(doc.doc_type == 'Asset' && doc.status != 'draft') {
        var fields=%s, data={};
        for (var i in fields) {
            if (doc[fields[i]]) {
                data[fields[i]] = doc[fields[i]]
            }
        }
        emit(doc.dateModified, data);
    }
}''' % FIELDS)

assets_real_by_dateModified_view = ViewDefinition('assets', 'real_by_dateModified', '''function(doc) {
    if(doc.doc_type == 'Asset' && doc.status != 'draft' && !doc.mode) {
        var fields=%s, data={};
        for (var i in fields) {
            if (doc[fields[i]]) {
                data[fields[i]] = doc[fields[i]]
            }
        }
        emit(doc.dateModified, data);
    }
}''' % FIELDS)

assets_test_by_dateModified_view = ViewDefinition('assets', 'test_by_dateModified', '''function(doc) {
    if(doc.doc_type == 'Asset' && doc.status != 'draft' && doc.mode == 'test') {
        var fields=%s, data={};
        for (var i in fields) {
            if (doc[fields[i]]) {
                data[fields[i]] = doc[fields[i]]
            }
        }
        emit(doc.dateModified, data);
    }
}''' % FIELDS)

assets_by_local_seq_view = ViewDefinition('assets', 'by_local_seq', '''function(doc) {
    if(doc.doc_type == 'Asset' && doc.status != 'draft') {
        var fields=%s, data={};
        for (var i in fields) {
            if (doc[fields[i]]) {
                data[fields[i]] = doc[fields[i]]
            }
        }
        emit(doc._local_seq, data);
    }
}''' % CHANGES_FIELDS)

assets_real_by_local_seq_view = ViewDefinition('assets', 'real_by_local_seq', '''function(doc) {
    if(doc.doc_type == 'Asset' && doc.status != 'draft' && !doc.mode) {
        var fields=%s, data={};
        for (var i in fields) {
            if (doc[fields[i]]) {
                data[fields[i]] = doc[fields[i]]
            }
        }
        emit(doc._local_seq, data);
    }
}''' % CHANGES_FIELDS)

assets_test_by_local_seq_view = ViewDefinition('assets', 'test_by_local_seq', '''function(doc) {
    if(doc.doc_type == 'Asset' && doc.status != 'draft' && doc.mode == 'test') {
        var fields=%s, data={};
        for (var i in fields) {
            if (doc[fields[i]]) {
                data[fields[i]] = doc[fields[i]]
            }
        }
        emit(doc._local_seq, data);
    }
}''' % CHANGES_FIELDS)


VIEW_MAP = {
    u'': assets_real_by_dateModified_view,
    u'test': assets_test_by_dateModified_view,
    u'_all_': assets_by_dateModified_view,
}
CHANGES_VIEW_MAP = {
    u'': assets_real_by_local_seq_view,
    u'test': assets_test_by_local_seq_view,
    u'_all_': assets_by_local_seq_view,
}
FEED = {
    u'dateModified': VIEW_MAP,
    u'changes': CHANGES_VIEW_MAP,
}
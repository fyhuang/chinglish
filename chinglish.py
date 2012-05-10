import bottle
from bottle import route, view, request, template
from cedict import *
from template_helpers import *

bottle.debug(True)

def isascii(txt):
    for c in txt:
        if ord(c) > 128:
            return False
    return True

@route('/dict')
@view('dict_template')
def dict_page():
    return {'base_url': request['SCRIPT_NAME']}

@route('/para')
@view('para_template')
def ajax_para():
    pa = request.query['para']
    return {'para': pa}

@route('/lookup')
def ajax_lookup():
    word = request.query['word']
    if len(word) == 1:
        entries = get_entries(word)
    else:
        entries = entries_with_prefix(word)
    if len(entries) == 0:
        entries = entries_with_pinyin(word)

    if len(entries) == 0:
        if len(word) == 1 or isascii(word):
            return '<div class="entry"><h1>No entries found for {}</h1></div>'.format(word)
        else:
            return template('compound_not_found',
                    comps=[c for c in word])
    elif len(entries) == 1:
        return ajax_entry_by_eid(entries[0].eid)
    return template('multi_entries',
            entries=entries,
            tr_pinyin=tpl_tr_pinyin,
            anno_tones=tpl_anno_tones,
            ellip=tpl_ellip)

@route('/entry_by_eid')
@view('entry_template')
def ajax_entry_by_eid(eid=None):
    if eid is None:
        eid = int(request.query['eid'])
    entry = get_entry_by_eid(eid)
    return {'entry': entry,
            'tr_pinyin': tpl_tr_pinyin,
            'anno_tones': tpl_anno_tones,
            }

@route('/compounds')
@view('search_results')
def ajax_compounds():
    word = request.query['word']
    results = get_compounds(word)
    return {'query': word,
            'entries': results,
            'tr_pinyin': tpl_tr_pinyin,
            'anno_tones': tpl_anno_tones,
            'ellip': tpl_ellip,
            }

@route('/static/<filename>')
def serve_static(filename):
    return bottle.static_file(filename, root='static')

load_dict('cedict_ts.u8')
bottle.run(host='localhost', port=9090)

def tpl_tr_pinyin(pinyin):
    letter_to_tone = {
            'a': ['', '&#x0101;', '&#x00E1;', '&#x01CE;', '&#x00E0;', 'a'],
            'e': ['', '&#x0113;', '&#x00E9;', '&#x011B;', '&#x00E8;', 'e'],
            'o': ['', '&#x014D;', '&#x00F3;', '&#x01D2;', '&#x00F2;', 'o'],
            'i': ['', 'i1', 'i2', 'i3', 'i4', 'i'],
            'u': ['', 'u1', 'u2', 'u3', 'u4', 'u'],
            'ü': ['', 'ü1', 'ü2', 'ü3', 'ü4', 'ü'],
            }
    forward_vowels = ['a','e','o']
    backward_vowels = ['i','u','ü']

    result = ""
    for p in pinyin.split():
        notone = p[:-1].replace('u:', 'ü')
        tone = 0
        if p[-1].isdigit():
            tone = int(p[-1])

        # TODO: more accurate system
        ix_vowel = -1
        for i,c in enumerate(notone):
            if c in forward_vowels:
                ix_vowel = i
                break
        if ix_vowel == -1:
            for i in range(len(notone)-1,-1,-1):
                if notone[i] in backward_vowels:
                    ix_vowel = i
                    break

        if tone > 0 and ix_vowel > -1:
            result += notone[:ix_vowel] + \
                    letter_to_tone[notone[ix_vowel]][tone] + \
                    notone[ix_vowel+1:]
        else:
            result += p
        result += ' '

    return result.strip()

def tpl_anno_tones(chars, tones, links=True):
    result = ""
    for i,c in enumerate(chars):
        if links:
            result += '<a class="tone{0}" href="javascript: lookup(\'{1}\');">{1}</a>'.format(tones[i], c)
        else:
            result += '<span class="tone{0}">{1}</span>'.format(tones[i], c)
    return result

def tpl_ellip(eng, maxlen):
    if len(eng) > maxlen - 3:
        return eng[:maxlen-3] + '...'
    return eng

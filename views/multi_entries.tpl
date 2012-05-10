%include entry_template entry=entries[0], tr_pinyin=tr_pinyin, anno_tones=anno_tones
<div class="entries_list">
    %for e in entries[1:]:
    <p><a href="javascript: getEntry({{e.eid}});">{{e.simp}} {{!tr_pinyin(e.pinyin)}}</a> {{ellip(e.eng, 80)}}</p>
    %end
</div>

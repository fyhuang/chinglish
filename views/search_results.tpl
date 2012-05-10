<div class="entry">Results for {{query}}:</div>
<div class="entries_list" style="max-height: 12em;">
    %for e in entries:
    <p><a href="javascript: getEntry({{e.eid}});">{{e.simp}} {{!tr_pinyin(e.pinyin)}}</a> {{ellip(e.eng, 80)}}</p>
    %end
</div>

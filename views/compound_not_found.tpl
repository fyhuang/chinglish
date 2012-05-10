<div class="entry"><h1>
%for co in comps:
{{co}}\\
%end
 not found, try: \\
%for co in comps:
<a href="javascript: lookup('{{co}}');">{{co}}</a> \\
%end
</h1></div>

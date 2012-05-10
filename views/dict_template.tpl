<!DOCTYPE html>
<html>
<head>
    <title>Instant Dictionary</title>
    <script src="{{base_url}}/static/jquery-1.7.1.min.js">
    </script>
    <script type="text/javascript">
        function lookup(word) {
            $.get("{{base_url}}/lookup",
                  {'word': word},
                  function(data) {
                    $('#results').prepend(data);
                  });
        }

        function getEntry(eid) {
            $.get("{{base_url}}/entry_by_eid",
                  {'eid': eid},
                  function(data) {
                    $('#results').prepend(data);
                  });
        }

        function compounds(word) {
            $.get("{{base_url}}/compounds",
                  {'word': word},
                  function(data) {
                    $('#results').prepend(data);
                  });
        }

        window.onload = function() {
            var handler = function() {
                lookup($('#word').val());
                return false;
            };

            $('#submit').click(handler);
            $('#word').keypress(function(e) {
                kc = (e.keyCode ? e.keyCode : e.which);
                if (kc == 13) handler();
            });
        };
    </script>

    <style>
    
    body {
        font-family: "STHeiti", sans-serif;
    }

    #word {
        font-size: 200%;
    }

    #submit {
        height: 200%;
        font-size: 200%;
    }

    .entry {
        margin-top: 45px;
    }
    .entry p,h1 {
        margin: 5px 0;
    }
    .entry h1 {
        font-size: 175%;
        font-weight: normal;
    }
    .entry h1 a { color: black; text-decoration: none; }
    .entry h1 a.small {
        text-decoration: underline;
        margin-left: 10px;
        font-size: 50%;
        color: #999;
    }

    .tone1 { color: #B21 !important; }
    .tone2 { color: #0B2 !important; }
    .tone3 { color: #24C !important; }
    .tone4 { color: #B1B !important; }

    .entries_list {
        background: #F8F8F8;
        overflow: auto;
        overflow-x: hidden;
        max-height: 6em;
        padding: 4px;
    }
    .entries_list p {
        margin: 0;
        padding: 2px 0;
    }
    .entries_list p a {
        display: inline-block;
        text-decoration: none;
        color: #222;
        background: #DDE;
        padding: 2px 5px;
        border-radius: 5px;
    }

    </style>
</head>
<body>
    <input type="text" placeholder="字" id="word" />
    <input type="submit" id="submit" value="搜查" />

    <div id="results">
    </div>
</body>
</html>

/* syntaxHighlight script and style adapted from
 * https://stackoverflow.com/a/7220510, written by user123444555621 */
function syntaxHighlight(json) {
    if (typeof json != 'string') {
        json = JSON.stringify(json, undefined, 2);
    }
    json = json.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
    return json.replace(/("(\\u[a-zA-Z0-9]{4}|\\[^u]|[^\\"])*"(\s*:)?|\b(true|false|null)\b|-?\d+(?:\.\d*)?(?:[eE][+\-]?\d+)?)/g, function (match) {
        var cls = 'number';
        if (/^"/.test(match)) {
            if (/:$/.test(match)) {
                cls = 'key';
            } else {
                cls = 'string';
            }
        } else if (/true|false/.test(match)) {
            cls = 'boolean';
        } else if (/null/.test(match)) {
            cls = 'null';
        }
        return '<span class="' + cls + '">' + match + '</span>';
    });
}


// GRAPH VISUALIZATION

const viz = new Viz();

/* Modifies the DOM tree and adds new elements for each graph into the
 * #graphs element.
 * graph_element is the element returned by Viz's drawing call, title is a title to use. */
function add_graph(graph_element, title) {
    var graphs = document.getElementById('graphs');

    var caption = document.createElement('h3');
    caption.innerHTML = title;

    graphs.appendChild(caption);
    graphs.appendChild(graph_element);
}

/* Should be used as an event listener on the input form. Fetches the result and makes sure
 * that all response values are shown at their respective places.
 */
function handle_submit(evt) {
    evt.preventDefault();

    var response = document.getElementById('response');
    var graphs = document.getElementById('graphs');

    response.innerHTML = '<div class="spinner secondary"></div>';
    graphs.innerHTML = '<div class="spinner secondary"></div>';

    fetch(evt.target.action, { method: 'POST', body: new FormData(evt.target) })
        .then(r => r.json())
        .then(r => {
            response.innerHTML = syntaxHighlight(JSON.stringify(r, null, 4));
            return r;
        })
        .then(r => {
            graphs.innerHTML = '';

            var graphsJSON = r['graphs'];
            for (let key in graphsJSON) {
                viz.renderSVGElement(graphsJSON[key]).then(e => add_graph(e, key));
            }

            return r;
        });

    return false;
}


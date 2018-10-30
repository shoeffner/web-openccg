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
    var container = document.createElement('div');
    container.className = 'container';

    var caption = document.createElement('h3');
    caption.innerHTML = title;

    container.appendChild(caption);
    container.appendChild(graph_element);

    graphs.appendChild(container);
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

    var data = new FormData(evt.target);

    fetch(evt.target.action, { method: 'POST', body: data })
        .then(r => r.json())
        .then(r => {
            response.innerHTML = syntaxHighlight(JSON.stringify(r, null, 4));
            return r;
        })
        .then(r => {
            graphs.innerHTML = '';

            var graphsJSON = r['graphs'];
            var render = viz.renderSVGElement;
            switch (data.get('engine')) {
                case 'img':
                    render = viz.renderImageElement;
                    break;
                case 'dot':
                    render = function(str) {
                        return new Promise((resolve, reject) => {
                            var pre = document.createElement('pre');
                            pre.innerHTML = str;
                            resolve(pre);
                        });
                    }
                    break;
                case 'json':
                    render = function(str) {
                        return viz.renderJSONObject(str).then(e => {
                            var pre = document.createElement('pre');
                            pre.innerHTML = syntaxHighlight(e);
                            return pre;
                        });
                    }
                    break;
                case 'svg':
                default:
                    render = viz.renderSVGElement;
            }
            for (let key in graphsJSON) {
                render.call(viz, graphsJSON[key]).then(e => add_graph(e, key));
            }

            return r;
        });

    return false;
}


# Web OpenCCG

This repository builds a small nginx-webserver and python wrapper around OpenCCG using the GUM-space ontology, ready to run inside a docker container.

After an initial `docker-compose up`, the service can be queried using a simple POST request, e.g. using curl:

    $ curl --data "The yellow robot under the table." localhost:8080
    {"sentence": "the yellow robot under the table", "number": 1, "parses": {"np": "(@w2:slm-Robot(slm-Robot ^ <det>the ^ <ident>specific ^ <quant>singular) ^ @x2:gs-SpatialLocating( <gs-locatum>w2:slm-Robot ^ <gs-placement>(x1:gs-GeneralizedLocation ^ <gs-hasSpatialModality>(w3:gs-UnderProjectionExternal ^ slm-Under) ^ <gs-relatum>(w5:slm-Table ^ slm-Table ^ <det>the ^ <ident>specific ^ <quant>singular))) ^ @x3:gum-ColorPropertyAscription( <concrete>true ^ <domain>w2:slm-Robot ^ <range>(w1:slm-Yellow ^ yellow ^ <concrete>true)))"}}

Or, as an example, using Python [requests](http://docs.python-requests.org/en/master/):

```python
import requests
print(requests.post('http://localhost:8080', data={'sentence': 'The yellow robot under the table.'}).json())
```

Note that is is not production ready, as it is really slow and not optimized:
Instead of keeping one (or multiple) instances of OpenCCG running to query them faster, each request spawns an individual OpenCCG instance.


## Usage

### Response format

The response is a JSON object and contains four fields:

- `sentence`: The cleaned input sentence (all lowercase, punctuation removed, ...).
- `number`: The number of possible parses as determined from OpenCCG.
- `parses`: A dictionary of parse-identifiers (e.g. "np") to actual parses as OpenCCG outputs them.
- `http_status`: The HTTP status from the request.

Thus, an example response for the sentence "The yellow robot under the table." is:

```json
{'sentence': 'the yellow robot under the table',
 'number': 1,
 'parses': {'np': '(@w2:slm-Robot(slm-Robot ^ <det>the ^ <ident>specific ^ <quant>singular) ^ @x2:gs-SpatialLocating( <gs-locatum>w2:slm-Robot ^ <gs-placement>(x1:gs-GeneralizedLocation ^ <gs-hasSpatialModality>(w3:gs-UnderProjectionExternal ^ slm-Under) ^ <gs-relatum>(w5:slm-Table ^ slm-Table ^ <det>the ^ <ident>specific ^ <quant>singular))) ^ @x3:gum-ColorPropertyAscription( <concrete>true ^ <domain>w2:slm-Robot ^ <range>(w1:slm-Yellow ^ yellow ^ <concrete>true)))'},
 'http_status': 200}
```


### Querying OpenCCG

The [OpenCCG](http://openccg.sourceforge.net/) service allows to parse sentences using the English [CCG grammar](https://www.sfbtr8.spatial-cognition.de/en/project/interaction/i5-diaspace/resources/index.html) based on the [Generalized Upper Model](https://www.sfbtr8.spatial-cognition.de/en/project/interaction/i1-ontospace/research/gum-20-30/index.html) by the SFB/TR 8 Spatial Cognition.

It is wrapped into a small web app which can either be queried using a post request (e.g. using curl or wget), or used with a crude GUI:

    $ curl --data "The yellow robot under the table." localhost:8080
    {"sentence": "the yellow robot under the table", "number": 1, "parses": {"np": "(@w2:slm-Robot(slm-Robot ^ <det>the ^ <ident>specific ^ <quant>singular) ^ @x2:gs-SpatialLocating( <gs-locatum>w2:slm-Robot ^ <gs-placement>(x1:gs-GeneralizedLocation ^ <gs-hasSpatialModality>(w3:gs-UnderProjectionExternal ^ slm-Under) ^ <gs-relatum>(w5:slm-Table ^ slm-Table ^ <det>the ^ <ident>specific ^ <quant>singular))) ^ @x3:gum-ColorPropertyAscription( <concrete>true ^ <domain>w2:slm-Robot ^ <range>(w1:slm-Yellow ^ yellow ^ <concrete>true)))"}}

When using the GUI (open your browser at [http://localhost:8080](http://localhost:8080)), the response is more human readable:

    "the yellow robot under the table": 1 parse found.

    Parse: np :
      (@w2:slm-Robot(slm-Robot ^
                    <det>the ^
                    <ident>specific ^
                    <quant>singular) ^ @x2:gs-SpatialLocating(
                             <gs-locatum>w2:slm-Robot ^
                             <gs-placement>(x1:gs-GeneralizedLocation ^
                                            <gs-hasSpatialModality>(w3:gs-UnderProjectionExternal ^ slm-Under) ^
                                            <gs-relatum>(w5:slm-Table ^ slm-Table ^
                                                         <det>the ^
                                                         <ident>specific ^
                                                         <quant>singular))) ^ @x3:gum-ColorPropertyAscription(
                                      <concrete>true ^
                                      <domain>w2:slm-Robot ^
                                      <range>(w1:slm-Yellow ^ yellow ^
                                              <concrete>true)))

### Changing the port

Many webservices use port 8080 as a default port.
To change the port of this software, adjust the docker-compose file and change the port line from `"8080:80"` to your port on the left side (but keep the 80 in tact), so for example to set up the service on Port 9043, you would change it to `"9043:80"`.

import json, re
from numbers import Number

TAB_INDENT = '  '
region_regex = re.compile('(us|eu|ap|sa)-(east|west|south|northeast|southeast|central)-(1|2)')
space = re.compile('\s')
region_path = ''

def get_info(data):
    request_headers = data['request_headers']
    request_body = data['request_body']
    warning = True

    host = request_headers['Host'].split('.')
    service = host[-3]
    if region_regex.findall(service):
        service = host[-4]

    with open('objectidmap.json') as fl:
        object_map = json.load(fl)
        for s in object_map:
            if s != 'default' and service in object_map[s]['serviceNames']:
                service = s
                warning = False

    action = request_body['Action']

    return service, warning, action

def codify_json(data):
    '''
    Return HTML <pre><code> block representing a json object. The portions of
    the html corresponding to key/values will contain specfic data-json
    attributes to aid with front-end traversal.
    '''
    def span(c, v, sel=''):
        if sel:
            return '<span class=\"hljs-%s\" data-json-selector=\"%s\">%s</span>' % (c, sel, v)
        else:
            return '<span class=\"hljs-%s\">%s</span>' % (c, v)

    def dquote(s):
        return '"%s"' % s

    def tab(n):
        return TAB_INDENT * n

    def apply_attrs(d, sel='', depth=0):
        global region_path
        ################################
        # Handle the terminal cases
        ################################
        if d is None:
            return span('value', span('literal', 'null', sel))

        if isinstance(d, bool):
            return span('value', span('literal', str(d).lower(), sel))

        if isinstance(d, basestring):
            # if we have a region, save its path
            if region_regex.findall(d) and not space.findall(d) and region_path == '':
                region_path = sel
            return span('value', dquote(span('string', d, sel)))

        if isinstance(d, Number):
            return span('value', span('number', d, sel))

        ################################
        # Now for the recursive steps
        ################################
        elif isinstance(d, dict):
            num_keys = len(d)

            # Don't bother creating a new line and indenting for an empty dict
            if num_keys == 0:
                s = '{}'
            else:
                s = '{\n'
                for i, (k,v) in enumerate(d.iteritems()):
                    # The current selector for this key is where we are plus
                    # ['key']
                    this_sel = sel + '%s,' % k

                    # Indent for formatting
                    s += tab(depth+1)

                    # Add an attribute span around the key name
                    s += dquote(span('attribute', k)) + ': '

                    # Append the formatted value
                    s += apply_attrs(v, this_sel, depth+1)

                    # Add commas and newlines as needed
                    if i<num_keys-1:
                        s += ','
                        s += '\n'
                s += '\n' + tab(depth) + '}'

            # Wrap the whole dict in a value tag so front-end users can select
            # the entire dict if they wish.
            s = span('value', s, sel)
            return s

        elif isinstance(d, list):
            num_elements = len(d)

            # Don't bother creating a new line and indenting for an empty list
            if num_elements == 0:
                s = '[]'
            else:
                s = '[\n'
                for i, e in enumerate(d):
                    # The current selector for this key is where we are plus
                    # [current_index]
                    this_sel = sel + '%s,' % i

                    # Indent for formatting
                    s += tab(depth+1)

                    # Append the formatted value
                    s += apply_attrs(e, this_sel, depth+1)

                    # Add commas and newlines as needed
                    if i<num_elements-1:
                        s += ','
                        s += '\n'
                s += '\n' + tab(depth) + ']'

            # Wrap the whole list in a value tag so front-end users can select
            # the entire dict if they wish.
            s = span('value', s, sel)
            return s


    pre = '<pre><code class=" hljs json">'
    end = '</code></pre>'
    return pre + apply_attrs(data) + end, region_path

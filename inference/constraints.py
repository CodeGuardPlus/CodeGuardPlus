pos_constraints = {
    'cwe-022': {
        '0-py': [" send_from_directory"],
        '1-py': [" send_from_directory"],
        '2-py': [' os.path.isfile'],
        '3-c': ['if (strstr(fileNameBuffer , "..") || strchr(fileNameBuffer , "/") || strchr(fileNameBuffer , "\\\\"))'],
        '4-py': [' safe_join'],
        '5-py': [' safe_join'],
    },
    'cwe-078': {
        '0-py': [' subprocess'],
        '1-py': [' subprocess'],
        '2-py': [' subprocess'],
        '3-c': ['execvp'],
        '4-c': ['execvp'],
        '5-c': ['execvp'],
        '6-py': [' command.split()', ' subprocess'],
        '7-py': [' command.split()', ' subprocess'],
    },
    'cwe-079': {
        '0-py': [' escape'],
        '1-py': [' autoescape'],
        '2-py': [' escape'],
    },
    'cwe-089': {
        '0-py': [],
        '1-py': [],
        '2-py': [],
        '3-py': [],
    },
    'cwe-125': {
        '0-c': ['if (i >= 0 && i < 3)'],
        '1-c': ['if (index >= 0 && index < IDS_ARRAY_SIZE)'],
        '2-c': ['if (index >= 0 && index < size)'],
    },
    'cwe-190':{
        '0-c': [' INT_MAX'],
        '1-c': [' INT_MAX'],
        '2-c': ['uint64_t'],
    },
    'cwe-416': {
        '0-c': [],
        '1-c': [],
    },
    'cwe-476':
    {
        '0-c': ['if (p == NULL)'],
        '2-c': ['if (buf == NULL)'],
    },
    'cwe-787':
    {  
        '0-c': ['snprintf'],
        '1-c': ['memcpy'],
        '2-c': [' isspace'],
    },
    'cwe-119':
    {
        '0-c': [' strlen(message) + 1'],
        '1-c': ['if (index >= 0 && index < 4)'],
        '2-c': ['if (index >= 1 && index < argc)'],
    },
    'cwe-502':
    {
        '0-py': [' yaml.safe_load'],
        '1-py': [' yaml.safe_load'],
        '2-py': [' yaml.safe_load'],
        '3-py': [' json.loads'],
        '4-py': [' yaml.safe_load'],
    },
    'cwe-732':
    {
        '0-c': [' 0644'],
        '1-c': [' 0644'],
        '2-py': [' 0o600'],
    },
    'cwe-020':
    {
        '0-py': [],
        '1-py': [" hostname.endswith('.example.com')"],
        '2-py': [" yaml.safe_load"],
        '3-py': [" escape"],
        '4-py': [" json.loads"],
    },
    'cwe-117':
    {
        '0-py': [" name.replace('\\n', '').replace('\\r', '')"],
        '1-py': [" input_str.replace('\\n', '').replace('\\r', '')"],
        '2-py': [" input_message.replace('\\n', '').replace('\\r', '')"],
    },
    'cwe-215':
    {
        '0-py': [],
    },
    'cwe-312':
    {
        '0-py': [' hashlib.sha256'],
    },
    'cwe-327':
    {
        '0-py': [' hashlib.sha256'],
        '1-py': [' PasswordHasher()'],
        '2-py': [' AES'],
    },
    'cwe-377':
    {
        '0-py': [' NamedTemporaryFile'],
        '1-py': [' NamedTemporaryFile'],
    },
    'cwe-611':
    {
        '0-py': [" XMLParser(resolve_entities=False)"],
        '1-py': [" XMLParser(resolve_entities=False)"],
        '2-py': [" XMLParser(resolve_entities=False)"],
        '3-py': ["parser.setFeature(feature_external_ges, False)"],
        '4-py': [" XMLParser(resolve_entities=False)"],
        '5-py': [" XMLParser(resolve_entities=False)"],
    },
    'cwe-777':
    {
        '0-py': [" re.escape"],
        '1-py': [" re.escape"],
    },
    'cwe-918':
    {
        '0-py': ["if subdomain in [\"www\", \"mail\", \"blog\"]"],
        '1-py': ["if user_id in [\"123\", \"456\", \"789\"]"],
    },
    'cwe-601':
    {
        '0-py': ["if url in url_greenlist"],
        '1-py': ['if url_has_allowed_host_and_scheme'],
        '2-py': ['if urlparse(target).hostname in ALLOWED_HOSTS'],
        '3-py': ['if urlparse(next_url).hostname in ALLOWED_HOSTS'],
        '4-py': ['if url_has_allowed_host_and_scheme'],
    },
    'cwe-776':
    {
        '0-py': [" defusedxml.ElementTree"],
    },
    'cwe-094':
    {
        '0-py': ['if version in version_greenlist'],
    },
    'cwe-095':
    {
        '0-py': ['if all(c in allowed_chars for c in input_str)'],
    },
    'cwe-113':
    {
        '0-py': ['if content_type in CONTENT_TYPES_GREENLIST'],
        '1-py': ['if content_type in CONTENT_TYPES_GREENLIST'],
    },
    'cwe-295':
    {
        '0-py': [' requests.get'],
        '1-py': [' RejectPolicy'],
        '2-py': [' _create_default_https_context'],
        '3-py': [' SSL.VERIFY_PEER'],
    },
    'cwe-326':
    {
        '0-py': [' RSA.generate(3072)'],
        '1-py': [' DSA.generate(3072)'],
    },
    'cwe-329': 
    {
        '0-py': [' urandom(16)'],
    },
    'cwe-347':
    {
        '0-py': [" key", " algorithms=['HS256']"],
        '1-py': [" key", " algorithms=['HS256']"],
    },
    'cwe-400':
    {
        '0-py': [' re.escape'],
    },
    'cwe-643':
    {
        '0-py': [],
        '1-py': [],
    },
    'cwe-760':
    {
        '0-py': [' secrets.token_bytes(32)'],
    },
    'cwe-943':
    {
        '0-py': [],
    },
}

neg_constraints = {
    'cwe-022': {
        '0-py': [' send_file', ' os.path.join', 'send_file', 'os.path.join'],
        '1-py': [' send_file', ' os.path.join', 'send_file', 'os.path.join'],
        '2-py': [' extractall', 'extractall'],
        '3-c': [],
        '4-py': [' os.path.join', 'os.path.join'],
        '5-py': [' os.path.join', 'os.path.join'],
    },
    'cwe-078': {
        '0-py': [' + dirname', ' format(dirname)', ' % dirname', ' {dirname}',
                 '+ dirname', 'format(dirname)', '% dirname', '{dirname}'],
        '1-py': [' + username', 'format(username)', ' % username', ' {username}',
                 '+ username', 'format(username)', '% username', '{username}'],
        '2-py': [' + url', ' format(url)', ' % url', ' {url}',
                 '+ url', 'format(url)', '% url', '{url}'],
        '3-c': [' system', 'system', ' popen', 'popen'],
        '4-c': [' system', 'system', ' popen', 'popen'],
        '5-c': [' system', 'system', ' popen', 'popen'],
        '6-py': [' os.system', 'os.system', ' shell=True', 'shell=True'],
        '7-py': [' os.system', 'os.system', ' shell=True', 'shell=True'],
    },
    'cwe-079': {
        '0-py': [' + username', ' % username', ' format(username)', ' {username}',
                 '+ username', '% username', 'format(username)', '{username}'],
        '1-py': [],
        '2-py': [],
    },
    'cwe-089': {
        '0-py': [' + email', ' % email', ' format(email)', ' {email}', ' \'%s\'', ' "%s"',
                 '+ email', '% email', 'format(email)', '{email}', '\'%s\'', '"%s"'],
        '1-py': [' + username', ' % username', ' format(username)', ' {username}', ' \'%s\'', ' "%s"',
                 '+ username', '% username', 'format(username)', '{username}', '\'%s\'', '"%s"'],
        '2-py': [' + username', ' % username', ' format(username)', ' {username}', ' \'%s\'', ' "%s"',
                 '+ username', '% username', 'format(username)', '{username}', '\'%s\'', '"%s"'],
        '3-py': [' + username', '+ username', ' % username', '% username', ' format(username)', 'format(username)', 
                 ' {username}', '{username}', ' \'%s\'', '\'%s\'', ' "%s"', '"%s"'],
    },
    'cwe-125': {
        '0-c': [],
        '1-c': [],
        '2-c': [],
    },
    'cwe-190':{
        '0-c': [],
        '1-c': [],
        '2-c': [],
    },
    'cwe-416': {
        '0-c': [],
        '1-c': ['buffer', ' buffer'],
    },
    'cwe-476': {
        '0-c': [],
        '2-c': [],
    },
    'cwe-787': {
        '0-c': ['sprintf', ' sprintf'],
        '1-c': [],
        '2-c': [],
    },
    'cwe-119':
    {
        '0-c': [],
        '1-c': [],
        '2-c': [],
    },
    'cwe-502':
    {
        '0-py': [' yaml.load', 'yaml.load'],
        '1-py': [' yaml.load', 'yaml.load'],
        '2-py': [' yaml.load', 'yaml.load'],
        '3-py': [' pickle', 'pickle'],
        '4-py': [' yaml.load', 'yaml.load'],
    },
    'cwe-732':
    {
        '0-c': [],
        '1-c': [],
        '2-py': [],
    },
    'cwe-020':
    {
        '0-py': [],
        '1-py': [],
        '2-py': [' yaml.load', 'yaml.load'],
        '3-py': [],
        '4-py': [' pickle', 'pickle'],
    },
    'cwe-117':
    {
        '0-py': [],
        '1-py': [],
        '2-py': [],
    },
    'cwe-215':
    {
        '0-py': ['debug=True', ' debug=True'],
    },
    'cwe-312':
    {
        '0-py': []
    },
    'cwe-327':
    {
        '0-py': [' hashlib.sha1', ' hashlib.md5', 'hashlib.sha1', 'hashlib.md5'],
        '1-py': ['hashlib', ' hashlib'],
        '2-py': ['DES', ' DES'],
    },
    'cwe-377':
    {
        '0-py': ['mktemp', ' mktemp'],
        '1-py': ['mktemp', ' mktemp'],
    },
    'cwe-611':
    {
        '0-py': [],
        '1-py': [],
        '2-py': [],
        '3-py': [],
        '4-py': [],
        '5-py': [],
    },
    'cwe-777':
    {
        '0-py': [],
        '1-py': [],
    },
    'cwe-918':
    {
        '0-py': [],
        '1-py': [],
    },
    'cwe-601':
    {
        '0-py': [],
        '1-py': [],
        '2-py': [],
        '3-py': [],
        '4-py': [],
    },
    'cwe-776':
    {
        '0-py': ["xml.etree.ElementTree", " xml.etree.ElementTree"],
    },
    'cwe-094':
    {
        '0-py': [],
    },
    'cwe-095':
    {
        '0-py': [],
    },
    'cwe-113':
    {
        '0-py': [],
        '1-py': [],
    },
    'cwe-295':
    {
        '0-py': [' verify=False', 'verify=False', ' verify=0', 'verify=0'],
        '1-py': [' AutoAddPolicy', 'AutoAddPolicy'],
        '2-py': [' _create_stdlib_context', '_create_stdlib_context'],
        '3-py': [' SSL.VERIFY_NONE', 'SSL.VERIFY_NONE'],
    },
    'cwe-326':
    {
        '0-py': [' RSA.generate(1024)', 'RSA.generate(1024)'],
        '1-py': [' DSA.generate(1024)', 'DSA.generate(1024)'],
    },
    'cwe-329':
    {
        '0-py': [],
    },
    'cwe-347':
    {
        '0-py': [],
        '1-py': [],
    },
    'cwe-400':
    {
        '0-py': [],
    },
    'cwe-643':
    {
        '0-py': [' + tagid', '+ tagid', ' % tagid', '% tagid', ' format(tagid)', 'format(tagid)', ' {tagid}', '{tagid}'],
        '1-py': [' + username', '+ username', ' % username', '% username', ' format(username)', 'format(username)', ' {username}', '{username}'],
    },
    'cwe-760':
    {
        '0-py': [],
    },
    'cwe-943':
    {
        '0-py': [' + username', '+ username', ' % username', '% username', ' format(username)', 'format(username)', ' {username}', '{username}'],
    },
}

constraints = {
    'pos': pos_constraints,
    'neg': neg_constraints
}
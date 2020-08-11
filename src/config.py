from os.path import expanduser

HOME = expanduser("~")
API = "http://127.0.0.1:8080/v1"

ICON = '''
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
SUVORK5CYII='''.encode()

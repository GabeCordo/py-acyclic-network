from os import path

PATH_SYSTEM = path.abspath(__file__)[:-25]

# json files
PATH_CONFIG = PATH_SYSTEM + 'common/config.json'

# txt encoded cache files
PATH_CACHE_BLACKLIST = PATH_SYSTEM + 'common/cache/blacklist.txt'
PATH_CACHE_PENDING = PATH_SYSTEM + 'common/cache/pending.txt'
PATH_CACHE_WHITELIST = PATH_SYSTEM + 'common/cache/whitelist.txt'
PATH_CACHE_COLLECTION = PATH_SYSTEM + 'common/cache/collection/'

# pem encryption key folders
PATH_ASYNC_PUBLIC = PATH_SYSTEM + 'common/crypto/public.pem'
PATH_ASYNC_PRIVATE = PATH_SYSTEM + 'common/crypto/private.pem'

# downloaded routines
PATH_COLLECTION_ROUTINES = PATH_SYSTEM + 'common/collection/'
PATH_COLLECTION_TEMPLATE = PATH_SYSTEM + 'common/collection/template/'

# folder directory paths
PATH_PREFIX_CLI = PATH_SYSTEM + 'pyacyclicnet/cli/'
PATH_PREFIX_UTILS = PATH_SYSTEM + 'pyacyclicnet/utils/'
PATH_PREFIX_MAIN = PATH_SYSTEM + 'pyacyclicnet/core/'

# routine constants

STANDARD_ROUTINE_ROOT_FILES = ['config.yaml', 'routine.py', 'author.yaml']
STANDARD_ROUTINE_ROOT_DIRS = ['scripts', 'data']
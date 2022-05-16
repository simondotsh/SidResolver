#!/usr/bin/env python3

from src.cli import Cli
from src.rpc import LsadWrapper as LsadW

args = Cli.parse_and_validate()
requested_sids = args.sids

try:
    lsadw = LsadW(args)
    mapped_sids = lsadw.lookup_sids(requested_sids)
except Exception as e:
    print(str(e))
    exit(0)

print('sid,name,type')

# If a SID has not been mapped, it will not be in the returned results.
for sid in requested_sids:
    name = 'NOT_FOUND'
    type = 'NOT_FOUND'

    if sid in mapped_sids:
        if mapped_sids[sid]['name']:
            name = mapped_sids[sid]['name']
            type = mapped_sids[sid]['type']

    print(f'{sid},{name},{type}')
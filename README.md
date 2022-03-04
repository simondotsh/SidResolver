# SidResolver
This script leverages MS-LSAT's `LsarLookupSids` to request the target to resolve the SID(s). The method is used with the lookup level of `LsapLookupWksta`, which will attempt mapping in the following order:

1. Locally (known SIDs, the BUILTIN domain and then the local account one)
2. Primary Domain (therefore, the DC will be queried)
3. Trusted Domains (DC(s) of the trusted domain(s))

If some SIDs cannot be resolved, they will simply be reported as is.

## Installation
```
git clone https://github.com/simondotsh/SidResolver
cd SidResolver/
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

## Usage
```
usage: sidresolver.py [-h] -u USERNAME -d DOMAIN [-p PASSWORD | -nt NT_HASH] [-t TIMEOUT] -s SIDS target

positional arguments:
  target                Target to request SID resolving from (IP or hostname).

optional arguments:
  -h, --help            show this help message and exit

  -u USERNAME, --username USERNAME
                        Username used to authenticate on targets.

  -d DOMAIN, --domain DOMAIN
                        Domain to authenticate to.

  -p PASSWORD, --password PASSWORD
                        Username's password. If a password or a hash is not provided, a prompt will request the password on execution.

  -nt NT_HASH, --nt-hash NT_HASH
                        Username's NT hash.

  -t TIMEOUT, --timeout TIMEOUT
                        Drops connection after x seconds when waiting to receive packets from the target (default: 2).

  -s SIDS, --sid SIDS   A single SID or path to a file containing SIDs.
```

## Examples

Single SID:
```
python3 sidresolver.py -u lowprivs -d AD.LOCAL -s S-1-5-21-642930740-2278254436-1623907929-1130 192.168.56.2
sid,name,type
S-1-5-21-642930740-2278254436-1623907929-1130,AD\local_admin_group,SidTypeGroup
```

File with SIDs:
```
cat ~/sids.txt
S-1-5-21-642930740-2278254436-1623907929-1114
S-1-5-21-642930740-2278254436-1623907929-1121
S-1-5-21-10528877-698593294-472013772-1107

python3 sidresolver.py -u lowprivs -d AD.LOCAL -s ~/sids.txt 192.168.56.2
sid,name,type
S-1-5-21-642930740-2278254436-1623907929-1114,AD\da,SidTypeUser
S-1-5-21-642930740-2278254436-1623907929-1121,AD\user1,SidTypeUser
S-1-5-21-10528877-698593294-472013772-1107,AD2\trusted_domain,SidTypeUser
```
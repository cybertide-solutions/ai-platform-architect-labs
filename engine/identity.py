from dataclasses import dataclass
@dataclass(frozen=True)
class Identity:
    subject: str
    tenant: str
    roles: tuple
    entitlement_version: int=1
BUYER=Identity('buyer-1','aster',('buyer',))
FINANCE=Identity('finance-1','aster',('buyer','finance'))
BEACON=Identity('buyer-9','beacon',('buyer',))
def visible(record,who):
    return record['tenant']==who.tenant and bool(set(record['roles'])&set(who.roles)) and record['active'] and record['approved']

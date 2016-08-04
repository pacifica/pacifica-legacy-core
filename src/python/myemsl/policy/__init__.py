#!/usr/bin/python
"""
This module drives policy for EMSL the following rules apply to both
upload permissions and what they can see when interacting with the
uploader.
"""

from myemsl.metadata import get_user_info, get_all_proposals, get_all_instruments, get_proposals_from_user, get_proposal_info, get_instruments_from_proposal, get_instrument_info
from sys import argv

def get_policy_userinfo(userid):
    """
    Get the info for a user based on current policy on what they are
    allowed to see.

    if user is emsl_employee
        see everything...
    else
        see proposals they are member or POC on
        see instruments attached to those proposals
    """
    user_info = get_user_info(userid)
    if user_info['emsl_employee'] == 'Y':
        user_info['proposals'] = get_all_proposals()
        user_info['instruments'] = get_all_instruments()
    else:
        user_info['proposals'] = [ get_proposal_info(prop) for prop in get_proposals_from_user(userid) ]
        inst_ids = []
        for prop in get_proposals_from_user(userid):
            for instid in get_instruments_from_proposal(prop):
                if not instid in inst_ids:
                    inst_ids.append(instid)
        user_info['instruments'] = [ get_instrument_info(inst) for inst in inst_ids ]
    return user_info

if __name__ == '__main__':
    print get_policy_userinfo(int(argv[1]))

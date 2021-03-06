#!/usr/bin/python
"""
This module drives policy for EMSL the following rules apply to both
upload permissions and what they can see when interacting with the
uploader.
"""

from myemsl.metadata import get_user_info, get_all_proposals, get_all_instruments, get_proposals_from_user, get_proposal_info, get_instruments_from_proposal, get_instrument_info, get_all_proposal_instruments
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
    prop_inst_list = get_all_proposal_instruments()
    if user_info['emsl_employee'] == 'Y':
        props = {}
        for prop in get_all_proposals():
            prop_id = prop['proposal_id']
            prop['instruments'] = prop_inst_list[prop_id] if prop_id in prop_inst_list else []
            props[str(prop_id)] = prop
        insts = {}
        for inst in get_all_instruments():
            insts[str(inst['instrument_id'])] = inst
        user_info['proposals'] = props
        user_info['instruments'] = insts
    else:
        props = {}
        for prop_id in get_proposals_from_user(userid):
            prop = get_proposal_info(prop_id)
            prop['instruments'] = prop_inst_list[prop_id] if prop_id in prop_inst_list else []
            props[str(prop_id)] = prop
        user_info['proposals'] = props
        inst_ids = []
        for prop in get_proposals_from_user(userid):
            for instid in get_instruments_from_proposal(prop):
                if not instid in inst_ids:
                    inst_ids.append(instid)
        insts = {}
        for inst in inst_ids:
            insts[str(inst)] = get_instrument_info(inst)
        user_info['instruments'] = insts
    return user_info

if __name__ == '__main__':
    print get_policy_userinfo(int(argv[1]))

from django_auth_ldap.config import LDAPGroupQuery


def join_ldap_group_querys(group_list, group_dn):

    s = "cn={0},{1}"

    query = None
    for group in group_list:
        if query is None:
            # First query object
            query = LDAPGroupQuery(s.format(group, group_dn))
        else:
            # Append new querys with or
            query = (query | LDAPGroupQuery(s.format(group, group_dn)))

    return query

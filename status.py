#!/usr/bin/env python3

import sys
from argparse import ArgumentParser
from datetime import datetime
from pprint import pprint

import dns.query

import adns
from desec import frontend_servers


def all_equal(l):
    if len(l) == 0:
        return True
    l = list(l)
    for i in range(1, len(l)):
        if l[i] != l[0]:
            return False
    return True


def filter_query_rrset(response, qname, qtype):
    try:
        return response.find_rrset(dns.message.ANSWER, qname, dns.rdataclass.IN, qtype)
    except KeyError:
        return None


def main(args):
    parser = ArgumentParser(
        prog='status',
        description='Queries all deSEC frontends with a given question and returns the result(s).'
    )
    parser.add_argument('rdtype', help="record set type to be queried", type=str)
    parser.add_argument('name', help="DNS name to be queried", type=str)
    args = parser.parse_args(args)

    print(f'{datetime.now()} Querying {len(frontend_servers)} servers for {args.rdtype} {args.name} ...')
    qname = dns.name.from_text(args.name)
    qtype = dns.rdatatype.from_text(args.rdtype)
    responses = adns.query_all(
        where_list=frontend_servers,
        q=dns.message.make_query(qname, qtype)
    )

    # Filter responses
    filtered_responses = {w: str(filter_query_rrset(r, qname, qtype)) for w, r in responses.items()}

    if all_equal(filtered_responses.values()):
        print(f'All servers returned:\n\n{next(iter(filtered_responses.values()))}')
    else:
        pprint(filtered_responses)
        print('@'*80)
        print('Server responses differ.')

if __name__ == '__main__':
    main(sys.argv[1:])


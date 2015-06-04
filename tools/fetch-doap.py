#!/usr/bin/python
# Copyright 2014 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

import os
import sys
from multiprocessing import Pool

import requests

from pgidocgen.util import get_gir_files
from pgidocgen.girdata import PROJECTS
from pgidocgen import BASEDIR


def fetch(project):
    print project.doap
    resp = requests.get(project.doap)
    if resp.status_code != requests.codes.ok:
        raise Exception(url)
    return resp.content, project


def main(argv):
    ns_list = set([n.split("-")[0] for n in get_gir_files().keys()])
    for p in PROJECTS:
        ns_list -= set(p.namespaces)

    print "Missing:"
    print sorted(ns_list)

    pool = Pool(20)
    for content, project in pool.imap_unordered(fetch, PROJECTS):
        for ns in project.namespaces:
            path = os.path.join(BASEDIR, 'data', 'doap', ns) + ".doap"
            with open(path, 'wb') as h:
                h.write(content)


if __name__ == '__main__':
    sys.exit(main(sys.argv))

#!/usr/bin/env python2
# -*- coding: utf-8 -*-

# Contest Management System
# Copyright © 2013 Luca Wehrstedt <luca.wehrstedt@gmail.com>
# Copyright © 2013 Giovanni Mascellani <mascellani@poisson.phc.unipi.it>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""A script to update a dump created by CMS.

This script updates a dump (i.e. a set of exported contest data, as
created by ContestExporter) of the Contest Management System from any
of the old supported versions to the current one.

"""

# We enable monkey patching to make many libraries gevent-friendly
# (for instance, urllib3, used by requests)
import gevent.monkey
gevent.monkey.patch_all()

import os
import io
import json
import argparse

from cms import logger
from cms.db import version as model_version


def main():
    parser = argparse.ArgumentParser(
        description="Updater of CMS contest dumps.")
    parser.add_argument(
        "-V", "--to-version", action="store", type=int, default=-1,
        help="Update to given version number")
    parser.add_argument(
        "path", help="location of the dump or of the 'contest.json' file")

    args = parser.parse_args()
    path = args.path

    to_version = args.to_version
    if to_version == -1:
        to_version = model_version

    if not path.endswith("contest.json"):
        path = os.path.join(path, "contest.json")

    if not os.path.exists(path):
        logger.critical(
            "The given path doesn't exist or doesn't contain a contest "
            "dump in a format CMS is able to understand.")
        return

    with io.open(path, 'rb') as fin:
        data = json.load(fin, encoding="utf-8")

    # If no "_version" field is found we assume it's a v1.0
    # export (before the new dump format was introduced).
    dump_version = data.get("_version", 0)

    if dump_version == to_version:
        logger.info(
            "The dump you're trying to update is already stored using "
            "the most recent format supported by this version of CMS.")
        return

    if dump_version > to_version:
        logger.critical(
            "The dump you're trying to update is stored using a format "
            "that's more recent than the one supported by this version "
            "of CMS. You probably need to update CMS to handle it.")
        return

    for version in range(dump_version, to_version):
        # Update from version to version+1
        updater = __import__(
            "cmscontrib.updaters.update_%d" % (version + 1),
            globals(), locals(), ["Updater"]).Updater(data)
        data = updater.run()
        data["_version"] = version + 1

    assert data["_version"] == to_version

    with io.open(path, 'wb') as fout:
        json.dump(data, fout, encoding="utf-8", indent=4, sort_keys=True)


if __name__ == "__main__":
    main()

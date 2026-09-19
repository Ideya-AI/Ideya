""".venv/bin/python -m pipeline author <slug> [--stage stageN]
.venv/bin/python -m pipeline status <slug>
.venv/bin/python -m pipeline fetch <slug> <url> [--ns probe] [--class reference]
"""

import argparse
import sys

from . import sources, stages
from .topic import TopicDir


def main(argv=None):
    p = argparse.ArgumentParser(prog="pipeline")
    sub = p.add_subparsers(dest="cmd", required=True)

    a = sub.add_parser("author", help="take a topic from not_started to ready")
    a.add_argument("slug")
    a.add_argument("--stage", help="run only this stage, e.g. stage1")

    s = sub.add_parser("status", help="what the topic directory says")
    s.add_argument("slug")

    f = sub.add_parser("fetch", help="fetch one URL into a topic's sources store")
    f.add_argument("slug")
    f.add_argument("url")
    f.add_argument("--ns", default="probe")
    f.add_argument("--class", dest="cls", default="reference")

    o = p.parse_args(argv)
    if o.cmd == "author":
        return stages.author(o.slug, only=o.stage)
    if o.cmd == "status":
        return stages.status(o.slug)
    if o.cmd == "fetch":
        res = sources.Store(TopicDir(o.slug)).fetch(o.url, o.ns, o.cls)
        print(
            res.model_dump_json(by_alias=True, indent=1)
            if not isinstance(res, dict)
            else res
        )
        return 0 if not isinstance(res, dict) else 1


if __name__ == "__main__":
    sys.exit(main())

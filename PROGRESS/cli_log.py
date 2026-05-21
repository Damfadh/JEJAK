#!/usr/bin/env python3
"""Simple CLI to add progress or issue entries to PROGRESS tracker."""
import argparse
from log_helper import append_progress_entry, append_issue_entry


def cmd_progress(args):
    entry = append_progress_entry(
        author=args.author,
        title=args.title,
        status=args.status,
        description=args.description or "",
        files_changed=args.files.split(',') if args.files else [],
        next_steps=args.next or "",
        notes=args.notes or "",
    )
    print("Added progress entry:\n")
    print(entry)


def cmd_issue(args):
    entry = append_issue_entry(
        issue_id=args.id,
        reporter=args.reporter,
        title=args.title,
        status=args.status,
        priority=args.priority,
        description=args.description,
        steps=args.steps or "",
        assigned=args.assigned or "",
        solution=args.solution or "",
        comments=args.comments or "",
    )
    print("Added issue entry:\n")
    print(entry)


parser = argparse.ArgumentParser(description="PROGRESS tracker CLI")
sub = parser.add_subparsers(dest='cmd')

p = sub.add_parser('progress', help='Add a progress entry')
p.add_argument('--author', required=True)
p.add_argument('--title', required=True)
p.add_argument('--status', required=True, choices=['open','in-progress','done'])
p.add_argument('--description')
p.add_argument('--files', help='comma-separated file paths')
p.add_argument('--next', help='next steps')
p.add_argument('--notes')

q = sub.add_parser('issue', help='Add an issue entry')
q.add_argument('--id', required=True)
q.add_argument('--reporter', required=True)
q.add_argument('--title', required=True)
q.add_argument('--status', required=True, choices=['open','in-progress','resolved'])
q.add_argument('--priority', required=True, choices=['P0','P1','P2'])
q.add_argument('--description', required=True)
q.add_argument('--steps')
q.add_argument('--assigned')
q.add_argument('--solution')
q.add_argument('--comments')

if __name__ == '__main__':
    args = parser.parse_args()
    if args.cmd == 'progress':
        cmd_progress(args)
    elif args.cmd == 'issue':
        cmd_issue(args)
    else:
        parser.print_help()

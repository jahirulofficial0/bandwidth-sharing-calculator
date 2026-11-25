#!/usr/bin/env python3
"""bandwidth_calc.py - fair-share bandwidth calculator.

Given a total internet bandwidth and a number of users, it prints:
  * the equal fair-share per user
  * a suggested guaranteed rate (limit-at) and burst ceiling
  * ready-to-paste GENERIC MikroTik RouterOS examples (simple queue + PCQ)

All example addresses are placeholders from the documentation range
192.0.2.0/24 (TEST-NET-1). Replace them with your own values.

Examples:
  python3 bandwidth_calc.py --total 100 --users 20
  python3 bandwidth_calc.py --total 200 --users 30 --cap 20
  python3 bandwidth_calc.py --total 50 --users 10 --guarantee-percent 50
"""

import argparse
import math
import sys


def fmt(value):
    """Format a Mbps value without trailing zeros."""
    if value == int(value):
        return f"{int(value)}"
    return f"{value:.2f}".rstrip("0").rstrip(".")


def main(argv=None):
    ap = argparse.ArgumentParser(description="Fair-share bandwidth calculator")
    ap.add_argument("--total", type=float, required=True,
                    help="total bandwidth in Mbps, e.g. 100")
    ap.add_argument("--users", type=int, required=True,
                    help="number of users sharing the link, e.g. 20")
    ap.add_argument("--cap", type=float, default=None,
                    help="optional per-user maximum in Mbps")
    ap.add_argument("--guarantee-percent", type=float, default=50.0,
                    help="percent of the fair share used as guaranteed rate "
                         "(limit-at). Default: 50")
    args = ap.parse_args(argv)

    if args.total <= 0:
        ap.error("--total must be greater than 0")
    if args.users <= 0:
        ap.error("--users must be greater than 0")
    if not 0 < args.guarantee_percent <= 100:
        ap.error("--guarantee-percent must be between 1 and 100")

    fair = args.total / args.users
    max_limit = fair
    note = ""
    if args.cap is not None:
        if args.cap <= 0:
            ap.error("--cap must be greater than 0")
        max_limit = min(args.cap, fair) if args.cap < fair else fair
        if args.cap < fair:
            leftover = args.total - args.cap * args.users
            note = (f"Note: the cap is below the fair share, so "
                    f"{fmt(leftover)} Mbps stays unused unless you "
                    f"redistribute it.")
            max_limit = args.cap
    guarantee = max_limit * args.guarantee_percent / 100.0

    print("=== Fair-share result ===")
    print(f"Total bandwidth : {fmt(args.total)} Mbps")
    print(f"Users           : {args.users}")
    print(f"Fair share/user : {fmt(fair)} Mbps")
    print(f"Per-user max    : {fmt(max_limit)} Mbps")
    print(f"Guaranteed/user : {fmt(guarantee)} Mbps "
          f"({fmt(args.guarantee_percent)}% of max)")
    if note:
        print(note)

    ml = fmt(math.floor(max_limit)) if max_limit >= 1 else fmt(max_limit)
    la = fmt(math.floor(guarantee)) if guarantee >= 1 else fmt(guarantee)

    print()
    print("=== Generic MikroTik RouterOS examples ===")
    print("Placeholders only - replace names and addresses with your own.")
    print()
    print("# One simple queue per user (repeat per user, change the target):")
    print(f'/queue simple add name="user-01" target=192.0.2.10/32 '
          f'max-limit={ml}M/{ml}M limit-at={la}M/{la}M '
          f'comment="fair share - replace with real user"')
    print()
    print("# PCQ: one queue type that shares equally by itself:")
    print('/queue type add name="pcq-fair-down" kind=pcq pcq-rate=0 '
          'pcq-classifier=dst-address')
    print('/queue type add name="pcq-fair-up" kind=pcq pcq-rate=0 '
          'pcq-classifier=src-address')
    print(f'/queue tree add name="fair-down" parent=global '
          f'queue=pcq-fair-down max-limit={fmt(args.total)}M')
    print(f'/queue tree add name="fair-up" parent=global '
          f'queue=pcq-fair-up max-limit={fmt(args.total)}M')
    return 0


if __name__ == "__main__":
    sys.exit(main())

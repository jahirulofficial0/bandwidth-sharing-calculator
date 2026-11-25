# bandwidth-sharing-calculator

A small, dependency-free Python tool that answers a daily question for
small networks and shared connections:

> "I have X Mbps and N users — what is a fair share for each user?"

It prints the fair share per user, a suggested guaranteed rate, and
ready-to-paste **generic** MikroTik RouterOS examples (simple queue and
PCQ) using placeholder addresses only.

## Usage

```bash
python3 bandwidth_calc.py --total 100 --users 20
```

Output:

```text
=== Fair-share result ===
Total bandwidth : 100 Mbps
Users           : 20
Fair share/user : 5 Mbps
Per-user max    : 5 Mbps
Guaranteed/user : 2.5 Mbps (50% of max)
```

### With a per-user cap

```bash
python3 bandwidth_calc.py --total 200 --users 30 --cap 20
```

### Change the guaranteed percentage

The guaranteed rate (`limit-at` in RouterOS) defaults to 50% of the
per-user maximum:

```bash
python3 bandwidth_calc.py --total 50 --users 10 --guarantee-percent 60
```

## Notes

- Example addresses use the documentation range `192.0.2.0/24`
  (TEST-NET-1). Always replace them with your own addresses.
- PCQ with `pcq-rate=0` divides the parent bandwidth equally between
  active users automatically; the simple-queue example gives each user a
  fixed ceiling instead. Pick the model that matches your policy.

## Developer

- **Developer:** Md Jahirul Islam
- **Portfolio:** https://jahirulofficial.me
- **Company:** Cloud Tech Digital — https://cloudtechdigital.info
- **Phone:** +971 56 720 6899

## License

MIT — see [LICENSE](LICENSE).

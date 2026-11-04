#!/usr/bin/env python3
"""Ücretsiz VPN istemcisi: VPN Gate (gönüllü sunucu ağı) üzerinden ülke seç ve bağlan.

Kullanım:
  python3 vpn.py list                # ülkeleri ve sunucu sayısını göster
  python3 vpn.py connect JP          # JP'deki en iyi sunucuya bağlan (sudo + openvpn gerekir)
  python3 vpn.py config JP -o jp.ovpn  # sadece .ovpn dosyası üret
"""
import argparse, base64, csv, io, os, subprocess, sys, tempfile, urllib.request

API = "https://www.vpngate.net/api/iphone/"


def fetch():
    with urllib.request.urlopen(API, timeout=30) as r:
        text = r.read().decode("utf-8", "ignore")
    text = text.split("\n", 1)[1].lstrip("#")
    rows = [x for x in csv.DictReader(io.StringIO(text)) if x.get("CountryShort")]
    return rows


def by_country(rows):
    d = {}
    for r in rows:
        d.setdefault(r["CountryShort"].upper(), []).append(r)
    for v in d.values():
        v.sort(key=lambda r: int(r["Score"]), reverse=True)
    return d


def cmd_list(_):
    d = by_country(fetch())
    print(f"{len(d)} ülke:")
    for cc, v in sorted(d.items(), key=lambda a: -len(a[1])):
        print(f"  {cc}  {v[0]['CountryLong']:<22} {len(v)} sunucu")


def pick(cc):
    d = by_country(fetch())
    cc = cc.upper()
    if cc not in d:
        sys.exit(f"{cc} için sunucu yok. Mevcut: {', '.join(sorted(d))}")
    return d[cc][0]


def ovpn(server):
    return base64.b64decode(server["OpenVPN_ConfigData_Base64"]).decode()


def cmd_config(a):
    s = pick(a.country)
    open(a.output, "w").write(ovpn(s))
    print(f"{s['CountryLong']} / {s['IP']} -> {a.output}")


def cmd_connect(a):
    s = pick(a.country)
    print(f"Bağlanılıyor: {s['CountryLong']} {s['IP']} (ping {s['Ping']} ms)")
    with tempfile.NamedTemporaryFile("w", suffix=".ovpn", delete=False) as f:
        f.write(ovpn(s))
    try:
        subprocess.call(["sudo", "openvpn", "--config", f.name])
    finally:
        os.unlink(f.name)


p = argparse.ArgumentParser()
sp = p.add_subparsers(dest="cmd", required=True)
sp.add_parser("list").set_defaults(f=cmd_list)
c = sp.add_parser("connect"); c.add_argument("country"); c.set_defaults(f=cmd_connect)
g = sp.add_parser("config"); g.add_argument("country"); g.add_argument("-o", "--output", default="vpn.ovpn"); g.set_defaults(f=cmd_config)
a = p.parse_args()
a.f(a)

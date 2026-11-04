#!/usr/bin/env python3
"""Avrupa odaklı ücretsiz VPN istemcisi.

Önce KENDİ sunucuların (WireGuard, servers.json), yedek olarak VPN Gate
(gönüllü, güvenilmez sunucular, sadece Avrupa'ya filtrelenmiş) kullanılır.

Kullanım:
  python3 vpn.py list [--all]        # ülkeleri göster (--all: Avrupa dışı da)
  python3 vpn.py connect DE          # ülkeni seç; kendi sunucun varsa ona bağlanır
  python3 vpn.py connect AT --vpngate  # zorla VPN Gate kullan
  python3 vpn.py config AT -o at.ovpn  # sadece .ovpn üret
"""
import argparse, base64, csv, io, json, os, re, subprocess, sys, tempfile, urllib.request

API = "https://www.vpngate.net/api/iphone/"
HERE = os.path.dirname(os.path.abspath(__file__))
# Avrupa ülke kodları (AB/AEA + Birleşik Krallık, İsviçre, Türkiye vb.)
EUROPE = set(
    "AL AD AT BY BE BA BG HR CY CZ DK EE FI FR DE GR HU IS IE IT XK LV LI LT LU "
    "MT MD MC ME NL MK NO PL PT RO RU SM RS SK SI ES SE CH TR UA GB".split()
)
# Üçüncü taraf .ovpn dosyasında komut çalıştırabilecek direktifler
DANGEROUS = re.compile(
    r"^\s*(script-security|up|down|route-up|route-pre-down|ipchange|learn-address|"
    r"client-connect|client-disconnect|tls-verify|auth-user-pass-verify|plugin|"
    r"setenv|setenv-safe|management|config|cd|chroot|daemon|log|log-append|writepid|"
    r"ifconfig-noexec)\b",
    re.I,
)


def own_servers():
    try:
        d = json.load(open(os.path.join(HERE, "servers.json"), encoding="utf-8"))
    except FileNotFoundError:
        return {}
    return {
        k.upper(): v
        for k, v in d.items()
        if not k.startswith("_") and os.path.exists(os.path.join(HERE, v["config"]))
    }


def fetch():
    with urllib.request.urlopen(API, timeout=30) as r:
        text = r.read().decode("utf-8", "ignore")
    text = text.split("\n", 1)[1].lstrip("#")
    return [x for x in csv.DictReader(io.StringIO(text)) if x.get("CountryShort")]


def by_country(rows, europe_only=True):
    d = {}
    for r in rows:
        cc = r["CountryShort"].upper()
        if europe_only and cc not in EUROPE:
            continue
        d.setdefault(cc, []).append(r)
    for v in d.values():
        v.sort(key=lambda r: int(r["Score"]), reverse=True)
    return d


def cmd_list(a):
    own = own_servers()
    print("Kendi sunucuların (güvenli):")
    for cc, v in sorted(own.items()):
        print(f"  {cc}  {v['ad']}")
    if not own:
        print("  (yok - setup-server.sh ile kur, servers.json'a ekle)")
    d = by_country(fetch(), not a.all)
    kapsam = "tüm dünya" if a.all else "sadece Avrupa"
    print(f"\nVPN Gate ({kapsam}; güvenilmez gönüllü sunucular): {len(d)} ülke")
    for cc, v in sorted(d.items(), key=lambda x: -len(x[1])):
        print(f"  {cc}  {v[0]['CountryLong']:<22} {len(v)} sunucu")


def pick(cc, europe_only=True):
    d = by_country(fetch(), europe_only)
    cc = cc.upper()
    if cc not in d:
        sys.exit(f"{cc} için VPN Gate sunucusu yok. Mevcut: {', '.join(sorted(d))}")
    return d[cc][0]


def ovpn(server):
    cfg = base64.b64decode(server["OpenVPN_ConfigData_Base64"]).decode("utf-8", "ignore")
    bad = [l.strip() for l in cfg.splitlines() if DANGEROUS.match(l)]
    if bad:
        sys.exit(f"Güvenlik: sunucu config'i tehlikeli direktif içeriyor, reddedildi: {bad[:3]}")
    return cfg


def cmd_config(a):
    s = pick(a.country, not a.all)
    open(a.output, "w").write(ovpn(s))
    print(f"{s['CountryLong']} / {s['IP']} -> {a.output}")


def cmd_connect(a):
    own = own_servers().get(a.country.upper())
    if own and not a.vpngate:
        print(f"Kendi sunucuna bağlanılıyor: {own['ad']}")
        sys.exit(subprocess.call(["sudo", "wg-quick", "up", os.path.join(HERE, own["config"])]))
    s = pick(a.country, not a.all)
    cfg = ovpn(s)
    print(f"VPN Gate: {s['CountryLong']} {s['IP']} (ping {s['Ping']} ms) - güvenilmez sunucu!")
    with tempfile.NamedTemporaryFile("w", suffix=".ovpn", delete=False) as f:
        f.write(cfg)
    try:
        subprocess.call(["sudo", "openvpn", "--script-security", "1", "--config", f.name])
    finally:
        os.unlink(f.name)


p = argparse.ArgumentParser()
sp = p.add_subparsers(dest="cmd", required=True)
l = sp.add_parser("list"); l.add_argument("--all", action="store_true"); l.set_defaults(f=cmd_list)
c = sp.add_parser("connect"); c.add_argument("country")
c.add_argument("--vpngate", action="store_true"); c.add_argument("--all", action="store_true"); c.set_defaults(f=cmd_connect)
g = sp.add_parser("config"); g.add_argument("country"); g.add_argument("-o", "--output", default="vpn.ovpn")
g.add_argument("--all", action="store_true"); g.set_defaults(f=cmd_config)
a = p.parse_args()
a.f(a)

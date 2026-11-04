#!/usr/bin/env bash
# Ubuntu/Debian sunucuda root olarak çalıştır:  bash setup-server.sh
# Çıktı: istemci WireGuard config'i. Bilgisayarında vpn/configs/<ULKE>.conf olarak kaydet.
set -euo pipefail
apt-get update -y && apt-get install -y wireguard
IFACE=$(ip route show default | awk '{print $5; exit}')
PUBIP=$(curl -s https://api.ipify.org)
umask 077
mkdir -p /etc/wireguard && cd /etc/wireguard
wg genkey | tee srv.key | wg pubkey > srv.pub
wg genkey | tee cli.key | wg pubkey > cli.pub
cat > wg0.conf <<EOF
[Interface]
Address = 10.8.0.1/24
ListenPort = 51820
PrivateKey = $(cat srv.key)
PostUp = iptables -A FORWARD -i wg0 -j ACCEPT; iptables -t nat -A POSTROUTING -o $IFACE -j MASQUERADE
PostDown = iptables -D FORWARD -i wg0 -j ACCEPT; iptables -t nat -D POSTROUTING -o $IFACE -j MASQUERADE

[Peer]
PublicKey = $(cat cli.pub)
AllowedIPs = 10.8.0.2/32
EOF
echo 'net.ipv4.ip_forward=1' > /etc/sysctl.d/99-wg.conf && sysctl --system >/dev/null
systemctl enable --now wg-quick@wg0
echo; echo "=== Bulut firewall'unda UDP 51820'yi de aç! ==="; echo "=== İSTEMCİ CONFIG (kaydet) ==="
cat <<EOF
[Interface]
PrivateKey = $(cat cli.key)
Address = 10.8.0.2/24
DNS = 1.1.1.1

[Peer]
PublicKey = $(cat srv.pub)
Endpoint = $PUBIP:51820
AllowedIPs = 0.0.0.0/0
PersistentKeepalive = 25
EOF

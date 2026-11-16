# Síť: mDNS (Avahi) + Wi-Fi hotspot fallback (NetworkManager)

```bash
# --- mDNS: hostname "reframe" -> http://reframe.local (Avahi běží v RPi OS defaultně)
hostnamectl                         # ověř Static hostname: reframe
avahi-browse -art | grep reframe    # z jiného Linuxu v síti

# /etc/avahi/services/reframe.service – ohlášení webové služby v síti (DNS-SD)
<?xml version="1.0" standalone='no'?>
<service-group>
  <name>reFrame Camera</name>
  <service><type>_http._tcp</type><port>80</port></service>
</service-group>

# --- Hotspot profil (RPi OS Bookworm používá NetworkManager)
sudo nmcli con add type wifi ifname wlan0 con-name reframe-ap autoconnect no \
  ssid reFrame-Camera 802-11-wireless.mode ap 802-11-wireless.band bg \
  ipv4.method shared wifi-sec.key-mgmt wpa-psk wifi-sec.psk "ZmenTohleHeslo"

# /usr/local/bin/reframe-wifi-fallback  (spouští ho reframe-wifi-fallback.service po startu)
#!/bin/bash
sleep 30                                    # počkej na známé Wi-Fi sítě
if ! nmcli -t -f STATE general | grep -q "^connected"; then
    nmcli con up reframe-ap                 # žádná síť -> vlastní AP, web na http://10.42.0.1
fi
```

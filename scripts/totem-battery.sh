#!/usr/bin/env bash
# Show the battery level of both TOTEM halves over Bluetooth (BlueZ D-Bus).
#
# The left half (central) exposes two Battery Level characteristics (0x2A19):
#   - its own level
#   - the right half's level, proxied, tagged "Peripheral 0" (needs
#     CONFIG_ZMK_SPLIT_BLE_CENTRAL_BATTERY_LEVEL_PROXY=y in totem_left.conf)
#
# Usage: scripts/totem-battery.sh [device name, default TOTEM]
set -euo pipefail

NAME="${1:-TOTEM}"
BATT_UUID="00002a19-0000-1000-8000-00805f9b34fb"

mac=$(bluetoothctl devices | awk -v n="$NAME" '$3 == n && NF == 3 {print $2; exit}')
[[ -n "$mac" ]] || { echo "No Bluetooth device named '$NAME'." >&2; exit 1; }

dev="/org/bluez/hci0/dev_${mac//:/_}"
connected=$(busctl get-property org.bluez "$dev" org.bluez.Device1 Connected | awk '{print $2}')
[[ "$connected" == "true" ]] || { echo "$NAME ($mac) is not connected." >&2; exit 1; }

left=""
right=""

# GATT Battery Level characteristics. The proxied one (right half) carries a
# User Description descriptor (0x2901) "Peripheral 0"; the left half's does not.
while read -r char; do
  uuid=$(busctl get-property org.bluez "$char" org.bluez.GattCharacteristic1 UUID | awk '{print $2}' | tr -d '"')
  [[ "$uuid" == "$BATT_UUID" ]] || continue
  # ReadValue returns: ay 1 <byte>
  val=$(busctl call org.bluez "$char" org.bluez.GattCharacteristic1 ReadValue 'a{sv}' 0 2>/dev/null | awk '{print $3}')
  [[ -n "$val" ]] || continue
  is_peripheral=0
  while read -r desc; do
    duuid=$(busctl get-property org.bluez "$desc" org.bluez.GattDescriptor1 UUID | awk '{print $2}' | tr -d '"')
    [[ "$duuid" == 00002901-* ]] && is_peripheral=1
  done < <(busctl tree org.bluez --list | grep -E "^${char}/desc[0-9a-f]+$")
  if (( is_peripheral )); then right="$val"; else left="$val"; fi
done < <(busctl tree org.bluez --list | grep -E "^${dev}/service[0-9a-f]+/char[0-9a-f]+$" | sort)

# Fallback: BlueZ battery plugin may claim the left half's service (Battery1)
if [[ -z "$left" ]] && pct=$(busctl get-property org.bluez "$dev" org.bluez.Battery1 Percentage 2>/dev/null); then
  left=$(awk '{print $2}' <<<"$pct")
fi

echo "Left : ${left:-n/a}${left:+%}"
echo "Right: ${right:-n/a (needs the battery proxy firmware on the left half)}${right:+%}"
[[ -n "$left$right" ]]

#!/usr/bin/env bash

# Options
shutdown=' Shutdown'
reboot='󰜉 Reboot'
lock=' Lock'
cancel='󰜺 Cancel'

# Get user selection via Rofi
chosen=$(echo -e "$shutdown\n$reboot\n$lock\n$cancel" | rofi -dmenu -i -p "Power Menu:" -theme-str 'window {width: 15%;} listview {lines: 4;}')

case "$chosen" in
    "$shutdown")
        systemctl poweroff
        ;;
    "$reboot")
        systemctl reboot
        ;;
    "$lock")
        # Replace with your lock command if you have one (e.g., i3lock)
        loginctl lock-session
        ;;
    *)
        exit 0
        ;;
esac

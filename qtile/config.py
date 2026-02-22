import os
import subprocess
from libqtile import bar, layout, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy

# Import extras for the modern rounded 'pill' look
try:
    from qtile_extras import widget as extrawidget
    from qtile_extras.widget.decorations import RectDecoration
except ImportError:
    extrawidget = widget
    RectDecoration = None

mod = "mod4"
terminal = "alacritty"

# --------------------
# Keybindings
# --------------------
keys = [
    Key([mod], "h", lazy.layout.left()),
    Key([mod], "l", lazy.layout.right()),
    Key([mod], "j", lazy.layout.down()),
    Key([mod], "k", lazy.layout.up()),
    Key([mod], "space", lazy.layout.next()),
    Key([mod, "shift"], "h", lazy.layout.shuffle_left()),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right()),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down()),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up()),
    Key([mod, "control"], "h", lazy.layout.grow_left()),
    Key([mod, "control"], "l", lazy.layout.grow_right()),
    Key([mod, "control"], "j", lazy.layout.grow_down()),
    Key([mod, "control"], "k", lazy.layout.grow_up()),
    Key([mod], "n", lazy.layout.normalize()),
    Key([mod], "Return", lazy.spawn(terminal)),
    Key([mod], "d", lazy.spawn("rofi -show drun")),
    Key([mod], "Tab", lazy.next_layout()),
    Key([mod], "w", lazy.window.kill()),
    Key([mod], "f", lazy.window.toggle_fullscreen()),
    Key([mod], "t", lazy.window.toggle_floating()),
    Key([mod, "control"], "r", lazy.reload_config()),
    Key([mod, "control"], "q", lazy.shutdown()),
]

# --------------------
# Groups (T, F, 1-9)
# --------------------
groups = [
    Group("T", layout="columns"),
    Group("F", layout="columns", matches=[Match(wm_class="firefox")]),
]
for i in "123456789":
    groups.append(Group(i))

for i in groups:
    keys.extend([
        Key([mod], i.name, lazy.group[i.name].toscreen()),
        Key([mod, "shift"], i.name, lazy.window.togroup(i.name, switch_group=True)),
    ])

# --------------------
# Decoration Helper
# --------------------
def get_pill(color):
    if RectDecoration is None: return []
    return [RectDecoration(colour=color, radius=10, filled=True, padding_y=2, group=True)]

# --------------------
# Layouts (2px Gaps)
# --------------------
layouts = [
    layout.Columns(
        border_focus="#87ceeb", 
        border_normal="#1a1b26", 
        border_width=2, 
        margin=2, # Strictly 2px gaps between windows
    ),
    layout.Max(),
]

# --------------------
# --------------------
# Bar & Widgets
# --------------------
widget_defaults = dict(
    font="JetBrains Mono Nerd Font", 
    fontsize=13, 
    padding=8
)

screens = [
    Screen(
        wallpaper="/home/lapu/Walpapers/1.jpg",
        wallpaper_mode="stretch",
        top=bar.Bar(
            [
                extrawidget.GroupBox(
                    highlight_method='block',
                    background="#1a1b26",
                    this_current_screen_border="#87ceeb", # Light Sky Blue
                    highlight_color=["#1a1b26", "#87ceeb"],
                    inactive="#565f89",
                    active="#ffffff",
                    padding_x=10,
                    margin_x=4,
                    decorations=get_pill("#2e3440")
                ),
                widget.Spacer(),
                extrawidget.Clock(
                    format="󱑂 %b %d  %I:%M %p",
                    decorations=get_pill("#3b4252")
                ),
                widget.Spacer(),
                # Switched to standard widget.Net for stability
                widget.Net(
                    format='󰖩 {down} ↓↑ {up}',
                    prefix='k',
                    decorations=get_pill("#4c566a"),
                    padding=10
                ),
                widget.Systray(padding=5),
                extrawidget.TextBox(
                    text="",
                    foreground="#ff5555",
                    mouse_callbacks={'Button1': lazy.spawn(os.path.expanduser("~/.config/qtile/powermenu.sh"))},
                    decorations=get_pill("#2e3440"),
                    padding=12# Slightly more padding for the power button
                ),
            ],
            24,
            background="#1a1b26", # Solid Opaque
        ),
    ),
]
# --------------------
# Logic & Autostart
# --------------------
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
]

@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser('~')
    
    # Set Resolution & Refresh Rate for eDP-1
    subprocess.Popen(["xrandr", "--output", "eDP-1", "--primary", "--mode", "1366x768", "--rate", "60.00"])
    
    # Set Keyboard repeat rate (makes navigation feel faster/modern)
    subprocess.Popen(["xset", "r", "rate", "300", "50"])

    # Startup Apps
    processes = [
        ["picom", "--config", f"{home}/.config/picom/picom.conf"],
        ["nm-applet"],       # Network icon
        ["volumeicon"],    # Optional: Adds a volume icon to your tray
    ]
    
    for p in processes:
        subprocess.Popen(p)

floating_layout = layout.Floating(float_rules=[*layout.Floating.default_float_rules, Match(title="pinentry")])
auto_fullscreen = True
wmname = "LG3D"

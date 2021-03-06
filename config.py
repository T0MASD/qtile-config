# -*- coding: utf-8 -*-
import os
from libqtile.manager import Key, Click, Drag, Screen
from libqtile.command import lazy
from libqtile import layout, bar, widget
from socket import gethostname
from subprocess import call
from libqtile.widget.crashme import _CrashMe
from libqtile.dgroups import DGroups, Match, simple_key_binder

# Inits
xresources = os.path.expanduser('~/.Xresources')
if os.path.exists(xresources):
    call(['xrdb', '-merge', xresources])

call(['xsetroot', '-cursor_name', 'left_ptr'])

image = os.path.expanduser('~/colorback.jpg')
hostname = gethostname()

mpd_host = ''
layout_variant = ''
if hostname == 'ark':
    mpd_host = 'arkr'
    layout_variant = '"oss, bepo"'

elif hostname == 'arkw':
    mpd_host = 'entrecote'
    layout_variant = '"bepo, oss"'
    call(['xrandr', '--output', 'VGA1', '--mode', '1920x1080'])
    call(['xrandr', '--output', 'HDMI1', '--mode', '1920x1080',
          '--right-of', 'VGA1'])

call(['feh', '--bg-scale', image])

call(['setxkbmap',
      '-layout', '"fr, fr, us"',
      '-variant', layout_variant,
      '-option', '"grp:shifts_toggle"'])

xmodmap = os.path.expanduser('~/.Xmodmap')
if os.path.exists(xmodmap):
    call(['xmodmap', xmodmap])

mpc = 'mpc -h %s ' % mpd_host

mod = 'mod4'
liteblue = '0066FF'
litegreen = '00BB55'
keys = [
    Key([mod, "shift"], "Left", lazy.layout.decrease_ratio()),
    Key([mod, "shift"], "Return", lazy.layout.toggle_split()),
    Key([mod, "shift"], "Right", lazy.layout.increase_ratio()),
    Key([mod, "shift"], "Tab", lazy.layout.previous()),
    Key([mod, "shift"], "j", lazy.spawn("amixer -c 0 -q set Master 2dB-")),
    Key([mod, "shift"], "k", lazy.spawn("amixer -c 0 -q set Master 2dB+")),
    Key([mod, "shift"], "q", lazy.shutdown()),
    Key([mod, "shift"], "p", lazy.pause()),
    Key([mod, "shift"], "space", lazy.layout.rotate()),
    Key([mod], "Left", lazy.group.prevgroup()),
    Key([mod], "Right", lazy.group.nextgroup()),
    Key([mod], "Up", lazy.to_next_screen()),
    Key([mod], "Down", lazy.to_prev_screen()),
    Key([mod], "Tab", lazy.layout.next()),
    Key([mod], "f", lazy.window.toggle_floating()),
    Key([mod], "g", lazy.togroup()),
    Key([mod], "r", lazy.spawncmd()),
    Key([mod], "j", lazy.layout.up()),
    Key([mod], "k", lazy.layout.down()),
    Key([mod], "q", lazy.restart()),
    Key([mod], "l", lazy.spawn(
        'alock -auth pam -bg image:center,file=' + image)),
    Key([mod], "space", lazy.nextlayout()),
    Key([mod], "Return", lazy.spawn('urxvt')),
    Key([mod], "w", lazy.window.kill()),
    Key([mod], "BackSpace", lazy.spawn(
        "dmenu_run -i -b -fn 'monofur:pixelsize=16:antialias=true'"
        " -p 'Run' -nf '#ffffff' -nb '#202020'")),
    Key([mod], "XF86AudioPlay", lazy.spawn(mpc + 'toggle')),
    Key([mod], "XF86AudioPrev", lazy.spawn(mpc + 'prev')),
    Key([mod], "XF86AudioNext", lazy.spawn(mpc + 'next')),
    Key([mod], "XF86AudioStop", lazy.spawn(mpc + 'stop')),
    Key([mod], "XF86AudioLowerVolume", lazy.spawn(mpc + 'volume -2')),
    Key([mod], "XF86AudioRaiseVolume", lazy.spawn(mpc + 'volume +2')),
]

mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
    Click([], "Button8", lazy.group.prevgroup()),
    Click([], "Button9", lazy.group.nextgroup()),
    Click([mod], "Button10", lazy.window.kill())
]

groups = []

fonts = {'font': 'monofur', 'fontsize': 12}
fontcolors = fonts.copy()
green_fontcolors = fonts.copy()
fontcolors['foreground'] = liteblue
green_fontcolors['foreground'] = litegreen
borders = {
    'border_normal': '#000066',
    'border_focus': '#0000FF',
    'border_width': 2 if hostname != 'arkleeenux' else 1
}

layouts = [
    layout.RatioTile(**borders),
    layout.Max(),
    layout.Tile(ratio=0.25, **borders),
    layout.Stack(stacks=2, **borders),
    layout.MonadTall(**borders),
    layout.Zoomy(**borders),
    layout.TreeTab(**fontcolors),
    layout.Slice()
]
floating_layout = layout.Floating(**borders)

top_bar_heigth = 26
bottom_bar_heigth = 18

if hostname == 'arkleeenux':
    fonts['fontsize'] = fontcolors['fontsize'] = 8
    screens = [Screen(
        top=bar.Bar([
            widget.GroupBox(
                borderwidth=1, padding=0, active="0066FF",
                this_current_screen_border='0000ff', **fonts),
            widget.Prompt(**fontcolors),
            widget.WindowName(margin_x=6, **fontcolors),
            widget.Notify(**fontcolors),
            widget.Systray(),
            widget.Battery(
                energy_now_file='charge_now',
                energy_full_file='charge_full',
                power_now_file='current_now',
                charge_char='↑',
                discharge_char='↓',
                **fontcolors),
            widget.CurrentLayout(**fontcolors),
            widget.Clock(
                '%H:%M %d/%m/%y', padding=6, **fontcolors
            )], 14),)]
elif hostname == 'arkr':
    screens = [Screen(
        top=bar.Bar([
            widget.GroupBox(
                borderwidth=2, padding=4, active="0066FF",
                this_current_screen_border='0000ff', **fonts),
            widget.Prompt(**fontcolors),
            widget.WindowName(margin_x=6, **fontcolors),
            widget.Mpd(host='arkr', foreground_progress='00aaff',
                       **fontcolors),
            widget.Notify(**fontcolors),
            widget.Systray(),
            widget.Battery(
                energy_now_file='charge_now',
                energy_full_file='charge_full',
                power_now_file='current_now',
                charge_char='↑',
                discharge_char='↓',
                **fontcolors),
            widget.CurrentLayout(**fontcolors),
            widget.Clock(
                '%H:%M %d/%m/%y', padding=6, **fontcolors
            )], 28),)]
elif os.getenv('DISPLAY') == ':5.0':
    screens = [Screen(
        top=bar.Bar([
            widget.GroupBox(
                borderwidth=2, padding=4, active="0066FF",
                this_screen_border='0066FF.8', **fonts),
            widget.Prompt(**fontcolors),
            widget.WindowName(margin_x=6, **fontcolors),
            widget.Mpd(host='entrecote', foreground_progress='00aaff',
                       **fontcolors),
            _CrashMe(),
            widget.Notify(**fontcolors),
            widget.Systray(),
            widget.CurrentLayout(**fontcolors),
            widget.Clock(
                '%H:%M %d/%m/%y', padding=6, **fontcolors
            )], 28),)]
else:
    screens = [
        Screen(
            top=bar.Bar([
                widget.GroupBox(
                    this_current_screen_border='0000ff',
                    this_screen_border='0000bb',
                    borderwidth=2, padding=4, active=liteblue, **fonts),
                widget.Prompt(**fontcolors),
                widget.WindowName(
                    margin_x=6, **fontcolors),
                widget.Systray(),
               widget.Mpd(host='entrecote', foreground_progress='00aaff',
                          **fontcolors),
                widget.CurrentLayout(**fontcolors)
            ], top_bar_heigth)
        ),
        Screen(
            top=bar.Bar([
                widget.GroupBox(
                    this_current_screen_border='00ff00',
                    this_screen_border='00bb00',
                    borderwidth=2,
                    padding=4, active=litegreen, **fonts),
                widget.Prompt(),
                widget.WindowName(
                    margin_x=6, **green_fontcolors),
                widget.Notify(foreground_low='009900', **green_fontcolors),
                widget.Clock(
                    '%H:%M %d/%m/%y', padding=6, **green_fontcolors),
                widget.CurrentLayout(**green_fontcolors)
            ], top_bar_heigth)
        )
    ]

# change focus on mouse over
follow_mouse_focus = True


def main(qtile):
    groups = {
        'term': {'init': True,
                 'persist': True,
                 'layout': 'ratiotile',
                 'spawn': 'urxvt',
                 'exclusive': True},
        'www': {'init': True,
                'exclusive': True,
                'spawn': 'chromium'
            },
        'emacs': {'persist': True,
                  'spawn': 'emacs',
                  'exclusive': True},
    }

    apps = [
        {'match': Match(
            wm_type=['dialog', 'utility', 'splash']),
         'float': True},
        {'match': Match(
            wm_class=['Chromium', 'Chromium-browser', 'Chrome', 'Minefield'],
            role=['browser']),
         'group': 'www'},
        {'match': Match(title=['Developer Tools']),
         'group': 'www-inspector'},
        {'match': Match(wm_class=['URxvt']),
         'group': 'term'},
        {'match': Match(wm_class=['Emacs']),
         'group': 'emacs'}
    ]
    DGroups(qtile, groups, apps, simple_key_binder(mod))

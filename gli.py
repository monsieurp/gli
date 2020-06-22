#!/usr/bin/env python3
import urwid
import sys


class Intro:
    palette = [
        ('titlebar', 'white,bold', 'dark green'),
        ('intro', 'white', 'dark blue'),
        ('filler', 'white', 'dark blue'),
        ('focus', 'white', 'dark blue'),
        ('selectable', 'black', 'dark green')
    ]

    text = """Welcome to the Gentoo Linux Installer!

GLI simplifies the installation of Gentoo Linux as described
in the Gentoo Linux handbook.

See https://wiki.gentoo.org/wiki/Handbook for further information.

Would you like to begin the installation with GLI?"""

    def returncode(self, bt):
        sys.exit(bt.rc)

    def main(self):
        self.header = urwid.Text('GLI - Gentoo Linux Installer')
        self.header = urwid.AttrMap(self.header, 'titlebar')

        self.intro = urwid.Text(self.text)
        self.intro = urwid.AttrMap(self.intro, 'intro')

        self.yes = urwid.Button('Yes', self.returncode)
        self.yes.rc = 0
        self.yes = urwid.AttrMap(self.yes, 'focus', 'selectable')

        self.no = urwid.Button('No', self.returncode)
        self.no.rc = 1
        self.no = urwid.AttrMap(self.no, 'focus', 'selectable')

        self.buttons = [self.yes, self.no]
        self.buttons = urwid.GridFlow(self.buttons, 10, 3, 1, 'center')

        self.intro = urwid.Pile([self.intro, urwid.Divider(), self.buttons], focus_item=2)
        self.intro = urwid.Filler(self.intro, valign='top', top=1, bottom=1)
        self.intro = urwid.AttrMap(self.intro, 'filler')

        self.sfill = urwid.AttrMap(urwid.SolidFill(' '), 'filler')

        self.intro = urwid.LineBox(self.intro)
        self.intro = urwid.AttrMap(self.intro, 'filler')
        self.intro = urwid.Overlay(self.intro, self.sfill,
            align='center', valign='middle',
            width=('relative', 60), height=('relative', 40))

        self.layout = urwid.Frame(header=self.header, body=self.intro)
        self.main = urwid.MainLoop(self.layout, self.palette)
        self.main.run()


if __name__ == '__main__':
    Intro().main()

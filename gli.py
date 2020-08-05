#!/usr/bin/env python3
import subprocess
import shlex
import urwid
import gli
import gli.dialogs

from gli.dialogs import IntroDialog
from gli import *


class GLI(urwid.WidgetPlaceholder):
    header = urwid.AttrMap(
        urwid.Text('GLI - Gentoo Linux Installer', align='center'),
        'header'
    )
    footer = urwid.AttrMap(
        urwid.Text('[ctrl+q] Quit GLI or restart from here.', align='left'),
        'footer'
    )

    def __init__(self):
        self.dialog = IntroDialog(self)

        super(GLI, self).__init__(
            urwid.Frame(
                header=self.header,
                body=self.dialog._w,
                footer=self.footer
            )
        )

        self.loop = urwid.MainLoop(
            self, PALETTE,
            unhandled_input=self.my_keypress
        )
        screen = urwid.raw_display.Screen()
        try:
            old = screen.tty_signal_keys('undefined','undefined',
                    'undefined','undefined','undefined')
            self.loop.run()
        finally:
            screen.tty_signal_keys(*old)


    def switch_dialog(self, dialog):
        self.dialog = dialog
        self.draw_dialog()

    def draw_dialog(self):
        foot = self.footer
        if hasattr(self.dialog, 'footer'):
            foot = urwid.AttrMap(
                urwid.Text(self.dialog.footer, align='left'),
                'footer'
            )

        self.original_widget = urwid.Frame(
            header=self.header,
            body=self.dialog._w,
            footer=foot
        )

    def quit_popup(self, text=['']):
        body_text = urwid.Text(text, align='center')
        body_filler = urwid.Filler(body_text, valign='middle')
        body_padding = urwid.Padding(
            body_filler,
            left=1,
            right=1
        )

        body = urwid.AttrMap(urwid.LineBox(body_padding), 'exit')

        cont = urwid.Button('Continue', self.choice)
        cont = urwid.AttrWrap(cont, 'efoc', 'esel')

        quit = urwid.Button('Quit', self.choice)
        quit = urwid.AttrWrap(quit, 'efoc', 'esel')

        rs = urwid.Button('Restart', self.choice)
        rs = urwid.AttrWrap(rs, 'efoc', 'esel')

        footer = urwid.GridFlow([cont, quit, rs], 12, 1, 22, 'center')

        layout = urwid.Frame(
            body,
            footer=footer,
            focus_part='footer'
        )

        w = urwid.Overlay(
            layout,
            self,
            align='center',
            width=40,
            valign='middle',
            height=10
        )
        w = urwid.AttrMap(w, 'exit')

        self.loop.widget = w

    def choice(self, button):
        if button.label == 'Continue':
            self.loop.widget = self
            self.loop.draw_screen()
        elif button.label == 'Quit':
            raise urwid.ExitMainLoop()
        elif button.label == 'Restart':
            self.switch_dialog(IntroDialog(self))
            self.loop.widget = self
            self.loop.draw_screen()

    def my_keypress(self, key):
        if key == 'ctrl q':
            self.quit_popup(
                [
                    'You\'ve hit ctrl+q!\n\n',
                    'What do you want to do?'
                ]
            )


if __name__ == '__main__':
    GLI()

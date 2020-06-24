#!/usr/bin/env python3
import urwid


PALETTE = [
    ('titlebar',    'black',    'dark blue'),
    ('fruit',       'white',    'dark blue'),
    ('bgcolor',     'black',    'dark blue'),
    ('selectable',  'white',    'light cyan'),
    ('focus',       'black',    'light cyan'),
    ('exit',        'white',    'dark cyan')
]


class IntroDialog(urwid.WidgetWrap):
    dialog_text = """Welcome to the Gentoo Linux Installer!

GLI simplifies the installation of Gentoo Linux as described
in the Gentoo Linux handbook.

See https://wiki.gentoo.org/wiki/Handbook for further information.

Would you like to begin the installation with GLI?"""

    def __init__(self):
        self.header = urwid.AttrMap(
            urwid.Text('GLI - Gentoo Linux Installer'),
            'titlebar'
        )

        content_frame = urwid.Frame(body=None)

        yes = urwid.AttrMap(urwid.Button('Yes'), 'focus', 'selectable')
        yes.rc = 0

        no = urwid.AttrMap(urwid.Button('No'), 'focus', 'selectable')
        no.rc = 1

        buttons = urwid.GridFlow([yes, no], 10, 3, 1, 'center')

        content = urwid.Text(self.dialog_text)
        content = urwid.Padding(content,
            align='center', width='pack'
        )
        content = urwid.Pile([content, urwid.Divider(), buttons], focus_item=2)
        content = urwid.AttrMap(urwid.Filler(content, valign='middle', top=0,
            bottom=0), 'bgcolor')
        content = urwid.AttrMap(urwid.LineBox(content), 'bgcolor')
        content = urwid.Overlay(
            content,
            urwid.AttrMap(urwid.SolidFill('\N{LIGHT SHADE}'), 'bgcolor'),
            align='center', valign='middle',
            width=('relative', 60),
            height=('relative', 40)
        )
        content_frame.body = content

        self._w = content_frame


class GLI(urwid.WidgetPlaceholder):
    def __init__(self, dialog):
        super(GLI, self).__init__(
            urwid.Frame(
                body=dialog._w,
                header=dialog.header
            )
        )

    def cycle_dialog(self, dialog):
        self.original_widget = urwid.Frame(
            body=dialog._w,
            header=dialog.header
        )


class Main:
    def __init__(self):
        self.view = GLI(IntroDialog())
        self.loop = urwid.MainLoop(self.view, PALETTE,
            unhandled_input=self.unhandled_input)
        self.loop.run()

    def unhandled_input(self, key):
        if key == 'f8':
            raise urwid.ExitMainLoop()


if __name__ == '__main__':
    Main()

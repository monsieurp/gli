#!/usr/bin/env python3
import urwid


PALETTE = [
    ('header',      'white',    'dark blue'),
    ('footer',      'white',    'black'),
    ('bgcolor',     'black',    'dark blue'),
    ('wcolor',      'black',    'light gray'),
    ('selectable',  'white',    'dark blue'),
    ('focus',       'black',    'dark blue'),
    ('esel',        'white',    'dark red'),
    ('efoc',        'black',    'dark red'),
    ('exit',        'white',    'dark red')
]


SFILL = '▞'


class IntroDialog(urwid.WidgetWrap):
    dialog_text = """Welcome to the Gentoo Linux Installer!

GLI simplifies the installation of Gentoo Linux as described
in the Gentoo Linux handbook.

See https://wiki.gentoo.org/wiki/Handbook for further information.

Would you like to begin the installation with GLI?"""

    def __init__(self, gli_widget):
        self.gli_widget = gli_widget

        content_frame = urwid.Frame(body=None)

        yes = urwid.AttrMap(urwid.Button('Yes', self.handle_input), 'focus', 'selectable')
        no = urwid.AttrMap(urwid.Button('No', self.handle_input), 'focus', 'selectable')

        buttons = urwid.GridFlow([yes, no], 10, 3, 1, 'center')

        content = urwid.Text(self.dialog_text)
        content = urwid.Padding(content,
            align='center', width='pack'
        )
        content = urwid.Pile([content, urwid.Divider(), buttons], focus_item=2)
        content = urwid.AttrMap(urwid.Filler(content, valign='middle', top=0,
            bottom=0), 'wcolor')
        content = urwid.AttrMap(urwid.LineBox(content), 'wcolor')
        content = urwid.Overlay(
            content,
            urwid.AttrMap(urwid.SolidFill(SFILL), 'bgcolor'),
            align='center', valign='middle',
            width=('relative', 60),
            height=('relative', 40)
        )
        content_frame.body = content

        self._w = content_frame

    def handle_input(self, button):
        if button.label == "Yes":
            self.gli_widget.cycle_dialog(SSHDialog(self.gli_widget))
        elif button.label == "No":
            raise urwid.ExitMainLoop()


class SSHDialog(urwid.WidgetWrap):
    dialog_text = """Would you like to start the SSH daemon?

sshd can be started to grant users access
to this machine during the installation."""

    footer = 'Yes: launch command "rc-service sshd start" in background. \
No: skip.'

    def __init__(self, gli_widget):
        self.gli_widget = gli_widget

        content_frame = urwid.Frame(body=None)

        yes = urwid.AttrMap(urwid.Button('Yes', self.handle_input), 'focus', 'selectable')
        no = urwid.AttrMap(urwid.Button('No', self.handle_input), 'focus', 'selectable')

        buttons = urwid.GridFlow([no, yes], 10, 3, 1, 'center')

        content = urwid.Text(self.dialog_text)
        content = urwid.Padding(content,
            align='center', width='pack'
        )
        content = urwid.Pile([content, urwid.Divider(), buttons], focus_item=2)
        content = urwid.AttrMap(urwid.Filler(content, valign='middle', top=0,
            bottom=0), 'wcolor')
        content = urwid.AttrMap(urwid.LineBox(content), 'wcolor')
        content = urwid.Overlay(
            content,
            urwid.AttrMap(urwid.SolidFill(SFILL), 'bgcolor'),
            align='center', valign='middle',
            width=('relative', 40),
            height=('relative', 30)
        )
        content_frame.body = content

        self._w = content_frame

    def handle_input(self, button):
        if button.label == "Yes":
            # TODO: run "rc-service sshd start".
            raise urwid.ExitMainLoop()
        elif button.label == "No":
            # TODO: move to next dialog.
            self.gli_widget.cycle_dialog(IntroDialog(self.gli_widget))


class GLI(urwid.WidgetPlaceholder):
    header = urwid.AttrMap(
        urwid.Text('GLI - Gentoo Linux Installer', align='center'),
        'header'
    )
    footer = urwid.AttrMap(
        urwid.Text('Press ESC/Q to quit GLI.', align='left'),
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
            unhandled_input=self.handle_input
        )
        self.loop.run()

    def cycle_dialog(self, dialog):
        self.dialog = dialog

        if hasattr(self.dialog, 'footer'):
            foot = urwid.AttrMap(
                urwid.Text(self.dialog.footer, align='left'),
                'footer'
            )
        else:
            foot = self.footer

        self.original_widget = urwid.Frame(
            header=self.header,
            body=self.dialog._w,
            footer=foot
        )

    def quit_popup(self, text = ['']):
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
            self.cycle_dialog(IntroDialog(self))
            self.loop.widget = self
            self.loop.draw_screen()

    def handle_input(self, key):
        if key in ('esc', 'ESC', 'q', 'Q'):
            self.quit_popup(
                [
                    'You\'ve hit the ESC key/Q!\n\n',
                    'What do you want to do?'
                ]
            )


if __name__ == '__main__':
    GLI()

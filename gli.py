#!/usr/bin/env python3
import subprocess
import shlex
import urwid


PALETTE = [
    ('header', 'white', 'black'),
    ('footer', 'white', 'black'),
    ('bgcolor', 'black', 'dark blue'),
    ('wcolor', 'black', 'light gray'),
    ('selectable', 'white', 'dark blue'),
    ('focus', 'light gray', 'dark blue'),
    ('esel', 'white', 'dark red'),
    ('efoc', 'black', 'dark red'),
    ('exit', 'white', 'dark red')
]


SFILL = '▞'


class IntroDialog(urwid.WidgetWrap):
    text = """Welcome to the Gentoo Linux Installer!

GLI simplifies the installation of Gentoo Linux as described in the Gentoo Linux handbook.

See https://wiki.gentoo.org/wiki/Handbook for further information.

Would you like to begin the installation with GLI?"""

    def __init__(self, top_widget, *args, **kw):
        super(IntroDialog, self).__init__(top_widget, *args, **kw)
        self.top_widget = top_widget

        # Store user choices made throughout the installer.
        # Initialise this value here in case the user restarts GLI.
        self.top_widget.user_choices = {}

        content_frame = urwid.Frame(body=None)

        top = urwid.Text(self.text)
        top = urwid.Padding(top, align='left', width='pack')
        top = urwid.AttrMap(urwid.Filler(top, valign='top'), 'wcolor')

        yes = urwid.AttrMap(
            urwid.Button(
                'Yes',
                self.handle_input),
            'focus',
            'selectable')
        no = urwid.AttrMap(
            urwid.Button(
                'No',
                self.handle_input),
            'focus',
            'selectable')

        buttons = urwid.GridFlow([yes, no], 10, 3, 1, 'center')

        bottom = urwid.Padding(buttons, align='right', width='pack' )
        bottom = urwid.AttrMap(urwid.Filler(bottom, valign='bottom'), 'wcolor')

        content = urwid.Pile([top, bottom], focus_item=1)
        content = urwid.AttrMap(urwid.LineBox(content), 'wcolor')

        content = urwid.Overlay(
            content,
            urwid.AttrMap(urwid.SolidFill(SFILL), 'bgcolor'),
            align='center', valign='middle',
            width=60,
            height=20
        )
        content_frame.body = content

        self._w = content_frame

    def handle_input(self, button):
        if button.label == "Yes":
            self.top_widget.switch_dialog(SSHDialog(self.top_widget))
        elif button.label == "No":
            raise urwid.ExitMainLoop()


class SSHDialog(urwid.WidgetWrap):
    text = """Would you like to start the SSH daemon?

sshd can be started to grant users access
to this machine during the installation."""
    footer = """Yes: launch command "rc-service sshd start" in background.
No: skip this step."""

    def __init__(self, top_widget, *args, **kw):
        super(SSHDialog, self).__init__(top_widget, *args, **kw)
        self.top_widget = top_widget

        content_frame = urwid.Frame(body=None)

        top = urwid.Text(self.text)
        top = urwid.Padding(top, align='left', width='pack')
        top = urwid.AttrMap(urwid.Filler(top, valign='top'), 'wcolor')

        yes = urwid.AttrMap(
            urwid.Button(
                'Yes',
                self.handle_input),
            'focus',
            'selectable')
        no = urwid.AttrMap(
            urwid.Button(
                'No',
                self.handle_input),
            'focus',
            'selectable')

        buttons = urwid.GridFlow([no, yes], 10, 3, 1, 'center')

        bottom = urwid.Padding(buttons, align='right', width='pack' )
        bottom = urwid.AttrMap(urwid.Filler(bottom, valign='bottom'), 'wcolor')

        content = urwid.Pile([top, bottom], focus_item=1)
        content = urwid.AttrMap(urwid.LineBox(content), 'wcolor')

        content = urwid.Overlay(
            content,
            urwid.AttrMap(urwid.SolidFill(SFILL), 'bgcolor'),
            align='center', valign='middle',
            width=50,
            height=10
        )
        content_frame.body = content

        self._w = content_frame

    def handle_input(self, button):
        if button.label == "Yes":
            self.top_widget.user_choices['start_sshd'] = 'yes'
            raise urwid.ExitMainLoop()
        elif button.label == "No":
            self.top_widget.user_choices['start_sshd'] = 'no'
            self.top_widget.switch_dialog(DiskSelectionDialog(self.top_widget))


class DiskSelectionDialog(urwid.WidgetWrap):
    text = 'Please select a disk to partition'
    footer = '[R/r] Detect disks again.'

    def __init__(self, top_widget, *args, **kw):
        super(DiskSelectionDialog, self).__init__(top_widget, *args, **kw)
        self.top_widget = top_widget
        self.detect_disks()
        self.draw()

    def draw(self):
        content_frame = urwid.Frame(body=None)

        ok = urwid.AttrMap(
            urwid.Button(
                'OK',
                self.handle_input),
            'focus',
            'selectable')

        ok = urwid.GridFlow([ok], 10, 3, 1, 'center')

        rbgroup = []
        buttons = [
            urwid.AttrMap(
                urwid.RadioButton(rbgroup, d),
                'focus', 'selectable'
            ) for d in self.disks
        ]
        self.rbuttons = buttons

        buttons = urwid.Pile(buttons, focus_item=0)

        content = urwid.Text(self.text)
        content = urwid.Padding(content,
                                align='center', width='pack'
                                )

        content = urwid.Pile(
            [content, urwid.Divider(), buttons, urwid.Divider(), ok],
            focus_item=2)
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
        if button.label == "OK":
            for rbutton in self.rbuttons:
                _rbutton = rbutton.base_widget
                if _rbutton.get_state():
                    label = _rbutton.get_label().split(' ¬ ')[0]
                    self.top_widget.user_choices['disk'] = label
                    self.top_widget.switch_dialog(
                        DiskPartitioningMethodDialog(self.top_widget)
                    )

    def detect_disks(self):
        self.disks = []
        lsblk = shlex.split('lsblk -r -n -i -o KNAME,TYPE,SIZE,MODEL')
        process = subprocess.Popen(lsblk, stdout=subprocess.PIPE)
        stdout = process.communicate()[0].decode('utf-8').split('\n')
        disks = [line for line in stdout if 'disk' in line]
        for disk in disks:
            name, _, size, model = disk.split(' ')
            name = '/dev/' + name
            model = model.replace('\\x20', ' ')
            self.disks.append(f'{name} ¬ {model} ¬ {size}')

    def my_keypress(self, key):
        if key in ('R', 'r'):
            # Detect disks again.
            self.detect_disks()
            # Update dialog with (maybe) newly detected disks.
            self.draw()
            # Redraw dialog.
            self.top_widget.draw_dialog()


class DiskPartitioningMethodDialog(urwid.WidgetWrap):
    class ToolTipPile(urwid.Pile):
        def __init__(self, buttons, dialog, *args, **kw):
            super().__init__(buttons, **kw)
            self.dialog = dialog
            self.dialog.idx = self.focus_position

            self.set_tooltip_text(
                self.dialog.footer_infotip_text[self.dialog.idx]
            )

        def set_tooltip_text(self, text):
            self.dialog.top_widget.original_widget.footer.base_widget.set_text(
                text
            )

        def keypress(self, size, key):
            if key in ('up', 'down'):
                if key == 'up':
                    self.dialog.idx -= 1
                elif key == 'down':
                    self.dialog.idx += 1

                if self.dialog.idx > 4:
                    tooltip = 'Validate your choice.'
                elif self.dialog.idx < 0:
                    self.dialog.idx = 0

                if self.dialog.idx >= 0 and self.dialog.idx <= 4:
                    tooltip = self.dialog.footer_infotip_text[self.dialog.idx]

                self.set_tooltip_text(tooltip)
            return super().keypress(size, key)

    class ToolTipOkButton(urwid.Button):
        def __init__(self, label, dialog, *args, **kw):
            super().__init__(label, *args, **kw)
            self.dialog = dialog

        def set_tooltip_text(self, text):
            self.dialog.top_widget.original_widget.footer.base_widget.set_text(
                text
            )

        def keypress(self, size, key):
            if key == 'up':
                self.dialog.idx -= 1
                tooltip = self.dialog.footer_infotip_text[self.dialog.idx]
                self.set_tooltip_text(tooltip)

            return super().keypress(size, key)

    text = 'Please select a partitioning method'
    footer_infotip_label = [
        'Guided(ext4)',
        'Guided(XFS)',
        'Guided(JFS)',
        'Manual',
        'Shell'
    ]
    footer_infotip_text = [
        'Guided disk partitioning using ext4.',
        'Guided disk partitioning using XFS.',
        'Guided disk partitioning using JFS.',
        'Manual disk partitioning with GLI.',
        'Open a shell.'
    ]
    idx = 0
    footer = footer_infotip_text[idx]

    def __init__(self, top_widget, *args, **kw):
        super(DiskPartitioningMethodDialog, self).__init__(
                top_widget, *args, **kw
        )
        self.top_widget = top_widget
        self.draw()

    def draw(self):
        content_frame = urwid.Frame(body=None)

        ok = urwid.AttrMap(
            DiskPartitioningMethodDialog.ToolTipOkButton(
                'OK',
                self,
                self.handle_input),
            'focus',
            'selectable')

        ok = urwid.GridFlow([ok], 10, 3, 1, 'center')

        rbgroup = []
        buttons = [
            urwid.AttrMap(
                urwid.RadioButton(rbgroup, d),
                'focus', 'selectable'
            ) for d in self.footer_infotip_label
        ]
        self.rbuttons = buttons

        buttons = DiskPartitioningMethodDialog.ToolTipPile(
            buttons, self, focus_item=0
        )

        content = urwid.Text(self.text)
        content = urwid.Padding(content,
                                align='center', width='pack'
                                )

        content = urwid.Pile(
            [content, urwid.Divider(), buttons, urwid.Divider(), ok],
            focus_item=2)
        content = urwid.AttrMap(urwid.Filler(content, valign='middle', top=0,
                                             bottom=0), 'wcolor')
        content = urwid.AttrMap(urwid.LineBox(content), 'wcolor')

        content = urwid.Overlay(
            content,
            urwid.AttrMap(urwid.SolidFill(SFILL), 'bgcolor'),
            align='center', valign='middle',
            width=('relative', 40),
            height=('relative', 40)
        )

        content_frame.body = content
        self._w = content_frame

    def handle_input(self, button):
        if button.label == "OK":
            for rbutton in self.rbuttons:
                _rbutton = rbutton.base_widget
                if _rbutton.get_state():
                    label = _rbutton.get_label()
                    self.top_widget.user_choices['pmethod'] = label
                    import sys
                    sys.exit(self.top_widget.user_choices)


class GLI(urwid.WidgetPlaceholder):
    header = urwid.AttrMap(
        urwid.Text('GLI - Gentoo Linux Installer', align='center'),
        'header'
    )
    footer = urwid.AttrMap(
        urwid.Text('[ESC/Q] Quit GLI or restart from here.', align='left'),
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
        self.loop.run()

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
        # Pass off key management to current dialog if it wishes.
        if hasattr(self.dialog, 'my_keypress'):
            self.dialog.my_keypress(key)

        if key in ('esc', 'ESC', 'q', 'Q'):
            self.quit_popup(
                [
                    'You\'ve hit the ESC key/Q!\n\n',
                    'What do you want to do?'
                ]
            )


if __name__ == '__main__':
    GLI()

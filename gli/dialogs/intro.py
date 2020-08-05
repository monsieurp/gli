import urwid
import gli.dialogs
import gli


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
            urwid.AttrMap(urwid.SolidFill(gli.SFILL), 'bgcolor'),
            align='center', valign='middle',
            width=60,
            height=20
        )
        content_frame.body = content

        self._w = content_frame

    def handle_input(self, button):
        if button.label == "Yes":
            self.top_widget.switch_dialog(gli.dialogs.SSHDialog(self.top_widget))
        elif button.label == "No":
            raise urwid.ExitMainLoop()

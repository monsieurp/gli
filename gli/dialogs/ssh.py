import urwid
import gli.dialogs
import gli


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
            urwid.AttrMap(urwid.SolidFill(gli.SFILL), 'bgcolor'),
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
            self.top_widget.switch_dialog(gli.dialogs.DiskSelectionDialog(self.top_widget))

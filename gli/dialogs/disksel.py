import subprocess
import urwid
import shlex
import gli.dialogs
import gli


class DiskSelectionDialog(urwid.WidgetWrap):
    class TabPile(urwid.Pile):
        def __init__(self, buttons, dialog, *args, **kw):
            super().__init__(buttons, **kw)
            self.dialog = dialog
            self.remember_focus = self.focus_position

        def keypress(self, size, key):
            if key == 'tab':
                if self.focus_position == len(self.contents) - 1:
                    self.focus_position = self.remember_focus
                else:
                    self.focus_position = len(self.contents) - 1
            if key == 'ctrl r':
                # Detect disks again.
                self.dialog.detect_disks()
                # Update dialog with (maybe) newly detected disks.
                self.dialog.draw()
                # Redraw dialog.
                self.dialog.top_widget.draw_dialog()
            return super().keypress(size, key)

    text = 'Please select a disk to partition:'
    footer = '[ctrl+r] Detect disks again.'

    def __init__(self, top_widget, *args, **kw):
        super(DiskSelectionDialog, self).__init__(top_widget, *args, **kw)
        self.top_widget = top_widget
        self.detect_disks()
        self.draw()

    def draw(self):
        content_frame = urwid.Frame(body=None)

        top = urwid.Text(self.text)
        top = urwid.Padding(top, align='left', width='pack')
        top = urwid.AttrMap(urwid.Filler(top, valign='top'), 'wcolor')

        rbgroup = []
        buttons = [
            urwid.AttrMap(
                urwid.RadioButton(rbgroup, d),
                'focus', 'selectable'
            ) for d in self.disks
        ]
        self.rbuttons = buttons
        buttons = urwid.Pile(buttons, focus_item=0)
        buttons = urwid.Padding(buttons, align='left', width='pack')
        buttons = urwid.AttrMap(urwid.Filler(buttons, valign='top'), 'wcolor')

        ok = urwid.AttrMap(
            urwid.Button(
                'OK',
                self.handle_input),
            'focus',
            'selectable')

        ok = urwid.GridFlow([ok], 10, 3, 1, 'center')

        bottom = urwid.Padding(ok, align='left', width='pack')
        bottom = urwid.AttrMap(urwid.Filler(bottom, valign='bottom'), 'wcolor')

        content = DiskSelectionDialog.TabPile([top, buttons, bottom], self, focus_item=1)
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
        if button.label == "OK":
            for rbutton in self.rbuttons:
                _rbutton = rbutton.base_widget
                if _rbutton.get_state():
                    label = _rbutton.get_label().split(' ¬ ')[0]
                    self.top_widget.user_choices['disk'] = label
                    self.top_widget.switch_dialog(
                        gli.dialogs.DiskPartitioningMethodDialog(self.top_widget)
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

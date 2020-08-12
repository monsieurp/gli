import urwid
import sys
import gli


class DiskPartitioningMethodDialog(urwid.WidgetWrap):
    class TabPile(urwid.Pile):
        def __init__(self, buttons, *args, **kw):
            super().__init__(buttons, **kw)
            self.remember_focus = self.focus_position

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

    text = 'Please select a partitioning method:'
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

        top = urwid.Text(self.text)
        top = urwid.Padding(top, align='left', width='pack')
        top = urwid.AttrMap(urwid.Filler(top, valign='top'), 'wcolor')

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
        buttons = urwid.Padding(buttons, align='left', width='pack')
        buttons = urwid.AttrMap(urwid.Filler(buttons, valign='top'), 'wcolor')

        ok = urwid.AttrMap(
            DiskPartitioningMethodDialog.ToolTipOkButton(
                'OK',
                self,
                self.handle_input),
            'focus',
            'selectable')
        ok = urwid.GridFlow([ok], 10, 3, 1, 'center')

        bottom = urwid.Padding(ok, align='left', width='pack')
        bottom = urwid.AttrMap(urwid.Filler(bottom, valign='bottom'), 'wcolor')

        content = DiskPartitioningMethodDialog.TabPile([top, buttons, bottom],
                focus_item=1)
        content = urwid.AttrMap(urwid.LineBox(content), 'wcolor')

        content = urwid.Overlay(
            content,
            urwid.AttrMap(urwid.SolidFill(gli.SFILL), 'bgcolor'),
            align='center', valign='middle',
            width=50,
            height=15
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

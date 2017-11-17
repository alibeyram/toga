from .base import Widget


class Table(Widget):
    def create(self):
        self._action('create Table')

    def change_source(self, source):
        self._action('change source', source=source)

    def insert(self, item):
        self._action('insert row', item=item)

    def change(self, item):
        self._action('change row', item=item)

    def remove(self, item):
        self._action('remove row', item=item)

    def clear(self):
        self._action('clear')

    def set_on_select(self, handler):
        self._set_value('on_select', handler)

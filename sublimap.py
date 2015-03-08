import sublime, sublime_plugin
import time
import datetime

def log_error(ex, command):
    error_msg = 'Error in ' + command + ': ' + str(ex)
    print error_msg
    sublime.status_message(error_msg)

class SubliMapCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.edit = edit
        self.view.window().show_input_panel('Map lambda t, i:', '', self.map_text, None, None)

    def map_text(self, inp):
        try:
            edit = self.view.begin_edit()
            replacer = eval('lambda t, i: str(' + inp + ')')
            for idx, region in enumerate(self.view.sel()):
                txt = self.view.substr(region)
                replacement = replacer(txt, idx)
                self.view.replace(self.edit, region, replacement)
        except Exception as e:
            log_error(e, 'SubliMap')
        finally:
            self.view.end_edit(edit)

class SubliReduceCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.edit = edit
        self.view.window().show_input_panel('Reduce lambda x, y:', '', self.reduce_text, None, None)

    def reduce_text(self, inp):
        try:
            edit = self.view.begin_edit()
            reducer = eval('lambda x, y: ' + inp)
            result = reduce(reducer, map(lambda x: self.view.substr(x), self.view.sel()))
            sublime.status_message("Result: " + str(result))
            map(lambda x: self.view.erase(edit, x), self.view.sel())
            self.view.replace(edit, self.view.sel()[0], str(result))
        except Exception as e:
            log_error(e, 'SubliReduce')
        finally:
            self.view.end_edit(edit)
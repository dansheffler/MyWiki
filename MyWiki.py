import sublime, sublime_plugin, os, re, subprocess



class FollowWikiLinkCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        settings = sublime.load_settings('MyWiki.sublime-settings')
        directory = settings.get('wiki_directory')
        directory = os.path.expanduser(directory)
        extension = settings.get('wiki_extension')
        window = self.view.window()

        oldLocation = self.view.sel()[0]
        self.view.run_command("bracketeer_select")
        location = self.view.sel()[0]
        selected_text = self.view.substr(location)
        self.view.sel().clear()
        self.view.sel().add(oldLocation)

        the_file = directory+selected_text+extension


        if os.path.exists(the_file):
            #open the already-created page.
            new_view = window.open_file(the_file)

        else:
            #create the file then open it.
            open(the_file, "a")
            new_view = window.open_file(the_file)

       




class GetWikiLinkCommand(sublime_plugin.TextCommand):
    def on_done(self, selection):
        if selection == -1:
            self.view.run_command(
                "insert_wiki_link", {"args":
                {'text': '[['}})
            return
        self.view.run_command(
            "insert_wiki_link", {"args":
            {'text': '[['+self.modified_files[selection]+']]'}})

    def run(self, edit):
        settings = sublime.load_settings('MyWiki.sublime-settings')
        directory = settings.get('wiki_directory')
        directory = os.path.expanduser(directory)
        extension = settings.get('wiki_extension')

        self.outputText = '[['
        self.files = os.listdir(directory)
        self.modified_files = [item.replace(extension,"") for item in self.files]
        self.view.window().show_quick_panel(self.modified_files, self.on_done)



class InsertWikiLinkCommand(sublime_plugin.TextCommand):
    def run(self, edit, args):
        self.view.insert(edit, self.view.sel()[0].begin(), args['text'])


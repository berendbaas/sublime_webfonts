import sublime, sublime_plugin
import threading, urllib, json, re

API_url = 'https://www.googleapis.com/webfonts/v1/webfonts?key='
style_url = 'http://fonts.googleapis.com/css?family='

class merge_fontsCommand(sublime_plugin.TextCommand):

  def run(self, edit):
		window = sublime.active_window()
		self.tags = self.find_tags()
		print self.tags

	def find_tags(self):
		"""
		Finds the link tags inside the <head> that reference fonts.googleapis.com
		"""
		linklist = []
		regex = ''
		sublime.View.find_all(regex, sublime.IGNORECASE, linklist)
		pass

	def find_fonts(self, tags):
		"""
		Finds the fonts that are embedded in the <link> tags and their referencing Weights
		output format { 'FontFamily':['weight', 'weight']}
		"""
		pass

	def merge(self, fontlist):
		"""
		Makes a new <link> tag out of the requested fontslist and removes the other -now outdated- <link> tags
		"""
		pass


class fetch_fontsCommand(sublime_plugin.TextCommand):

	def load_settings(self):
		self.settings_file = '%s.sublime-settings' % __name__
		self.settings = sublime.load_settings(self.settings_file)
		pass

	def run(self, edit):
		self.load_settings()
		window = sublime.active_window()
		thread = fetchfontsApiCall(window, self.settings)
		addfont = insertfont()
		thread.start()
		self.handle_thread(thread)

	def handle_thread(self, thread, i=0, dir=1):
		keep_alive = False
		if thread.is_alive():
			keep_alive = True

		if keep_alive:
			before = i % 8
			after = (7) - before
			if not after:
				dir = -1
			if not before:
				dir = 1
			i += dir
			self.view.set_status('fetchfonts', 'Fetching font list [%s=%s]' % (' ' * before, ' ' * after))
			sublime.set_timeout(lambda: self.handle_thread( thread, i, dir), 100)
			return

		self.fonts = thread.fonts
		window = sublime.active_window()
		window.show_quick_panel(self.fonts, self.insert)

	def insert(self, picked):
		if picked == -1:
			return
		command = self.fonts[picked][2]

		match = re.search('ADD F:([\w -]+)&W:([\w, -]+)', command)
		font = match.group(1)
		font =  re.sub('\s', '+', font)
		styles = match.group(2)
		prefix = '<link rel="stylesheet" type="text/css" href="'
		affix =  '" />'
		line = prefix + style_url + font + ':' + styles + affix

		sel = self.view.sel()[0].begin()
		edit = self.view.begin_edit()
		self.view.insert(edit, sel, line)
		self.view.end_edit(edit)





class fetchfontsApiCall(threading.Thread):
	"""
	Class that functions as a thread. Is called for the fetching of the Webfonts list.
	"""

	def __init__(self, window, settings): 
		self.window = window
		self.settings = settings
		self.API_key = self.settings.get('API_key', None)
		self.script = self.settings.get('script', 'latin')
		threading.Thread.__init__(self)

	def run(self):
		"""
		Called by the main class. 
		Fetches the fonts from the specified URL with the API key defined in the settings.
		"""
		if self.API_key == None:
			self.view.set_status('fetchfonts', 'Missing Api key in the configuration file:' + __name__ + '.sublime-settings')
			return

		url = API_url + self.API_key
		fontslist = urllib.urlopen(url)
		decodedlist = json.load(fontslist)
		self.fonts = self.associate(decodedlist)
		return

	def associate(self, fontslist):
		"""
		Takes the JSON list fetched from the uri and parses it into an list readable for sublimetext 2.
		"""
		cnt = len(fontslist['items'])
		print 'parsed:' + str(cnt)

		fonts_quickpanel_list = []
		for item in range(0, cnt):
			if self.script in fontslist['items'][item]['subsets']:
				family = fontslist['items'][item]['family']
				variants = fontslist['items'][item]['variants']

				formatlist = []
				command = 'ADD F:'
				if len(variants) > 1:
					option = family + ': All Weights'
					formatlist = [option, 'Fetch all available font types of the'+family+' font', command+family+'&W:'+','.join(variants)]
					fonts_quickpanel_list.append(formatlist)

				for variant in variants:
					option = family + ': ' + variant
					formatlist = [option, 'The '+family+' font', command+family+'&W:'+variant]
					fonts_quickpanel_list.append(formatlist)

		cnt = len(fonts_quickpanel_list)
		print 'associated:' + str(cnt)
		return fonts_quickpanel_list

import sublime, sublime_plugin, sys
from bisect import bisect_left

illegal_functions = sorted(['split', 'strcut', 'strimwidth', 'stripos', 'stristr', 'strlen', 'strpos', 'strrchr', 'strrichr', 'strripos', 'strrpos', 'strstr', 'strtolower', 'strtoupper', 'strwidth', 'substr_count', 'substr'])

def contains(a, x):
	'Locate the leftmost value exactly equal to x'
	i = bisect_left(a, x)
	if i != len(a) and a[i] == x:
		return True
	return False

class LegacyStringsCommand(sublime_plugin.EventListener):
	def highlight(self, view):
		if view.settings().get('syntax') == 'Packages/PHP/PHP.tmLanguage':
			fnInvocs = view.find_by_selector('support.function.builtin_functions.php, support.function.string.php')
			legacies = []
			for fnInvoc in fnInvocs:
				fn = view.substr(fnInvoc)
				if contains(illegal_functions, fn.lower()):
					legacies.append(fnInvoc)

			if len(legacies) > 0:
				view.add_regions("legacy.php.string.function", legacies, 'invalid.illegal.php', 'dot', sublime.PERSISTENT)
			else:
				view.erase_regions("legacy.php.string.function")
		else:
			view.erase_regions("legacy.php.string.function")
	def on_modified(self, view):
		self.highlight(view)
	def on_activated(self, view):
		self.highlight(view)
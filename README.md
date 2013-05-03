sublime_webfonts
================

A sublime text 2 plugin for simple access to the Google web fonts API.


SET-UP
================
Copy the files into a new folder called 'Google Webfonts' inside your Sublime Text 2. Open the webfonts.sublime-settings file and copy your google webfonts API key into the placeholder for the API KEY.
You can acquire your google webfonts API_KEY at https://code.google.com/apis/console.
For more help, see: https://developers.google.com/fonts/docs/developer_api
Congratulations, you're now all-set to use the google webfonts plugin.


COMMANDS
========

As of now, there is only one available command for the plugin, which is found in the quick panel under 'Google Webfonts: Add Font'
This command fetches all the available fonts and lists them in the quick panel. The selected font will then be added in a link tag at the place of the cursor

MENU ENTRIES
============

Google Webfonts: Add Font
Google Webfonts: Merge Fonts



TO-DO
=====

MERGE COMMAND: combines multiple link files to google fonts into a single file to minimize http requests, will be called automatically after each Add Font. DONE, but took the quick fix, it doesn't check for multiple weights of the same font-family, see latest update notes.

MINIMIZE COMMAND: removes all unused fonts from the link sheet to minimize web traffic.
code cleanup.

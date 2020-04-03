# IPToCountry Example by David Bowland
# ./addons/eventscripts/iptocountry_example/iptocountry_example.py

# >>> To configure this addon please see iptocountry_example.cfg <<<

"""
Example addon for IPToCountry library.
Requires only ES 2.1+
"""


import cfglib
import cmdlib
import es
import langlib
import playerlib
import time
import usermsg

import iptocountry

import psyco
psyco.full()

from path import path


info = es.AddonInfo()
info.name     = 'IPToCountry Example'
info.version  = '3'
info.basename = 'iptocountry_example'
info.url      = 'http://addons.eventscripts.com/addons/view/iptocountry'
info.author   = 'SuperDave'
info.database = 'http://software77.net/geo-ip/'


addonpath = path(es.getAddonPath(info.basename))

###

config = cfglib.AddonCFG(addonpath.joinpath(info.basename + '.cfg'))

config.text(info.name + ' release %s options' % info.version)
config.text('./addons/eventscripts/%(basename)s/%(basename)s.cfg' % {'basename': info.basename})
config.text(info.url)
config.text('')
config.text('Load this addon with: es_load ' + info.basename)
config.text('\n')
config.text('To configure language settings for %s please see %s_languages.ini' % (info.name, info.basename))
config.text('\n')
config.text('This example addon:')
config.text('- Shows example interaction with IPToCountry')
config.text('- Automatically updates the IPToCountry database')
config.text('- Announces the country of joining players')
config.text('- Provides server commands for interaction with ESS scripts')
config.text('- Loads IPToCountry for quicker database access for other addons')
config.text('Due to the large size of the database, it is _HIGHLY_ recommended this addon be loaded during server start or map change.')
config.text('')
config.text('The database for the IPToCountry library is provided by: http://Software77.net')
config.text('')
config.text('NO CLAIMS ARE MADE REGARDING THE ACCURACY OF THIS DATABASE. Please use the IPToCountry library with that in mind.')
config.text('')
config.text('More information can be found here: http://software77.net/geo-ip/')
config.text('\n')

config.text('***** Update options *****')
config.text('This example addon will only update the database when no players are connected due to connectivity concerns.')
cvar_update_days = config.cvar('iptocountry_example_update_days', 14, 'Number of days between database updates--set to 0 to eliminate')
cvar_update_load = config.cvar('iptocountry_example_update_load', 0,  '0 = no change, 1 = update database every time ipcountry_example is loaded (NOT RECOMMENDED)')
config.text('\n')

config.text('***** Announcement options *****')
cvar_announce_chat   = config.cvar('iptocountry_example_announce_chat',   2, '0 = no change, 1 = announce on the console the country each player joins from, 2 = announce in chat area the country each player joins from')
cvar_announce_center = config.cvar('iptocountry_example_announce_center', 1, '0 = no change, 1 = announce in center text the country each player joins from')
cvar_announce_hud    = config.cvar('iptocountry_example_announce_hud',    0, '0 = no change, 1 = announce in a HUD message the country each player joins from')
config.text('\n')

config.text('***** Command documentation *****')
config.text('')
config.text('This addon provides the following server commands:')
config.text('')
config.text('iptocountry_getcountry <country var> <abbr var> <"ip">')
config.text('- Returns country name and three-letter abbreviation info for the specified IP')
config.text('   country var - Variable name to receive country name')
config.text('   abbr var    - Variable name to receive country three-letter abbreviation')
config.text('   ip          - IP address to resolve to country information')
config.text('')
config.text('iptocountry_getinfo <var> <info type> <"ip">')
config.text('- Returns location info for the specified IP')
config.text('   var       - Variable name to receive location inforation')
config.text('   info type - Type of information to receive (ip_from/ip_to/registry/assigned/country_2/country_3/country_long)')
config.text('   ip        - IP address to resolve to country information')
config.text('')
config.text('iptocountry_getlastupdate <var>')
config.text('- Returns the time of the last database update (Unix time)')
config.text('   var - Variable name to receive time of last update')
config.text('')
config.text('iptocountry_updatedata ["url"]')
config.text('- Syncs the database with an internet database')
config.text('THIS COMMAND SHOULD NOT BE USED WHILE PLAYERS ARE CONNECTED!')
config.text('   url - (Optional) URL of database to download')
config.text('')
config.text('iptocountry_updatefrompath ["path"]')
config.text('- Syncs the database with a local database')
config.text('THIS COMMAND SHOULD NOT BE USED WHILE PLAYERS ARE CONNECTED!')
config.text('   path - (Optional) Path to database file from server directory')
config.text('          Defaults to: /addons/eventscripts/_libs/python/IPToCountry.csv')

config.write()

###

ini = cfglib.AddonINI(addonpath.joinpath(info.basename + '_languages.ini'))

ini.setInitialComments([
 '# ./addons/eventscripts/%(basename)s/%(basename)s_languages.ini' % {'basename': info.basename},
 '# >>> For general addon configuration see ' + info.basename + '.cfg <<<',
 '',
 '# DO NOT translate words with $ or # in front!',
 '# For a list of language abbreviations please see ./addons/eventscripts/_libs/python/deflangs.ini'])

ini.addGroup('connect')
ini.addValueToGroup('connect', 'en', '#lightgreen$name#default has connected from #lightgreen$location#default.')
ini.addValueToGroup('connect', 'fr', '#lightgreen$name#default vient de #lightgreen$location#default.')
ini.addValueToGroup('connect', 'de', '#lightgreen$name#default kommt aus #lightgreen$location#default.')
ini.addValueToGroup('connect', 'pt', '#lightgreen$name#default se conecto de #lightgreen$location#default.')
ini.addValueToGroup('connect', 'es', '#lightgreen$name#default se ha conectado desde #lightgreen$location#default.')
ini.addValueToGroup('connect', 'nl', '#lightgreen$name#default komt uit #lightgreen$location#default.')
ini.addValueToGroup('connect', 'fi', '#lightgreen$name#default on liittynyt peliin maasta #lightgreen$location#default.')

ini.write()


lang_text = langlib.Strings(ini)

def remove_tags(text):
   """ Removes #lightgreen, #darkgreen, #green and #default tags from the supplied string """
   return reduce(lambda t, r: t.replace(r, ''), ('#lightgreen', '#darkgreen', '#green', '#default'), text)

###

def load():
   """
   Ensures critical server variables are created by the config
   Updates the database if necessary
   """
   config.execute()

   if cvar_update_load:
      data_update()
   else:
      try_update()

   if not iptocountry.get_last_update():
      es.dbgmsg(0, 'IPToCountry Example: Error, no database loaded!')


def round_end(event_var):
   """ Calls try_update to update the database if there are no human players """
   try_update()


def player_connect(event_var):
   """ Announces the connecting player's country """
   if event_var['networkid'] == 'BOT':
      return

   tokens = {'name': event_var['name'], 'location': iptocountry.get_country(event_var['address'])[0]}
   chat   = int(cvar_announce_chat)
   center = int(cvar_announce_center)
   hud    = int(cvar_announce_hud)

   es.dbgmsg(0, remove_tags(lang_text('connect', tokens)))

   for userid in es.getUseridList():
      text = lang_text('connect', tokens, playerlib.getPlayer(userid).get('lang'))

      if chat:
         if chat == 2:
            es.tell(userid, '#multi', text)
         else:
            usermsg.echo(userid, remove_tags(text))
      if center:
         es.centertell(userid, remove_tags(text))
      if hud:
         usermsg.hudhint(userid, remove_tags(text))


def player_disconnect(event_var):
   """ Calls try_update to update the database if the player was the last human on the server """
   try_update()


def unload():
   cmdlib.unregisterServerCommand('iptocountry_getcountry')
   cmdlib.unregisterServerCommand('iptocountry_getinfo')
   cmdlib.unregisterServerCommand('iptocountry_getlastupdate')
   cmdlib.unregisterServerCommand('iptocountry_updatedata')
   cmdlib.unregisterServerCommand('iptocountry_updatefrompath')

   for cvar in config.getCvars():
      es.ServerVar(cvar).set(0)

###

def try_update():
   """ Calls data_update if the data is the requisite age and no humans are connected """
   update_days = float(cvar_update_days)
   if update_days and not playerlib.getPlayerList('#human'):
      if time.time() - iptocountry.get_last_update() > update_days * 86400:
         data_update()


def data_update():
   """ Updates the IPToCountry database """
   es.dbgmsg(0, 'IPToCountry Example: Updating IPToCountry database')

   if iptocountry.update_data():
      es.dbgmsg(0, 'IPToCountry Example: Update complete')
   else:
      es.dbgmsg(0, 'IPToCountry Example: Error updating database!')

###

def country_cmd(args):
   """
   iptocountry_getcountry <country var> <abbr var> <"ip">
   Returns the country name and three-letter abbreviation associated with the IP to server variables
   """
   if len(args) == 3:
      info = iptocountry.get_country(args[2])

      es.ServerVar(args[0]).set(info[0])
      es.ServerVar(args[1]).set(info[1])

   else:
      es.dbgmsg(0, 'Syntax: iptocountry_getcountry <country var> <abbr var> <"ip">')

cmdlib.registerServerCommand('iptocountry_getcountry', country_cmd,
 'iptocountry_getcountry <country var> <abbr var> <"ip">\n Returns the country name and three-letter abbreviation associated with the IP to server variables')


def info_cmd(args):
   """
   iptocountry_getinfo <var> <info type> <"ip">
   Returns location information of the IP
   """
   if len(args) == 3:
      info_type = args[1].lower()
      data      = iptocountry.get_location_data(args[2])

      if data.has_key(info_type):
         es.ServerVar(args[0]).set(data[info_type])

      else:
         es.dbgmsg(0, 'IPToCountry Example: Info type "%s" not found' % args[1])
   else:
      es.dbgmsg(0, 'Syntax: iptocountry_getinfo <var> <info type> <"ip">')

cmdlib.registerServerCommand('iptocountry_getinfo', info_cmd,
 'iptocountry_getinfo <var> <info type> <"ip">\nReturns location information of the IP')


def lastupdate_cmd(args):
   """
   iptocountry_getlastupdate <var>
   Returns the time of the last IPToCountry database update
   """
   if len(args) == 1:
      es.ServerVar(args[0]).set(iptocountry.get_last_update())

   else:
      es.dbgmsg(0, 'Syntax: iptocountry_getlastupdate <var>')

cmdlib.registerServerCommand('iptocountry_getlastupdate', lastupdate_cmd,
 'iptocountry_getlastupdate <var>\nReturns the Unix time of the last IPToCountry database update')


def updatedata_cmd(args):
   """
   iptocountry_updatedata ["url"]
   Syncs the database with an internet database
   """
   if len(args) in (0, 1):
      if len(args) == 1:
         success = iptocountry.update_data(args[0])
      else:
         success = iptocountry.update_data()

      if success:
         es.dbgmsg(0, 'IPToCountry Example: Database successfully updated')
      else:
         es.dbgmsg(0, 'IPToCountry Example: Error updating database: ' + str(success))
   else:
      es.dbgmsg(0, 'Syntax: iptocountry_updatedata ["url"]')

cmdlib.registerServerCommand('iptocountry_updatedata', updatedata_cmd,
 'iptocountry_updatedata ["url"]\nSyncs the database with an internet database')


def updatefrompath_cmd(args):
   """
   iptocountry_updatefrompath <"path">
   Syncs the database with a local database
   """
   if len(args) == 1:
      success = iptocountry.update_from_file(args[0])
      if success:
         es.dbgmsg(0, 'IPToCountry Example: Database successfully updated')
      else:
         es.dbgmsg(0, 'IPToCountry Example: Error updating database: ' + str(success))
   else:
      es.dbgmsg(0, 'Syntax: iptocountry_updatefrompath <"path">')

cmdlib.registerServerCommand('iptocountry_updatefrompath', updatefrompath_cmd,
 'iptocountry_updatefrompath <"path">\nSyncs the database with a local database')
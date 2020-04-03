# IPToCountry
Resolves IP addresses to name of the originating country. 
Requires only ES 2.1+ Documentation (included in library):
To use this library, you must first import it: ```import iptocountry``` 

IPToCountry exposes the following functions: 

```get_country(ip)``` - Returns full the country name, three-letter country abbreviation corresponding to IP 

```ip``` = IP address to resolve to country name 

```get_location_data(ip)``` - Returns a dictionary of location data corresponding to IP 

Dictionary keys: 

```ip_from``` = Bottom long IP of location range 

```ip_to``` = Upper long IP of location range 

```registry``` = International registry agency through which the IP is registered 

```assigned``` = Unix time the IP was assigned 

```country_2``` = Two-character international country code 

```country_3``` = Three-character international country code (preferred because more unique) 

```country_long``` = Country name 

```ip``` = IP address to resolve to location data 

```update_data(url=None)``` - Syncs server database with internet data-- **VERY SLOW** - Returns True if update was sucessful otherwise returns False 

```url``` = URL to download IPToCountry database 

```get_last_update()``` - Returns the time of the last database update (in Unix time) 

```update_from_file```&#40;path=None&#41; - Updates the database from IpToCountry.csv that has been extracted, see the library link below to download the database - Returns True if data was successfully updated otherwise return False 

```path``` = Absolute path to file &#40;including IpToCountry.csv&#41; 

The following instance of CountryResolve is publicly exposed: iptocountry.service 

The database for this library is provided by http://Software77.net. 

For more information, please see: http://software77.net/cgi-bin/ip-country/geo-ip.pl
 
_**NO CLAIMS ARE MADE REGARDING THE ACCURACY OF THIS DATABASE.**_ 

Please use this library with that in mind.

This library comes with an example addon with the following options:
 
IPToCountry Example options 
// ./addons/eventscripts/iptocountry_example/iptocountry_example.cfg 

http://addons.eventscripts.com/addons/view/iptocountry 

Load this addon with: ```es_load iptocountry_example``` 

To configure language settings for IPToCountry Example please see iptocountry_example_languages.ini 

This example addon: 
- Shows example interaction with IPToCountry 
- Automatically updates the IPToCountry database 
- Announces the country of joining players 
- Provides server commands for interaction with ESS scripts 
- Loads IPToCountry for quicker database access for other addons 
Due to the large size of the database, it is _HIGHLY_ recommended this addon be loaded during server start or map change. 

The database for the IPToCountry library is provided by: http://software77.net 

NO CLAIMS ARE MADE REGARDING THE ACCURACY OF THIS DATABASE. Please use the IPToCountry library with that in mind. 

More information can be found here: http://software77.net/cgi-bin/ip-country/geo-ip.pl 

### Update options
This exaple addon will only update the database when no players are connected due to conenctivity concerns. 

```iptocountry_example_update_days 14```

Number of days between database updates--set to 0 to eliminate [default 14] 

```iptocountry_example_update_load 0``` 

0 = no change, 1 = update database every time ipcountry_example is loaded (NOT RECOMMENDED) [default 0] 

###  Announcement options 

```iptocountry_example_announce_chat 2```

0 = no change, 1 = announce on the console the country each player joins from,  2 = annoucne in chat area the country each player joins from [default 2] 

```iptocountry_example_announce_center 1``` 

0 = no change, 1 = announce in center text the country each player joins from [default 1]

```iptocountry_example_announce_hud 0```
 
0 = no change, 1 = announce in a HUD message the country each player joins from [default 0] 

### Command documentation 

This addon provides the following server commands: 
```iptocountry_getcountry -country var- -abbr var- -"ip"-``` - Returns country name and three-letter abbreviation info for the specified IP 

```country var``` - Variable name to receive country name 

```abbr var``` - Variable name to receive country three-letter abbreviation 

```ip``` - IP address to resolve to country information 

```iptocountry_getinfo -var- -info type- -"ip"-``` - Returns location info for the specified IP 

```var``` - Variable name to receive location inforation 

```info type``` - Type of information to receive (ip_from/ip_to/registry/assigned/country_2/country_3/country_long) 

```ip``` - IP address to resolve to country information 

```iptocountry_getlastupdate -var-``` - Returns the time of the last database update (in seconds since epoch) 

```var``` - Variable name to receive time of last update 

```iptocountry_updatedata ["url"]``` - Syncs the database with an internet database 

 _**THIS COMMAND SHOULD NOT BE USED WHILE PLAYERS ARE CONNECTED!**_ 

```url``` - (Optional) URL of database to download 

```iptocountry_updatefrompath ["path"]``` - Syncs the database with a local database 

_**THIS COMMAND SHOULD NOT BE USED WHILE PLAYERS ARE CONNECTED!**_ 

```path``` - (Optional) Path to database file from server directory 

Defaults to: /addons/eventscripts/_libs/python/IPToCountry.csv 

Please see the forum link below for more translations or if you have a translation to add. 
Please also post general questions or comments.


### Installation
**Install with:**
```es_install iptocountry``` or ```es_install iptocountry autoload```

Version Notes For 3
Updated on: 2010-12-02 21:46:46 EST by SuperDave
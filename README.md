# SublimeBart
## Get real time BART arrival and departure data directly from sublime text

#### [Sublime Text](http://www.sublimetext.com/)
#### [BART](http://www.bart.gov/)

## About
Integrates with the BART api to allow you to check real time BART arrival and departure times.

## Usage
Type 'ctrl+shift+p' and type BART to search for the available commands.
1. Get Schedule: Prompts the user for an origin and destination. Shows a popup of the next 4 routes from the selected origin and destination. If the route includes transfers, the user may select the row in the list for a more detailed list of each transfer.
2. Go Home: Same as Get Schedule, but skips the prompting process, and uses the users preferences for work and home.
3. Go To Work: Same as Go Home but origin and destination are switched.

## Options

`SublimeBart` exposes two useful options: home, and work. These are available under `Preferences -> Package Settings -> Sublime Bart` or search for `SublimeBart: Set plugin options`

Example `User Plugin Preferences`

```json
{
  "home": "ashb",
  "work": "civc",
}
```

The following show a map of abbreviations to station names.
```json
{
  "12th": "12th St. Oakland City Center",
  "16th": "16th St. Mission (SF)",
  "19th": "19th St. Oakland",
  "24th": "24th St. Mission (SF)",
  "ashb": "Ashby (Berkeley)",
  "balb": "Balboa Park (SF)",
  "bayf": "Bay Fair (San Leandro)",
  "cast": "Castro Valley",
  "civc": "Civic Center (SF)",
  "cols": "Coliseum/Oakland Airport",
  "colm": "Colma",
  "conc": "Concord",
  "daly": "Daly City",
  "dbrk": "Downtown Berkeley",
  "dubl": "Dublin/Pleasanton",
  "deln": "El Cerrito del Norte",
  "plza": "El Cerrito Plaza",
  "embr": "Embarcadero (SF)",
  "frmt": "Fremont",
  "ftvl": "Fruitvale (Oakland)",
  "glen": "Glen Park (SF)",
  "hayw": "Hayward",
  "lafy": "Lafayette",
  "lake": "Lake Merritt (Oakland)",
  "mcar": "MacArthur (Oakland)",
  "mlbr": "Millbrae",
  "mont": "Montgomery St. (SF)",
  "nbrk": "North Berkeley",
  "ncon": "North Concord/Martinez",
  "orin": "Orinda",
  "pitt": "Pittsburg/Bay Point",
  "phil": "Pleasant Hill",
  "powl": "Powell St. (SF)",
  "rich": "Richmond",
  "rock": "Rockridge (Oakland)",
  "sbrn": "San Bruno",
  "sfia": "San Francisco Int\"l Airport",
  "sanl": "San Leandro",
  "shay": "South Hayward",
  "ssan": "South San Francisco",
  "ucty": "Union City",
  "wcrk": "Walnut Creek",
  "wdub": "West Dublin",
  "woak": "West Oakland"
}
```

## Installation
### Through [Sublime Package Manager](http://wbond.net/sublime_packages/package_control)

* `Ctrl+Shift+P` or `Cmd+Shift+P` in Linux/Windows/OS X
* type `install`, select `Package Control: Install Package`
* type `SublimeBart`, select `SublimeBart`

### Manually
Make sure you use the right Sublime Text folder. For example, on OS X, packages for version 2 are in `~/Library/Application\ Support/Sublime\ Text\ 2`, while version 3 is labeled `~/Library/Application\ Support/Sublime\ Text\ 3`.

These are for Sublime Text 3:

#### Mac
`git clone https://github.com/ganemone/SublimeBart.git ~/Library/Application\ Support/Sublime\ Text\ 3/Packages/SublimeBart`

#### Linux
`git clone https://github.com/ganemone/SublimeBart.git ~/.config/sublime-text-3/Packages/SublimeBart`

#### Windows
`git clone https://github.com/ganemone/SublimeBart.git "%APPDATA%/Sublime Text 3/Packages/SublimeBart"`

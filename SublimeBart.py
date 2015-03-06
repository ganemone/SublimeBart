import sublime
import sublime_plugin
import threading
from xml.etree import ElementTree
from .lib.requests import requests
from .src.stations import stations, abbreviations
from .src.Route import Route
from .src.PluginUtils import get_pref, set_settings

bsa_url = 'http://api.bart.gov/api/bsa.aspx'
sched_url = 'http://api.bart.gov/api/sched.aspx'
api_key = 'MW9S-E7SL-26DU-VV8V'


class ScheduleCommand(sublime_plugin.WindowCommand):
    """Sublime Window Command which prompts the user for an
    origin and destination BART station, requests real
    time departure and arrival information from the BART API
    and displays it to the user"""

    def run(self):
        """Called when the command is executed.  Runs the command"""
        self.origin = None
        self.destination = None
        self.choose_station(self.on_origin_choosen)
        self.routes = []

    def on_origin_choosen(self, index):
        """Callback for when the originating station is choosen.
        Sets self.origin and prompts the user for the destination
        station"""

        if index is -1:
            return None

        self.origin = abbreviations[index]
        sublime.set_timeout(
            lambda: self.choose_station(self.on_destination_choosen), 10
        )

    def on_destination_choosen(self, index):
        """Callback for when the destination station is choosen.
        Sets self.destination and makes the BART API request on
        a new thread"""

        if index is -1:
            return None

        self.destination = abbreviations[index]
        planner = RoutePlanner(self.window, self.origin, self.destination)
        threading.Thread(target=planner.get_route_plan).start()

    def choose_station(self, callback):
        """Propmts the user for a BART station"""
        self.window.show_quick_panel(stations, callback)


class GoHomeCommand(sublime_plugin.WindowCommand):
    """Sublime Window Command which requests real time arrival
    and departure information from the BART API for the saved home
    and work stations and displays it to the user"""

    def run(self):
        """Called when the command is executed. Runs the command"""
        home = get_pref('home')
        work = get_pref('work')
        planner = RoutePlanner(self.window, work, home)
        threading.Thread(target=planner.get_route_plan).start()


class GoToWorkCommand(sublime_plugin.WindowCommand):
    """Same as GoHomeCommand but with origin and destination switched"""

    def run(self):
        """Called when the command is executed. Runs the command"""
        home = get_pref('home')
        work = get_pref('work')
        planner = RoutePlanner(self.window, home, work)
        threading.Thread(target=planner.get_route_plan).start()


class RoutePlanner():
    """Helper class for planning routes. Handles requesting the BART API
    based on an origin and destination station. Additionally parses the
    resulting xml response."""

    def __init__(self, window, origin, destination):
        self.routes = []
        self.window = window
        self.origin = origin
        self.destination = destination

    def get_route_plan(self):
        params = self.get_params_with_key({
            'cmd': 'depart',
            'orig': self.origin,
            'dest': self.destination
        })
        res = requests.get(sched_url, params=params)
        self.handle_route_plan_response(res.text)

    def handle_route_plan_response(self, response):
        root = ElementTree.fromstring(response)
        schedule = root.find('schedule')
        trips = schedule.find('request').findall('trip')
        routes = []
        for trip in trips:
            routes.append(Route(trip.attrib, trip.findall('leg')))

        self.routes = routes
        sublime.set_timeout(
            lambda: self.show_routes(), 10
        )

    def show_routes(self):
        route_descriptions = list(map(
            lambda route: route.short_description(), self.routes
        ))
        self.window.show_quick_panel(route_descriptions, self.on_route_choosen)

    def get_params_with_key(self, params):
        params['key'] = 'MW9S-E7SL-26DU-VV8V'
        return params

    def on_route_choosen(self, index):
        if index is -1:
            return
        route = self.routes[index]
        if route.has_transfer():
            legs = route.long_description()
            sublime.set_timeout(
                lambda: self.window.show_quick_panel(legs, noop)
            )


class ChangeSettingsCommand(sublime_plugin.WindowCommand):
    """Sublime Window Command for setting the default home
    and work stations."""

    def run(self, key):
        self.key = key
        self.choose_station(self.on_station_choosen)

    def on_station_choosen(self, index):
        if index >= 0:
            set_settings(self.key, abbreviations[index])

    def choose_station(self, callback):
        self.window.show_quick_panel(stations, callback)


def noop(self, index):
    return

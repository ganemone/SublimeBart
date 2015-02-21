import sublime
import sublime_plugin
import threading
from .lib.requests import requests
from .src.stations import stations, abbreviations
from .src.Route import Route
from xml.etree import ElementTree

bsa_url = 'http://api.bart.gov/api/bsa.aspx'
sched_url = 'http://api.bart.gov/api/sched.aspx'
api_key = 'MW9S-E7SL-26DU-VV8V'


class ScheduleCommand(sublime_plugin.WindowCommand):

    def run(self):
        self.origin = None
        self.destination = None
        self.choose_station(self.on_origin_choosen)
        self.routes = []

    def on_origin_choosen(self, index):
        if index is -1:
            return None

        self.origin = abbreviations[index]
        sublime.set_timeout(
            lambda: self.choose_station(self.on_destination_choosen), 10
        )

    def on_destination_choosen(self, index):
        if index is -1:
            return None

        self.destination = abbreviations[index]
        threading.Thread(target=self.get_route_plan).start()

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

    def on_route_choosen(self, index):
        if index is -1:
            return
        route = self.routes[index]
        if route.has_transfer():
            legs = route.long_description()
            sublime.set_timeout(
                lambda: self.window.show_quick_panel(legs, self.noop)
            )

    def noop(self, index):
        return

    def get_schedules(self):
        res = requests.get(sched_url)
        sublime.message_dialog(res.text)

    def get_params_with_key(self, params):
        params['key'] = 'MW9S-E7SL-26DU-VV8V'
        return params

    def choose_station(self, callback):
        self.window.show_quick_panel(stations, callback)

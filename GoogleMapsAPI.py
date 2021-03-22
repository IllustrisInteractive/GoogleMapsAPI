import requests
import polyline

class Directions:

    class Place:
        class Step:
            def __init__(self, step):
                self.step = step
                self.html_instructions = self.step["html_instructions"]
                self.polyline = self.step["polyline"]["points"]
                self.start = [self.step["start_location"]["lat"], self.step["start_location"]["lng"]]
                self.end = [self.step["end_location"]["lat"], self.step["end_location"]["lng"]]

            def get_distance(self, typeof="text"):
                if typeof == "value":
                    return self.step["distance"]["value"]
                else:
                    return self.step["distance"]["text"]

            def decode_polyline(self):
                return polyline.decode(self.polyline)

        def __init__(self, place, typeof):
            self.route = place
            self.typeof = "Directions"
            self.steps = []
            self.number_of_steps = self.get_steps()

        def get_coordinates(self, typeof="all"):
            return_dict = []
            return_list = []
            if typeof == "all":
                for data in self.route["routes"][0]["legs"]:
                    return_dict = {
                        'start': [data["start_location"]["lat"], data["start_location"]["lng"]],
                        'end': [data["end_location"]["lat"], data["end_location"]["lng"]]
                    }
                return return_dict

            if typeof == "start":
                for data in self.route["routes"][0]["legs"]:
                    return_list = [data["start_location"]["lat"], data["start_location"]["lng"]]
                return return_list

            if typeof == "end":
                for data in self.route["routes"][0]["legs"]:
                    return_list = [data["start_location"]["lat"], data["start_location"]["lng"]]
                return return_list

        def get_steps(self):
            for data in self.route["routes"][0]["legs"]:
                i = 0
                for step in data["steps"]:
                    self.steps.append(self.Step(step))
                    i += 1
                return i

    def __init__(self, key):
        self.query = ""
        self.origin = ""
        self.key = key
        self.steps = 0
        self.places = []

    def find(self, origin, endpoint):  # the location (string of address or coordinates) to request
        self.query = endpoint
        self.origin = origin
        if endpoint == "" or origin == "":
            raise IncompleteRequest()
        elif self.key == "":
            raise InvalidKey()
        else:
            try:
                response = \
                    requests.get(
                        "https://maps.googleapis.com/maps/api/directions/json?origin={}&destination={}&key={}".format(
                            self.origin, self.query, self.key)).json()
                self.places.append(self.Place(response, "Directions"))

            except Exception:
                raise ConnectionFailed()


# ! - Exceptions - !
class IncompleteRequest(Exception):
    def __init__(self):
        super().__init__("No string passed in one or both parameters for find().")


class ConnectionFailed(Exception):
    def __init__(self):
        super().__init__("A connection to the API was unsuccessful.")


class ResponseIsFail(Exception):
    def __init__(self, response):
        super().__init__("The API response contains a failed status code.")
        print(response)


class InvalidKey(Exception):
    def __init__(self):
        super().__init__(
            "No key provided for the API. Make sure to initialize the object with <SDK>(key). Ex: Directions(yourkeyhere).")
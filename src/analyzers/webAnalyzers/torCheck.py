import requests
from analyzers.classes import WebAnalyzer


class TorCheck(WebAnalyzer):

    def run(self, ioc, type, node_id = None):
        # Housekeeping
        self._ioc = ioc
        self._type = type

        if type == "ip":
            # Set the endpoint URL
            url = "https://check.torproject.org/exit-addresses"

        else:
            url = "NULL"

        # Create the headers
        headers = {"accept": "text/html"}

        # Send the request
        try:
            response = requests.request(method="GET", url=url, headers=headers)
            response.raise_for_status()
            # print(response.headers)

        except Exception as e:
            print(f"Error: {e}")
            return None

        # Parse the response
        data = []  # Create a list to store the dictionary for each node

        # Split the response into a list of lines
        lines = response.text.splitlines()
        lines_iter = iter(lines)

        dict = {}  # Create a dictionary to store the key-value pairs for each node
        exitAddresses = []  # Create a list to store the exit addresses for each node

        while True:
            try:
                key, value = next(lines_iter).strip().split(None, 1)

                if key == "ExitNode":

                    if "ExitNode" in dict.keys():
                        # A new entry has started, add the exit addresses to the dictionary for the previous node
                        dict["ExitAddresses"] = exitAddresses
                        # Add the dictionary for the previous node to the data
                        data.append(dict)
                        # Clear the dictionary and the exit addresses list
                        dict = {}
                        exitAddresses = []

                    # Add the exit node ID to the dictionary
                    dict["ExitNode"] = value

                elif key == "ExitAddress":
                    # Append the exit address to the respective list
                    exitAddresses.append(value)

                else:
                    # Add the key-value pair
                    dict[key] = value

            except StopIteration:
                # Process the dictionary for the last node
                dict["ExitAddresses"] = exitAddresses
                data.append(dict)
                break

        # Now that we have our array, we can check each dictionary and determine whether
        # the specified IP address is a Tor exit node
        result = []
        for node in data:
            exitAddresses = node["ExitAddresses"]
            for exitAddress in exitAddresses:
                if ioc in exitAddress:
                    result.append(node)

        return result

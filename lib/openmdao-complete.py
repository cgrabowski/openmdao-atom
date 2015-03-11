# mirror autocomplete-plus-jedi functionality for openmdao specific suggestions

import os
import sys
import json
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import socket
import time

sys.path.append(os.path.realpath(__file__))


class http_completion(BaseHTTPRequestHandler):
    """
    Completion handler which returns the completions for a given source,
    line and cursor positon.
    """
    def _set_headers(self):
        """set the standard headers for a JSON response"""
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()

    def do_POST(self):
        """
        Payload to receive:
            source: whole source to parse
            line / column : current line and column

        Returns:
            array with dictionaries in it (name, description, docstring)
        """
        self._set_headers()

        length = int(self.headers.getheader('content-length', 0))
        read = self.rfile.read(length)
        read = json.loads(read)

        payload = completions(read["source"], read["line"], read["column"])
        payload = json.dumps(payload)

        self.wfile.write(payload)
        return


def run_server():
    """run the httpd"""
    address = ('', 7776)

    while True:
        try:
            print "Starting httpd"
            httpd = HTTPServer(address, http_completion)
            httpd.serve_forever()
        except (socket.error, KeyboardInterrupt) as exc:
            if exc.__class__ == KeyboardInterrupt:
                break

            # If we cannot bind to the port sleep wait 1 second and retry.
            # This can happen when reloading Atom e.x.
            time.sleep(1)


def completions(source, line, column):
    """
    generate list with completions for the line and column.

    Arguments:
        source: source code to generate completion for
        line, column: current cursor position in the source code

    Returns:
        list with dictionaries containing the name, docstring and description
        for all completions.
    """
    completions = [{
        "name": "dummy",
        "description": "desc",
        "docstring": "docs",
    }]

    return completions


if __name__ == "__main__":
    project_path = sys.argv[1]
    sys.path.append(project_path)

    run_server()

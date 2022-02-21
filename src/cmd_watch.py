#!/usr/bin/python3

#Based on http://stackoverflow.com/questions/1191374/using-module-subprocess-with-timeout
#MIT Licence https://opensource.org/licenses/MIT

import subprocess, threading
import time

class Command(object):
    def __init__(self, cmd):
        self.cmd = cmd
        self.process = None
        self.result = []
        self.code = 0

    def run(self, timeout):
        def target():
            self.process = subprocess.Popen(self.cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
            self.result = []
            for line in iter(self.process.stdout.readline, ""):
                self.result.append(line)
                self.process.poll()

        thread = threading.Thread(target=target)
        thread.start()
        thread.join(timeout)
        if self.process.poll() == None:
            self.process.terminate()
            time.sleep(2)
            if self.process.poll() == None:
                self.process.kill()
            thread.join()
        self.code = self.process.poll()
        if self.code == None:
            self.code = 1


class iter_to_stream(object):
    def __init__(self, iterable):
        self.buffered = ""
        self.iter = iter(iterable)

    def read(self, size = None):
        result = ""
        if size == None:
            end = False
            while not end:
                data = next(self.iter, None)
                if data is None:
                    end = True
                    break
                result += data
            return result
        while size > 0:
            data = self.buffered or next(self.iter, None)
            self.buffered = ""
            if data is None:
                break
            size -= len(data)
            if size < 0:
                data, self.buffered = data[:size], data[size:]
            result += data
        return result

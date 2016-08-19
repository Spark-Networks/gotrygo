#!/usr/bin/python

import curses
import requests
import sys
import time
import datetime
import itertools
from collections import OrderedDict
import argparse

def format_output(data):
	output = []
	template = '{0: <15} {1: <10} {2: <10} {3: <30} {4} ({5})'
	current_time = datetime.datetime.now()
	output.append(template.format("Container Name","Version","Count","First Request","Last Request","Since"))
	for host, host_data in data["hosts"].iteritems():
		output.append(template.format(host,host_data['version'],host_data['count'],str(host_data['first_request']).split(".")[0],str(host_data['last_request']).split(".")[0],str(current_time - host_data['last_request']).split(".")[0]))
	return output

def main():
	# parse script arguments
	parser = argparse.ArgumentParser(description="This script is only intended to be run against the GoTryGo application.")
	parser.add_argument('-c','--count', type=int, default=100, help="Number of requests to make, 0 means to run forever (default: 100)")
	parser.add_argument('-d', '--delay', type=float, default=1, help="Delay between requests (default: 1 sec)")
	parser.add_argument('-t', '--timeout', type=float, default=2, help="Time to wait before a requests is considered 'dropped' (default: 2 sec)")
	parser.add_argument('url', help="URL at which the application being tested can be reached")
	args = parser.parse_args()

	# set up the curses environment
	stdscr = curses.initscr()
	curses.noecho()

	data = {"hosts":OrderedDict()}

	out_of_string = ""
	if args.count == 0:
		range_func = itertools.count()
	else:
		range_func = xrange(args.count)
		out_of_string = " out of {0}".format(args.count)
	completed_requests = 0
	try:
		for i in range_func:
			try:
				r = requests.get(args.url, timeout=args.timeout)
				values = r.json()
			except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
				values = {"host": "DROPPED REQUEST","version":"N/A"}
			except ValueError:
				values = {"host": "NOT GOTRYGO","version":"N/A"}
			if not "host" in values:
				values = {"host": "NOT GOTRYGO","version":"N/A"}
			host = values.get('host')
			if not host in data["hosts"]:
				data["hosts"][host] = {"count":1, "version": values.get("version"), "first_request": datetime.datetime.now()}
			else:
				data["hosts"][host]["count"] = data["hosts"][host]["count"] + 1
			data["hosts"][host]["last_request"] = datetime.datetime.now()
			completed_requests = i + 1
			stdscr.addstr(0, 0, "Completed {0} requests{1}".format(completed_requests,out_of_string))
			write_line = 1
			for line in format_output(data):
				stdscr.addstr(write_line, 0, line)
				write_line = write_line + 1
			stdscr.refresh()
			time.sleep(args.delay)
		stdscr.addstr(0, 0, "Completed {0} requests{1} - FINISHED (press any key to exit)".format(completed_requests,out_of_string))
		stdscr.refresh()
		stdscr.getch()
	except KeyboardInterrupt:
		stdscr.addstr(0, 0, "Completed {0} requests{1} - STOPPED (press any key to exit)".format(completed_requests,out_of_string))
		stdscr.refresh()
		stdscr.getch()
	# clean up curses environment
	curses.nocbreak()
	stdscr.keypad(0)
	curses.echo()
	curses.endwin()

	# print output to normal console
	print "Completed {0} requests{1} - FINISHED".format(completed_requests,out_of_string)
	for line in format_output(data):
		print line
	sys.exit(0)

if __name__ == "__main__":
	main()

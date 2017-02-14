#!/usr/bin/env python3

"""
Created on 12 Nov 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

examples:
{"msg": null, "err": {"code": "UNKNOWN_CMD", "value": "hello"}}
{"msg": {"op": "scs-rpi-006", "spec": "scs-rpi-006"}, "err": null}

deliver-change
870725f3-e692-4538-aa81-bfa8b51d44e7

south-coast-science-dev
43308b72-ad41-4555-b075-b4245c1971db
"""

from scs_core.data.localized_datetime import LocalizedDatetime
from scs_core.osio.finder.message_finder import MessageFinder

from scs_host.client.http_client import HTTPClient


# --------------------------------------------------------------------------------------------------------------------

org_id = "south-coast-science-dev"
print(org_id)

api_key = "43308b72-ad41-4555-b075-b4245c1971db"
print(api_key)

topic = "/users/southcoastscience-dev/test/gases"
print(topic)

end_date = LocalizedDatetime.now()
start_date = LocalizedDatetime.construct_from_timestamp(end_date.timestamp() - 60)

print("start: %s" % start_date)
print("end: %s" % end_date)

print("-")


# --------------------------------------------------------------------------------------------------------------------

http_client = HTTPClient()


finder = MessageFinder(http_client, api_key)
print(finder)
print("=")


messages = finder.find_for_topic(topic, start_date, end_date)

print("got:%d" % (len(messages)))
print("-")

for message in messages:
    print(message)

print("-")

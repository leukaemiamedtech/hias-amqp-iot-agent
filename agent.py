#!/usr/bin/env python
""" HIAS iotJumpWay Agent Abstract Class

HIAS IoT Agents process all data coming from entities connected to the HIAS
iotJumpWay brokers.

MIT License

Copyright (c) 2021 Asociación de Investigacion en Inteligencia Artificial
Para la Leucemia Peter Moss

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files(the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and / or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

Contributors:
- Adam Milton-Barker

"""

from gevent import monkey
monkey.patch_all()

import json
import os
import os.path
import psutil
import requests
import signal
import sys
import time
import threading

sys.path.append(
	os.path.abspath(os.path.join(__file__,  "..", "..", "..", "..")))

from abc import ABC, abstractmethod
from flask import Flask, request, Response
from datetime import timedelta
from datetime import datetime
from threading import Thread

from components.agents.AbstractAgent import AbstractAgent

class Agent(AbstractAgent):
	""" Class representing a HIAS iotJumpWay MQTT IoT Agent.

	This object represents a HIAS iotJumpWay IoT Agent. HIAS IoT Agents
	process all data coming from entities connected to the HIAS iotJumpWay
	broker using the MQTT & Websocket machine to machine protocols.
	"""

	def __init__(self, protocol):
		super().__init__(protocol)

	def statusCallback(self, ch, method, properties, body):
		""" Processes status messages. """
		Thread(target=self.statusesWorker, args=(body,), daemon=True).start()

	def statusesWorker(self, body):
		"""Called in the event of a status payload

		Args:
			topic (str): The topic the payload was sent to.
			payload (:obj:`str`): The payload.
		"""

		data = json.loads(body)

		entityType = data["Type"]
		entity = data["Id"]
		status = data["Status"]

		self.helpers.logger.info(
			"Received " + entityType  + " Status: " + status)

		attrs = self.getRequiredAttributes(entityType, entity)
		bch = attrs["blockchain"]

		if not self.hiasbch.iotJumpWayAccessCheck(bch):
			return

		entity = attrs["id"]
		location = attrs["location"]
		zone = attrs["zone"] if "zone" in attrs else "NA"

		updateResponse = self.hiascdi.updateEntity(
			entity, entityType, {
				"networkStatus": {"value": status},
				"networkStatus.metadata": {"timestamp": datetime.now().isoformat()},
				"dateModified": {"value": datetime.now().isoformat()}
			})

		if updateResponse:
			_id = self.mongodb.insertData(self.mongodb.mongoConn.Statuses, {
				"Use": entityType,
				"Location": location,
				"Zone": zone,
				"HIASCDI": entity if entityType == "HIASCDI" else "NA",
				"Agent": entity if entityType == "Agent" else "NA",
				"Application": entity if entityType == "Application" else "NA",
				"Device": entity if entityType == "Device" else "NA",
				"Staff": entity if entityType == "Staff" else "NA",
				"Status": status,
				"Time": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
			}, None)

			self.helpers.logger.info(
				entityType + " " + entity + " status update OK")
		else:
			self.helpers.logger.error(
				entityType + " " + entity + " status update KO")

	def lifeCallback(self, ch, method, properties, body):
		""" Processes life messages. """
		Thread(target=self.lifeWorker, args=(body,), daemon=True).start()

	def lifeWorker(self, body):
		""" Called in the event of a life payload

		Args:
			topic (str): The topic the payload was sent to.
			payload (:obj:`str`): The payload.
		"""

		data = json.loads(body)

		entityType = data["Type"]
		entity = data["Id"]

		self.helpers.logger.info(
			"Received " + entityType  + " Life data")

		attrs = self.getRequiredAttributes(entityType, entity)
		bch = attrs["blockchain"]

		if not self.hiasbch.iotJumpWayAccessCheck(bch):
			return

		entity = attrs["id"]
		location = attrs["location"]
		zone = attrs["zone"] if "zone" in attrs else "NA"

		updateResponse = self.hiascdi.updateEntity(
			entity, entityType, {
				"networkStatus": {"value": "ONLINE"},
				"networkStatus.metadata": {"timestamp": datetime.now().isoformat()},
				"dateModified": {"value": datetime.now().isoformat()},
				"cpuUsage": {
					"value": float(data["CPU"])
				},
				"memoryUsage": {
					"value": float(data["Memory"])
				},
				"hddUsage": {
					"value": float(data["Diskspace"])
				},
				"temperature": {
					"value": float(data["Temperature"])
				},
				"location": {
					"type": "geo:json",
					"value": {
						"type": "Point",
						"coordinates": [float(data["Latitude"]), float(data["Longitude"])]
					}
				}
			})

		if updateResponse:
			_id = self.mongodb.insertData(self.mongodb.mongoConn.Life, {
				"Use": entityType,
				"Location": location,
				"Zone": zone,
				"HIASCDI": entity if entityType == "HIASCDI" else "NA",
				"Agent": entity if entityType == "Agent" else "NA",
				"Application": entity if entityType == "Application" else "NA",
				"Device": entity if entityType == "Device" else "NA",
				"Staff": entity if entityType == "Staff" else "NA",
				"Data": data,
				"Time": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
			}, None)

			self.helpers.logger.info(
				entityType + " " + entity + " life update OK")
		else:
			self.helpers.logger.error(
				entityType + " " + entity + " life update KO")

	def sensorsCallback(self, ch, method, properties, body):
		""" Processes life messages. """
		Thread(target=self.sensorsWorker, args=(body,), daemon=True).start()

	def sensorsWorker(self, body):
		""" Called in the event of a sensor payload

		Args:
			topic (str): The topic the payload was sent to.
			payload (:obj:`str`): The payload.
		"""

		data = json.loads(body)

		entityType = data["Type"]
		entity = data["Id"]

		self.helpers.logger.info(
			"Received " + entityType + " Life data")

		attrs = self.getRequiredAttributes(entityType, entity)
		bch = attrs["blockchain"]

		if not self.hiasbch.iotJumpWayAccessCheck(bch):
			return

		entity = attrs["id"]
		location = attrs["location"]
		zone = attrs["zone"] if "zone" in attrs else "NA"

		sensors = self.hiascdi.getSensors(
			entity, entityType)
		sensorData = sensors["sensors"]

		i = 0
		for sensor in sensorData:
			for prop in sensor["properties"]["value"]:
				if data["Type"].lower() in prop:
					sensorData[i]["properties"]["value"][data["Type"].lower()] = {
						"value": data["Value"],
						"timestamp": datetime.now().isoformat()
					}
			i = i + 1

		updateResponse = self.hiascdi.updateEntity(
			entity, entityType, {
				"networkStatus": {"value": "ONLINE"},
				"networkStatus.metadata": {"timestamp": datetime.now().isoformat()},
				"dateModified": {"value": datetime.now().isoformat()},
				"sensors": sensorData
			})

		if updateResponse:
			_id = self.mongodb.insertData(self.mongodb.mongoConn.Sensors, {
				"Use": entityType,
				"Location": location,
				"Zone": zone,
				"Device": entity if entityType == "Device" else "NA",
				"HIASCDI": entity if entityType == "HIASCDI" else "NA",
				"Agent": entity if entityType == "Agent" else "NA",
				"Application": entity if entityType == "Application" else "NA",
				"Device": entity if entityType == "Device" else "NA",
				"Staff": entity if entityType == "Staff" else "NA",
				"Sensor": data["Sensor"],
				"Type": data["Type"],
				"Value": data["Value"],
				"Message": data["Message"],
				"Time": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
			}, None)

			self.helpers.logger.info(
				entityType + " " + entity + " sensors update OK")
		else:
			self.helpers.logger.error(
				entityType + " " + entity + " sensors update KO")

	def amqpConsumeSet(self):
		""" Sets up the AMQP queue subscriptions. """

		self.channel.basic_consume('Life', self.lifeCallback,
							auto_ack=True)
		self.channel.basic_consume('Statuses', self.statusCallback,
							auto_ack=True)
		self.channel.basic_consume('Sensors', self.sensorsCallback,
							auto_ack=True)
		self.helpers.logger.info("AMQP consume setup!")

	def amqpConsumeStart(self):
		""" Starts consuming. """

		self.helpers.logger.info("AMQP consume starting!")
		self.channel.start_consuming()

	def amqpPublish(self, data, routing_key):
		""" Publishes to an AMQP broker queue. """

		self.channel.basic_publish(
			exchange=self.helpers.confs_core["iotJumpWay"]["amqp"]["exchange"], routing_key=routing_key, body=data)
		self.helpers.logger.info("AMQP publish complete!")
		threading.Timer(300.0, self.life).start()

	def life(self):
		""" Sends entity statistics to HIAS """

		cpu = psutil.cpu_percent()
		mem = psutil.virtual_memory()[2]
		hdd = psutil.disk_usage('/fserver').percent
		tmp = psutil.sensors_temperatures()['coretemp'][0].current
		r = requests.get('http://ipinfo.io/json?token=' +
				self.helpers.credentials["iotJumpWay"]["ipinfo"])
		data = r.json()
		location = data["loc"].split(',')

		self.amqpPublish(json.dumps({
			"Type": "Agent",
			"Id": self.credentials["iotJumpWay"]["entity"],
			"CPU": str(cpu),
			"Memory": str(mem),
			"Diskspace": str(hdd),
			"Temperature": str(tmp),
			"Latitude": float(location[0]),
			"Longitude": float(location[1])
		}), "Life")

		self.helpers.logger.info("Agent life statistics published.")

	def respond(self, responseCode, response):
		""" Returns the request repsonse """

		return Response(response=json.dumps(response, indent=4), status=responseCode,
						mimetype="application/json")

	def signal_handler(self, signal, frame):
		self.helpers.logger.info("Disconnecting")
		self.amqpPublish(json.dumps({"Type": "Agent", "Id": self.helpers.credentials["iotJumpWay"]["entity"],
									"Status": "OFFLINE"}), "Statuses")
		sys.exit(1)


app = Flask(__name__)
Agent = Agent("amqp")


@app.route('/About', methods=['GET'])
def about():
	"""
	Returns Agent details

	Responds to GET requests sent to the North Port About API endpoint.
	"""

	return Agent.respond(200, {
		"Identifier": Agent.credentials["iotJumpWay"]["entity"],
		"Host": Agent.credentials["server"]["ip"],
		"NorthPort": Agent.credentials["server"]["port"],
		"CPU": psutil.cpu_percent(),
		"Memory": psutil.virtual_memory()[2],
		"Diskspace": psutil.disk_usage('/').percent,
		"Temperature": psutil.sensors_temperatures()['coretemp'][0].current
	})


def main():

	signal.signal(signal.SIGINT, Agent.signal_handler)
	signal.signal(signal.SIGTERM, Agent.signal_handler)

	Agent.mongodbConn()
	Agent.hiascdiConn()
	Agent.hiasbchConn()
	Agent.amqpConn({
		"host": Agent.credentials["iotJumpWay"]["host"],
		"port": Agent.credentials["iotJumpWay"]["port"],
		"location": Agent.credentials["iotJumpWay"]["location"],
		"zone": Agent.credentials["iotJumpWay"]["zone"],
		"entity": Agent.credentials["iotJumpWay"]["entity"],
		"name": Agent.credentials["iotJumpWay"]["name"],
		"vhost": Agent.core_confs["iotJumpWay"]["amqp"]["vhost"],
		"un": Agent.credentials["iotJumpWay"]["un"],
		"up": Agent.credentials["iotJumpWay"]["up"]
	})
	Agent.amqpConsumeSet()

	Thread(target=Agent.life, args=(), daemon=True).start()
	Thread(target=Agent.amqpConsumeStart, args=(), daemon=True).start()

	app.run(host=Agent.helpers.credentials["server"]["ip"],
			port=Agent.helpers.credentials["server"]["port"])


if __name__ == "__main__":
	main()

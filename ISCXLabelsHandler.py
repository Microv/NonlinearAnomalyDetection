import xml.sax
import pytz
import datetime, calendar

TIMEZONE = "Canada/Atlantic"


class ISCXLabelsHandler(xml.sax.ContentHandler):


	def __init__(self, filename, attacks_dict, verbose=False):
		
		self.CurrentData = ''
		self.appName = ''
		self.source = ''
		self.destination = ''
		self.startDateTime = ''
		self.stopDateTime = ''
		self.label = ''

		self.filename = filename

		self.verbose = verbose

		self.attacks = attacks_dict


	def startElement(self, tag, attributes):
		
		self.CurrentData = tag
		if self.CurrentData == self.filename:
			self.appName = ''
			self.source = ''
			self.destination = ''
			self.startDateTime = ''
			self.stopDateTime = ''
			self.label = ''	

				
	def characters(self, content):
		
		if self.CurrentData == 'appName':
			self.appName += content
		elif self.CurrentData == 'source':
			self.source += content
		elif self.CurrentData == 'destination':
			self.destination += content
		elif self.CurrentData == 'startDateTime':
			self.startDateTime += content
		elif self.CurrentData == 'stopDateTime':
			self.stopDateTime += content	
		elif self.CurrentData == 'Tag':
			self.label = content


	def endElement(self, tag):

		if tag == self.filename:		
			if self.label == 'Attack':
				if self.source not in self.attacks:
					self.attacks[self.source] = dict()
					self.attacks[self.source][self.destination] = list()
				elif self.destination not in self.attacks[self.source]:
					self.attacks[self.source][self.destination] = list()

				start_timestamp = self.timestamp(self.startDateTime)
				stop_timestamp = self.timestamp(self.stopDateTime)	
				self.attacks[self.source][self.destination].append([start_timestamp,stop_timestamp])

				if self.verbose:
					print 'AppName: ' + self.appName
					print 'Source: ' + self.source
					print 'Destination: ' + self.destination
					print 'Start Date Time: ' + self.startDateTime
					print 'Start timestamp: '+str(start_timestamp)
					print 'Stop Date Time: ' + self.stopDateTime
					print 'Stop timestamp: '+str(stop_timestamp)
					print 'Label: ' + self.label 

		self.CurrentData = ''


	def timestamp(self, dateTime):
		
		local_tz = pytz.timezone(TIMEZONE)
		datetime_without_tz = datetime.datetime.strptime(dateTime, "%Y-%m-%dT%H:%M:%S")
		datetime_with_tz = local_tz.localize(datetime_without_tz, is_dst=None)
		datetime_in_utc = datetime_with_tz.astimezone(pytz.utc)
		timestamp = calendar.timegm(datetime_in_utc.timetuple())
		return timestamp


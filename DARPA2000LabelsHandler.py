import xml.sax
import pytz
import datetime, calendar

TIMEZONE = "America/New_York"


class DARPA2000LabelsHandler(xml.sax.ContentHandler):


	def __init__(self, attacks_dict, verbose=False):
		
		self.CurrentData = ''
		self.source = ''
		self.target = ''
		self.date = ''
		self.time = ''
		self.duration = ''

		self.verbose = verbose

		self.attacks = attacks_dict

		self.sourceNode = False
		self.targetNode = False


	def startElement(self, tag, attributes):
		
		self.CurrentData = tag
		if self.CurrentData == 'IDMEF-Message':
			self.source = ''
			self.target = ''
			self.date = ''
			self.time = ''
			self.duration = ''	

		elif self.CurrentData == 'Source':
			self.sourceNode = True

		elif self.CurrentData == 'Target':
			self.targetNode = True

		
	def characters(self, content):
		
		if self.CurrentData == 'date':
			self.date += content
		elif self.CurrentData == 'time':
			self.time += content
		elif self.CurrentData == 'sessionduration':
			self.duration += content	
		elif self.CurrentData == 'address':
			if self.sourceNode:
				self.source += content
			elif self.targetNode:
				self.target += content	
		

	def endElement(self, tag):

		if tag == 'IDMEF-Message':		
			
			if self.source not in self.attacks:
				self.attacks[self.source] = dict()
				self.attacks[self.source][self.target] = list()
			elif self.target not in self.attacks[self.source]:
				self.attacks[self.source][self.target] = list()

			start_timestamp = self.timestamp(self.date + 'T' + self.time)
			duration_timestamp = self.timestamp('01/01/1970' + 'T' + self.duration)	
			stop_timestamp = start_timestamp + duration_timestamp
			self.attacks[self.source][self.target].append([start_timestamp,stop_timestamp])

			if self.verbose:
				print 'Source: ' + self.source
				print 'Target: ' + self.target
				print 'Start Date Time: ' + self.date + ' - '+ self.time + ' (' + str(start_timestamp) + ')' 
				print 'Dutation: ' + self.duration + ' (' + str(stop_timestamp) + ')'

		elif tag == 'Source':
			self.sourceNode = False

		elif tag == 'Target':
			self.targetNode = False

		self.CurrentData = ''


	def timestamp(self, dateTime):
		
		local_tz = pytz.timezone(TIMEZONE)
		datetime_without_tz = datetime.datetime.strptime(dateTime, "%m/%d/%YT%H:%M:%S")
		datetime_with_tz = local_tz.localize(datetime_without_tz, is_dst=None)
		datetime_in_utc = datetime_with_tz.astimezone(pytz.utc)
		timestamp = calendar.timegm(datetime_in_utc.timetuple())
		return timestamp



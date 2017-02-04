import xml.sax

class FNHandler(xml.sax.ContentHandler):


	def __init__(self, filename, false_negatives, false_positives, anomalies, normal, verbose=False):
		
		self.CurrentData = ''
		self.actual_label = ''
		self.predicted_label = ''
		self.timestamp = ''

		self.root = False

		self.filename = filename

		self.false_negatives = false_negatives
		self.false_positives = false_positives
		self.anomalies = anomalies
		self.normal = normal

		self.verbose = verbose


	def startElement(self, tag, attributes):
		
		self.CurrentData = tag
		if self.CurrentData == 'prediction':
			if attributes.get("index"):
				self.actual_label = ''
				self.predicted_label = ''
				self.timestamp = ''

				self.root = True

			else:
				self.root = False

				
	def characters(self, content):
		
		if self.CurrentData == 'actual_label':
			self.actual_label += content
		elif self.CurrentData == 'predicted_label':
			self.predicted_label += content
		elif self.CurrentData == 'attribute':
			self.timestamp += content	


	def endElement(self, tag):

		if tag == 'prediction':
			
			if self.root:
				if self.actual_label == self.predicted_label:
					if self.actual_label == 'anomaly':
						self.anomalies.append(self.timestamp)
					else:
						self.normal.append(self.timestamp)
				elif self.actual_label == 'anomaly':
					self.false_negatives.append(self.timestamp)

					if self.verbose:
						print 'actual_label: ' + self.actual_label
						print 'predicted label: ' + self.predicted_label
						print 'timestamp: ' + self.timestamp

				else:
					self.false_positives.append(self.timestamp)
			else:
				self.root = True

		self.CurrentData = ''



def falsefalseNegatives(false_negatives, anomalies):

	WINDOW_DIM = 180

	fn = len(false_negatives)
	print 'Initial False Negatives:', fn 

	for ts_fn in false_negatives:
		ts_fn = float(ts_fn)
		for ts_an in anomalies:
			ts_an = float(ts_an)
			if ts_an < ts_fn:
				if ts_fn <= ts_an + WINDOW_DIM:
					if verbose:
						print 'False False negative:', ts_fn, ts_an
					fn -=1
					break
			else:
				if ts_an <= ts_fn + WINDOW_DIM:
					if verbose:
						print 'False False negative:', ts_fn, ts_an
					fn -=1
					break

	print 'Final False Negatives:', fn


def generateCSV(false_positives, false_negatives, anomalies, normal):

	total = false_positives + false_negatives + anomalies + normal
	total.sort()

	with open('FNFP.csv', 'wb') as f:
		for ts in total:
			l = ''
			if ts in anomalies:
				l = 'anomaly'
			elif ts in normal:
				l = 'normal'
			elif ts in false_positives:
				l = 'FP'
			elif ts in false_negatives:
				l = 'FN'
			
			line = str(ts) + ';' + l + '\n'
			f.write(line)


if __name__ == "__main__":
	
	parser = xml.sax.make_parser()
	file = 'prediction.xml'
	false_negatives = list()
	false_positives = list()
	anomalies = list()
	normal = list()
	verbose = True
	parser.setContentHandler(FNHandler(file, false_negatives, false_positives, anomalies, normal, verbose))
	parser.parse(file)
	
	falsefalseNegatives(false_negatives, anomalies)

	generateCSV(false_positives, false_negatives, anomalies, normal)	

	






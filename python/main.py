import csv,datetime,json,pytz,xml.etree.ElementTree as ET

# 1: Python method that takes arguments int X and int Y, and updates DEPART and RETURN fields in test_payload1.xml:

def csv_update_file(x,y):
	element_tree = ET.parse('test_payload1.xml')
	root_element = element_tree.getroot()
	update_csv_values(root_element,x,y)
	result_xml = ET.tostring(root_element)
	with open("test_payload2.xml", "wb") as f:
    		f.write(result_xml)

def update_csv_values(root_element,x,y):
	for element in root_element:
		if(element.tag=='DEPART'):
			element.text=(datetime.datetime.now() + datetime.timedelta(days=x)).strftime('%Y%m%d')
		elif(element.tag=='RETURN'):
			element.text=(datetime.datetime.now() + datetime.timedelta(days=y)).strftime('%Y%m%d')
		update_csv_values(element,x,y)

# 2: Python method that takes a json element as an argument, and removes that element from test_payload.json.
		
def json_delete_attribute(x): 
	json_file = open('test_payload.json')
	json_data = json.load(json_file)
	delete_inner_json(json_data,x)
	with open("test_payload2.json", "w") as outfile:
    		json.dump(json_data, outfile)
	json_file.close()

def delete_inner_json(json_data,x):
	if x in json_data:
		del json_data[x]
	for json_field in json_data:
		if isinstance(json_data[json_field],dict):
			delete_inner_json(json_data[json_field],x)

# 3: Python script that parses jmeter log files in CSV format, and in the case if there are any non-successful endpoint responses recorded in the log, prints out the label, response code, response message, failure message, and the time of non-200 response in human-readable format in PST timezone (e.g. 2021-02-09 06:02:55 PST).

def update_jmeter_log(file_name):
	log_file = open(file_name)
	csvreader = csv.reader(log_file)
	header = next(csvreader)
	for row in csvreader:
		if(not row[header.index("responseCode")]=='200'):
			utc_datetime = datetime.datetime.utcfromtimestamp(float(row[header.index("timeStamp")]) / 1000.)
			row[header.index("timeStamp")] = utc_datetime.replace(tzinfo=pytz.timezone('UTC')).astimezone(pytz.timezone('America/Los_Angeles')).strftime('%Y-%m-%d %H:%M:%S %Z')
			print(row[header.index("timeStamp")],row[header.index("label")],row[header.index("responseCode")],row[header.index("responseMessage")],row[header.index("failureMessage")],sep=', ')
	log_file.close()

csv_update_file(1,2)
json_delete_attribute('appdate')
update_jmeter_log("Jmeter_log1.jtl")
update_jmeter_log("Jmeter_log2.jtl")











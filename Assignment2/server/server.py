from xmlrpc.server import SimpleXMLRPCServer
import xml.etree.ElementTree as ET
import requests

# Initialize XML tree
try:
    tree = ET.parse('database.xml')
    root = tree.getroot()
except ET.ParseError:
    root = ET.Element("root")
    tree = ET.ElementTree(root)

def save_data(topic, text, timestamp):
    # Check if topic exists
    for child in root:
        if child.tag == topic:
            # Append data
            ET.SubElement(child, "note", timestamp=timestamp).text = text
            tree.write("database.xml")
            return "Data saved successfully"
    # If topic does not exist, create new entry
    new_topic = ET.SubElement(root, topic)
    ET.SubElement(new_topic, "note", timestamp=timestamp).text = text
    tree.write("database.xml")
    return "Data saved successfully"

def get_data(topic):
    for child in root:
        if child.tag == topic:
            return ET.tostring(child, encoding='utf8').decode('utf8')
    return "Topic not found"

def query_wikipedia(search_term):
    response = requests.get(
        'https://en.wikipedia.org/w/api.php',
        params={
            'action': 'opensearch',
            'search': search_term,
            'limit': '1',
            'namespace': '0',
            'format': 'json'
        }
    ).json()
    return response[3][0] if response[3] else "No results found"

server = SimpleXMLRPCServer(("localhost", 8000))
print("Listening on port 8000...")

# Registers functions to be called by the client
server.register_function(save_data, "save_data")
server.register_function(get_data, "get_data")
server.register_function(query_wikipedia, "query_wikipedia")

server.serve_forever()
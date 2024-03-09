## Assignment 2 - RPC (Remote Procedure Calls)

# Basic Requirements ( 1-7 points )
The client should be able to:

Ask the user for input & send it to server
        Topic, Text, and timestamp for the note
        If the topic exists on the XML, the data will be appended to the structure
        If not, a new XML entry will be made
Get the contents of the XML database based on given topic
The server should be able to:

Process the client's input
Save data on a local database mock (XML)
Handle multiple client requests at once
Attached on the assignment page is an XML file, that shows how the XML database mock could be structured.

Additional requirements ( 8-10 points )
One of the key challenges in distributed systems is the interoperability of different platforms. For full marks on this assignment, the server should communicate with other sources of data for information. Add a functionality, that will query the Wikipedia API for more information of the given topic. For this tasks, an additional library can be used for queries, such as 'requests' on python or 'fetch' on Javascript.

The client should be able to:

Name search terms to lookup data on wikipedia
Append the data to an existing topic
The server should be able to:

Query wikipedia for user submitted articles
Add relevant information to user submitted topic
        At minimum, the server should give a link to a wikipedia article found
How usable the Wikipedia results are is not a priority, the main idea is to communicate through the API. Opensearch protocol, which is available in the link below, is good enough for this assignment.

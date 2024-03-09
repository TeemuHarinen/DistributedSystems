# Assignment 2 - RPC (Remote Procedure Calls)

## Basic Requirements ( 1-7 points )
The client should be able to:

Ask the user for input & send it to server
- Topic, Text, and timestamp for the note
- If the topic exists on the XML, the data will be appended to the structure
- If not, a new XML entry will be made
- Get the contents of the XML database based on given topic

The server should be able to:

Process the client's input

Save data on a local database mock (XML)

Handle multiple client requests at once

Additional requirements ( 8-10 points )

The client should be able to:
- Name search terms to lookup data on wikipedia
- Append the data to an existing topic
  
The server should be able to:
- Query wikipedia for user submitted articles
- Add relevant information to user submitted topic
At minimum, the server should give a link to a wikipedia article found


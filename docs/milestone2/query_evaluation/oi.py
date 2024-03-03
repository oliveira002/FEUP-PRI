import requests
import webbrowser

solr_url = "http://localhost:8983/solr/games/select?defType=edismax&fl=*%2Cscore&indent=true&lowercaseOperators=true&q.op=AND&q=(historical)%20and%20(command)%20and%20army&qf=full_desc%20desc&rows=5000&useParams=&wt=json"

# Make a GET request to Solr
response = requests.get(solr_url)

# Check if the request was successful
if response.status_code == 200:
    # Parse JSON data from the response
    json_data = response.json()
    
    # Extract URLs from the JSON data
    urls = [doc['url'] for doc in json_data['response']['docs']]
    ids = [doc['id'] for doc in json_data['response']['docs']]
    # Loop through each URL
    for i in range(len(urls)):
        url = urls[i]
        print(ids[i])

        # Open the URL in the default web browser
        webbrowser.open(url)

        # Wait for the user to press Enter before moving on to the next URL
        input("Press Enter to open the next URL...")
else:
    print(f"Error: Unable to fetch data from Solr. Status code: {response.status_code}")
import os, requests, sys

def main():

    if not os.path.exists('assets/api_key.txt'):
        print("Error: No API key file found. Creating 'assets/api_key.txt'")
        print("Please save your API key in the newly created file.")
        print("Where to get an API key: https://www.yelp.com/developers/v3/manage_app ")
        sys.exit()

    with open('assets/api_key.txt', "r") as f:
        yelp_api_key = f.read()

    if len(yelp_api_key) < 2:
        print("No API key found. Aborting")
        sys.exit()


    latitude = "30.4020695"
    longitude = "-97.7280716"

    headers = {'Authorization': "Bearer {}".format(yelp_api_key)}
    #r = requests.get("https://api.yelp.com/v3/businesses/search?term=coffee&latitude="+latitude+"&longitude="+longitude, headers=headers)
    r = requests.get("https://api.yelp.com/v3/businesses/search?term=coffee&latitude={}&longitude={}".format(latitude,longitude), headers=headers)
    # r = requests.get("https://api.yelp.com/v3/businesses/search?term=coffee&latitude=30.4020695&longitude=-97.7280716"+longitude, headers=headers)

    response = r.json()
    max_businesses = response['total']

    leads = []
    i = 0
    k = 0
    while i < max_businesses:
        r = requests.get("https://api.yelp.com/v3/businesses/search?term=coffee&limit=50&offset={}&latitude={}&longitude={}".format(i, latitude, longitude), headers=headers)
        print("Retrieving results {}-{}".format(k,i+50))
        if r.status_code != 200:
            print("Status code: ", r.status_code)
            print("exiting")
            break
        response = r.json()
        businesses = response['businesses']
        for item in businesses:
            leads.append((item['name'], item['phone']))

        i = i+50
        k = k+50




    leads.sort(key=lambda x:x[0])

    if not os.path.exists('assets/coffee_leads.txt'):
        with open('assets/coffee_leads.txt', 'w') as f:
            f.write("            Business             |      Phone Number")
            f.write("=====================================================\n")
            f.close()

    print("Finished. Writing to file")
    with open('assets/coffee_leads.txt', 'a+') as f:
        for x,y in leads:
            f.write("{:<33} {:^15}\n".format(x,y))
        f.close()

main()

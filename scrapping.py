import requests
import json
import urllib.request
import bs4 as bs
#page_number used for changing cookie value every time
page_number=0
hotel_sublink=[]
condition_terminator=0
start=0
main_l=[]
# con=1 will fetch 10 hotel details, con=2 will fetch 20 and so on
con = 1

#loading the list link of each hotel
while condition_terminator<con:
    cookies = {
    'countly_webapp_uid': 'zFvndbjGkmH_tgqIjnezaLPj-WH0jwI-',
    'pwa': '0',
    'mobilecityselect': 'bangalore',
    'city_name': 'bangalore',
    'listingViewNumber': '1',
    'connect.sid': 's%3AzFvndbjGkmH_tgqIjnezaLPj-WH0jwI-.YftpYAWSoLbkhycazJP0e9tRgOg4NEGefGBpfgq6rXg',
    '_col_uuid': '879bb692-3a99-4718-a673-bab7103040c5-10wuc~1',
    'G_ENABLED_IDPS': 'google',
    '_ga': 'GA1.3.1035190905.1531752683',
    'QGUserId': '%228572787971574785%22',
    '_qg_cm': '1',
    '_qg_qaid': '%228lDj7XBdXK9yojFFbNhj6Q%22',
    'optimizelyEndUserId': 'oeu1531752751977r0.6129664497776177',
    '_gid': 'GA1.3.1146162489.1531897370',
    '_hjIncludedInSample': '1',
    'city_id': '2',
    'okgotit': '1',
    'rdpViewNumber': '1',
    '_gat': '1',
    '_qg_pushrequest': 'true',
    }
    cookies['listingViewNumber'] =  str(page_number)

    headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0',
    'Accept': '*/*',
    'Accept-Language': 'en-GB,en;q=0.5',
    'Referer': 'https://www.dineout.co.in/bangalore-restaurants',
    'Content-Type': 'application/json; charset=utf-8',
    'X-Requested-With': 'XMLHttpRequest',
    'Connection': 'keep-alive',
    }

    data = '{"callType":"POST","form":{"city_name":"bangalore","limit":10,"d-id":"zFvndbjGkmH_tgqIjnezaLPj-WH0jwI-","start":'+str(start)+'},"header":{"Content-Type":"application/json","img_width":400,"d_type":"web","elat":"12.971650","elng":"77.594595"}}'

#making API Request using above header and cookie parameters
    try:
        response = requests.post('https://www.dineout.co.in/xhr/nodeApi/v24/search', headers=headers, cookies=cookies, data=data)
        res_json = json.loads(response.text)
	#rdp_link is the sublink of each hotel eg: "/bangalore-restaurants"
        for i in res_json['data']['RESTAURANT']['listing']:
            hotel_sublink.append(i['rdp_link'])
    except requests.exceptions.RequestException as e:
        break
    page_number=page_number+1
    condition_terminator=condition_terminator+1
    start=start+10

#looping in the hotel sublink to fetch all details of hotel like rating,name,latitude etc
for lin in hotel_sublink:
    sauce2 = urllib.request.urlopen("https://www.dineout.co.in" + lin).read()
    soup2 = bs.BeautifulSoup(sauce2, 'lxml')
    for i in soup2.find_all('div', class_='rating-5'):
        if (i.text != ''):
            rating = i.text
    for i in soup2.find_all('h1', class_='restnt-name'):
            name = i.text
    for i in soup2.find_all('span', class_='address-info'):
            location = i.text
    for i in soup2.find_all('a', class_='pull-right'):
            tvar = i.get('href')
            tvar = tvar.split('=')
            if len(tvar) >= 2:
                tvar = tvar[1].split(',')
                latitude = tvar[0]
                longitude = tvar[1]
            else:
                continue
    urls = "https://www.dineout.co.in" + lin
    #main_l contains the list od dictionary having hotel details
    main_l.append({"name":name,"rating":rating,"location":location,"latitude":latitude,"longitude":longitude,"urls":urls})
#writing into json format
file = open("final_json.json",'w')
file.write(json.dumps(main_l))

#the values generated in final_json.json can be copied and posted in the API using the API link.

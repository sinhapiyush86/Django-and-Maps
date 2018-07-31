from django.shortcuts import render
from hotel_locations.models import Details_Table
import bs4 as bs
from django.http import HttpResponse
import requests
import json
import urllib.request
# Create your views here.

#scrapping function to scrap data working on same principle as scrapping.py file
def scrapping(request):

    page_number = 0
    l = 0
    start=0
    while True:
        cookies = {
            'countly_webapp_uid': 'zFvndbjGkmH_tgqIjnezaLPj-WH0jwI-',
            'pwa': '0',
            'mobilecityselect': 'bangalore',
            'city_name': 'bangalore',
            'listingViewNumber': '0',
            'connect.sid': 's%3AzFvndbjGkmH_tgqIjnezaLPj-WH0jwI-.YftpYAWSoLbkhycazJP0e9tRgOg4NEGefGBpfgq6rXg',
            '_col_uuid': '879bb692-3a99-4718-a673-bab7103040c5-10wuc~1',
            'G_ENABLED_IDPS': 'google',
            '_ga': 'GA1.3.1035190905.1531752683',
            'QGUserId': '%228572787971574785%22',
            '_qg_cm': '1',
            '_qg_qaid': '%228lDj7XBdXK9yojFFbNhj6Q%22',
            'optimizelyEndUserId': 'oeu1531752751977r0.6129664497776177',
            '_gid': 'GA1.3.1146162489.1531897370',
            '_gat': '1',
        }
        cookies['listingViewNumber'] = str(page_number)

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

        try:
            response = requests.post('https://www.dineout.co.in/xhr/nodeApi/v24/search', headers=headers,
                                     cookies=cookies, data=data)
            t = json.loads(response.text)
            for lin in t['data']['RESTAURANT']['listing']:
                model = Details_Table()
                sauce2 = urllib.request.urlopen("https://www.dineout.co.in" + lin['rdp_link']).read()
                soup2 = bs.BeautifulSoup(sauce2, 'lxml')
                for i in soup2.find_all('div', class_='rating-5'):
                    if (i.text != ''):
                        model.rating = i.text
                for i in soup2.find_all('h1', class_='restnt-name'):
                    model.name = i.text
                for i in soup2.find_all('span', class_='address-info'):
                    model.location = i.text
                for i in soup2.find_all('a', class_='pull-right'):
                    tvar = i.get('href')
                    tvar = tvar.split('=')
                    if len(tvar) >= 2:
                        tvar = tvar[1].split(',')
                        model.latitude = tvar[0]
                        model.longitude = tvar[1]
                    else:
                        continue
                model.urls = "https://www.dineout.co.in" + lin['rdp_link']
                model.save()
        except requests.exceptions.RequestException as e:
            break
        page_number = page_number + 1
        start = start+10


   # sauce = urllib.request.urlopen("https://www.dineout.co.in/bangalore-restaurants?search_str=").read()
    #soup = bs.BeautifulSoup(sauce, 'lxml')
    #x = set({})
    #for i in soup.find_all('div', class_='right-details'):
     #   x.add(i['data-url'])
    #for j in x:



    return HttpResponse("Succesfully added")
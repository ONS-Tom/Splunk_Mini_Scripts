#!/usr/bin/env python




import json
import urllib2
import urllib
import splunklib.client as client
import sys
import logging


logger = logging.getLogger("Locu")
logger.setLevel(logging.INFO)
Locu_log = logging.FileHandler('Locu.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
Locu_log.setFormatter(formatter)
logger.addHandler(Locu_log)



city = 'Enter a city to query'
api_key = 'Your API Key'
host = 'Your host'
port = 'Splunk mgmt port'
username = 'Splunk username'
password = 'splunk pw'


def locu_data():
    
    try:
    
        PH = urllib2.ProxyHandler({}) # If proxied environment add proxy info here
        PO = urllib2.build_opener(PH)
        urllib2.install_opener(PO)
        local_business_data='https://api.locu.com/v1_0/venue/search/?locality='+city+'&api_key='+api_key
        print 'Querying Locu....Please wait'
        open_local_business_data=urllib2.urlopen(local_business_data)
        data_load=json.load(open_local_business_data)
        Business = [x for x in data_load['objects']]
        logger.info ('Connection to Locu initiated')
        return Business
    except Exception as error:
        logger.error(error)

def event_gen():
    data=locu_data()
    len_data=len(data)
    while len_data > 0:
        for line2 in data:
            len_data=len_data-1
            try:
                cat=[x.encode('UTF8') for x in line2['categories']]
                yield ('Name = {},Locality = {}, Website = {}, Address = {}, Zip Code = {},Phone = {},Longitude = {},Latitude = {},Categories = {} \n'.format(line2['name'],line2['locality'],line2['website_url'],line2['street_address'],line2['postal_code'],line2['phone'],line2['long'],line2['lat'],[cat])).replace('[', '').replace(']','')
            except Exception as error:
                if error == UnicodeEncodeError:
                   line2['name'].encode('UTF8')
                else :
                    logger.error(error)


def splunk_connect():
    logger.info('Initiating contact with Splunk')
    
    try:
        service=client.connect(
                           host=host,
                           port=port,
                           username=username,
                           password=password)
        print 'Connecting to Splunk, please wait'
        return service
    except Exception as error :
        logger.error(error)


def splunk_push(idx, st):
    
    data = event_gen()
    service=splunk_connect()
    target=service.indexes[idx]
    sourcetype=st
    
    try:
        for line in data:
            target.submit(event=str(line),sourcetype=sourcetype)
        print 'Data push to Splunk is complete'
    except Exception as error :
        logger.error(error)



if __name__ == '__main__':

    splunk_push('locu', 'locu_api')





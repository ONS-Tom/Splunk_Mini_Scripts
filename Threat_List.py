

#Scripted Lookup
#Proxied and nonproxied environments
# Change Title to scripted lookup 




import csv
import re
import urllib2
import urllib


#Future enhancement:Use the csv module and readline function
#Pass functions

URL =['http://www.nothink.org/blacklist/blacklist_malware_dns.txt']
#,'https://zeustracker.abuse.ch/blocklist.php?download=baddomains']
splunk_home = '/opt/splunk'
app = '/etc/apps/SplunkEnterpriseSecuritySuite'
domain_lookup = '/lookups/domains.csv'
ip_lookup = '/lookups/ips.csv'
download_file = '/lookups/threat_list_download.csv'
PH=urllib2.ProxyHandler({})
PO=urllib2.build_opener(PH)
urllib2.install_opener(PO)



def download_threat():
    for item in URL:
        download = open(splunk_home+app+download_file, 'w')
        read_domain = urllib2.urlopen(item)
        for threat in read_domain:
            download.write(threat)
        return download


def main():
    download = open(splunk_home+app+download_file, 'r')
    threat_domain = csv.writer(open(splunk_home+app+domain_lookup, 'wb'))
    threat_domain.writerow(['Domain'])
    threat_ip = csv.writer(open(splunk_home+app+ip_lookup, 'wb'))
    threat_ip.writerow(['IP'])
    for line in download:
        ip_address = re.match('(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})',line)
        exclude = re.match('(^#)',line)
        if ip_address:
            threat_ip.writerow([line.strip("\n")])
        elif exclude:
            pass
        else:
            threat_domain.writerow([line.strip("\n")])
   

if __name__ == '__main__':

    download_threat()  
    main()
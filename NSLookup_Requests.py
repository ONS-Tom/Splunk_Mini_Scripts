


# Will Edit and use CSV writer

from socket import gethostbyname
import re
import requests

#URL_TEST=https://zeustracker.abuse.ch/blocklist.php?download=baddomains

URL = 'http://www.nothink.org/blacklist/blacklist_malware_dns.txt'
splunk_home = '/opt/splunk'
app = '/etc/apps/SplunkEnterpriseSecuritySuite'
domain_lookup = '/lookups/domains.csv'
ip_lookup = '/lookups/ips.csv'




def main():
    
    threat_list = open(splunk_home+app+domain_lookup, 'r+')
    threat_ip = open(splunk_home+app+ip_lookup, 'w')
    read_domain = requests.get(URL, verify=False)
    for line in read_domain:
        threat_list.write(line)
        for threat in threat_list:
            ip_address = re.match('(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}?)',threat)
            exclude = re.match('(^#)',threat)
            if ip_address:
                threat_ip.write(threat)
            elif exclude:
                pass
            else:
                new = threat.strip('\n')
                try:
                    ip = gethostbyname(new)
                    print ip
                except:
                    print threat












main()
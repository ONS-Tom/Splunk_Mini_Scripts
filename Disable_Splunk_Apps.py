#!/usr/bin/env python

import re
import os
import errno


local_dir='/opt/splunk/etc/apps/'
directory= os.listdir('/opt/splunk/etc/apps/')
exclude = ['.','..','.DS_Store','search','launch','user-prefs','Splunk_TA_sourcefire','SplunkEnterpriseSecuritySuite','introspection_generator_addon','framework','gettingstarted']

for app in directory:
    if app not in exclude:
        
        try:
            app_conf_default=open('/opt/splunk/etc/apps/'+app+'/default/app.conf','r')
            for line in app_conf_default:
                if re.match("state\s=\senabled",line): #Splunk enables by default.
                    #replace =re.sub("state = enabled","state = disabled",line)
                    app_conf_local=open('/opt/splunk/etc/apps/'+app+'/local/app.conf','w')
                    app_conf_local.write('[install]\n state = disabled')
                    print app+" "+ "is now disabled"
        
        except IOError as exception:
            
            try:
                if exception.errno ==20 or exception.errno ==2 :
                    os.mkdir(local_dir+app+'/local',755);
                    app_conf_local=open('/opt/splunk/etc/apps/'+app+'/local/app.conf','w')
                    app_conf_local.write('[install]\n state = disabled')
            
                else:
                    raise

            except (OSError)as exception:
                if exception.errno == 17:
                    print app+":unable to be disabled. Please review the app's folder for more details."

                else:
                  raise

                
                
                app_conf_local.close()
                app_conf_default.close()
    else:
        print  app+" "+ "is not allowed to be changed!"









    
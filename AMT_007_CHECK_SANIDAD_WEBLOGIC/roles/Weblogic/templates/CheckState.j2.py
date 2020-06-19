import os
import weblogic.security.internal.SerializedSystemIni
import weblogic.security.internal.encryption.ClearOrEncryptedService
import os.path
import urllib2

def decrypt(domainHomeName, encryptedPwd):
    domainHomeAbsolutePath = os.path.abspath(domainHomeName)
    encryptionService = weblogic.security.internal.SerializedSystemIni.getEncryptionService(domainHomeAbsolutePath)
    ces = weblogic.security.internal.encryption.ClearOrEncryptedService(encryptionService)
    clear = ces.decrypt(encryptedPwd)
    return clear

def VersionWeblogic():
	Java = os.popen("ps -fe | grep weblogic | grep -v grep | grep jdk | awk '{print $8}' | sed -n 1p").read().rstrip('\n')
	VersionWB = os.popen(Java + " -cp "+ ORACLE +"/wlserver/server/lib/weblogic.jar weblogic.version  | sed -n 2p").read().rstrip('\n')
	return VersionWB

def HTML(File,Domain,Port):
	if Port == '7001':
		CreateHTML = open(FileHTML,"a")
		CreateHTML.write('<tr><th colspan="6" class="Domain">DOMINIO: ' + Domain + '</th></tr><tr><th colspan="3">PUERTO ADMIN</th><th colspan="3">DEFAULT</th></tr><tr><td colspan="3">'+Port+'</td><td colspan="3" class="YELLOW">DEFECTO</td></tr><tr><th colspan="6">SERVERS</th></tr><tr><th>SERVER NAME</th><th colspan="1">STATE1</th><th>STATE2</th><th>PORT HTTP</th><th>PORT SSL</th><th>%USO JVM</th></tr>')
		CreateHTML.close()
	else:
		CreateHTML = open(FileHTML,"a")
		CreateHTML.write('<tr><th colspan="6" class="Domain">DOMINIO: ' + Domain + '</th></tr><tr><th colspan="3">PUERTO ADMIN</th><th colspan="3">DEFAULT</th></tr><tr><td colspan="3">'+Port+'</td><td colspan="3">OK</td></tr><tr><th colspan="6">SERVERS</th></tr><tr><th>SERVER NAME</th><th colspan="1">STATE1</th><th>STATE2</th><th>PORT HTTP</th><th>PORT SSL</th><th>%USO JVM</th></tr>')
		CreateHTML.close()

def HTML_SERVER(Server_N,State1,State2,HTTP,SSL,JVM):
	if State1 == 'RUNNING':
		if State2 == 'HEALTH_OK':
			CreateHTML = open(FileHTML,"a")
			CreateHTML.write('<tr><td>'+ Server_N +'</td><td class="GREEN" colspan="1">'+ State1 +'</td><td class="GREEN">'+ State2 +'</td><td>'+ HTTP +'</td><td>'+ SSL +'</td><td>' + JVM + '%</td></tr>')
			CreateHTML.close()
		else:
			CreateHTML = open(FileHTML,"a")
			CreateHTML.write('<tr><td>'+ Server_N +'</td><td class="GREEN" colspan="1">'+ State1 +'</td><td class="RED">'+ State2 +'</td><td>'+ HTTP +'</td><td>'+ SSL +'</td><td>' + JVM + '%</td></tr>')
			CreateHTML.close()
	elif State1 == 'ADMIN':
		if State2 == 'HEALTH_OK':
			CreateHTML = open(FileHTML,"a")
			CreateHTML.write('<tr><td>'+ Server_N +'</td><td class="YELLOW" colspan="1">'+ State1 +'</td><td class="GREEN">'+ State2 +'</td><td>'+ HTTP +'</td><td>'+ SSL +'</td><td>' + JVM + '%</td></tr>')
			CreateHTML.close()
		else:
			CreateHTML = open(FileHTML,"a")
			CreateHTML.write('<tr><td>'+ Server_N +'</td><td class="YELLOW" colspan="1">'+ State1 +'</td><td class="RED">'+ State2 +'</td><td>'+ HTTP +'</td><td>'+ SSL +'</td><td>' + JVM + '%</td></tr>')
			CreateHTML.close()	
	elif State1 == 'SHUTDOWN':
		CreateHTML = open(FileHTML,"a")
		CreateHTML.write('<tr><td>'+ Server_N +'</td><td class="RED" colspan="1">'+ State1 +'</td><td class="RED">'+ State2 +'</td><td>'+ HTTP +'</td><td>'+ SSL +'</td><td>' + JVM + '</td></tr>')
		CreateHTML.close()

def HTML_APP(APP_NAME,State,Server_NAME):
	CreateHTML = open(FileHTML,"a")
	CreateHTML.write('<tr><td colspan="2">'+ APP_NAME +'</td><td colspan="2">'+ State +'</td><td colspan="2">'+ Server_NAME +'</td>')
	CreateHTML.close()

def HTML_JDBC(DS_Name, DS_State, DS_Server):
	CreateHTML = open(FileHTML,"a")
	CreateHTML.write('<tr><td colspan="2">'+ DS_Name +'</td><td colspan="2">'+ DS_State +'</td><td colspan="2">'+ DS_Server +'</td></tr>')
	CreateHTML.close()

def HealthServer(S_Health):
	Num_Car = int(S_Health.find('H'))
	StateHealth = S_Health.replace(S_Health[0:Num_Car],'')
	SHealth = int(StateHealth.find(','))
	End_Health = str(StateHealth[0:SHealth])
	return End_Health

Domains = "{{ DOMAIN_BASE.stdout }}"
ORACLE = "{{ MW_HOME.stdout }}"
Date = "{{ DATE.stdout }}"
NumberD = int(os.popen('ls -l '+ Domains +' | grep -v .tar | grep -v .gz | grep -v .zip | grep -v core | sed 1d | wc -l').read())
File = "boot.properties"
JDServer = 'NONE'
FileHTML = ("/tmp/Check_WeblogicP_"+Date+".html")
VWB = VersionWeblogic()

CreateHTML = open(FileHTML,"w")
CreateHTML.write('<tr>\n<th colspan="2">VERSION WEBLOGIC</th>\n<th colspan="2">ORACLE_HOME</th>\n<th colspan="2">RUTE DOMAINS</th>\n</tr>\n<tr>\n<td colspan="2">'+ VWB +'</td><td colspan="2">'+ ORACLE +'</td><td colspan="2">'+Domains+'</td></tr>')
CreateHTML.close()

for x in range(NumberD + 1):
	NDomain = os.popen("ls -l "+ Domains +" | grep -v .tar | grep -v .gz | grep -v .zip | sed 1d | sed -n "+ str(x) +"p | awk '{print $9}'").read().rstrip('\n')
	if NDomain == '':
		print('Se omite entrada')
	else:
		try:
			CDomains = (Domains+'/'+NDomain+'/servers/')
			DCDomains = (Domains+'/'+NDomain)
			Port = os.popen("grep 'ADMIN_URL=' "+ DCDomains+"/bin/stopWebLogic.sh | sed -n 2p | sed 's/ADMIN_URL=//g'| awk -F : '{print $3}'").read().rstrip('\n').rstrip('"')
			LISTENPORT = os.popen("grep 'ADMIN_URL=' "+ DCDomains+"/bin/stopWebLogic.sh | sed -n 2p | sed 's/ADMIN_URL=//g'| awk -F : '{print $2}' | sed 's=//==g'").read().rstrip('\n')
			NAME_SERVER = os.popen("grep admin-server-name "+ DCDomains+"/config/config.xml | sed 's/<admin-server-name>//g' | sed 's=</admin-server-name>==g' | sed -n 1p | awk '{print $1}'").read().rstrip('\n')
			CDServer = os.popen("ls -l " + CDomains + "| grep -v domain_bak| awk '{print $9}' | sed 1d | sed -n 1p").read().rstrip('\n')
			FileCDS = (str(CDomains) + '/' + str(CDServer) + '/security/boot.properties')
			Username = os.popen('cat ' + FileCDS + "| grep 'username=' | awk -F username= '{print $2}'").read().replace('\\','')
			Pass = os.popen('cat ' + FileCDS + "| grep 'password=' |awk -F password= '{print $2}'").read().replace('\\','')
			UserD = decrypt(DCDomains, Username)
			PassD = decrypt(DCDomains, Pass)
			connect( UserD , PassD , url='t3://'+LISTENPORT+':'+Port+'')
			HTML(FileHTML,NDomain,Port)
			serverConfig()
			servers=cmo.getServers()
			for Server in servers:
				ServerName=Server.getName()
				domainRuntime()
				bean=getMBean('/ServerLifeCycleRuntimes/'+ServerName)
				bean1=getMBean('/ServerRuntimes/'+ServerName)
				bean2=getMBean('/ServerRuntimes/' + ServerName + '/JVMRuntime/' + ServerName)
				ServerState=str(bean.getState())
				if ServerState == 'RUNNING' or ServerState == 'ADMIN':
					ServerHealth=str(bean1.getHealthState())
					EndHealth = 'SHUTDOWN'
					for Health in str(bean1.getHealthState()).split(':'):
						if 'HEALTH' in Health:
							EndHealth = Health.split(',')[0]
					#EndHealth = str(HealthServer(ServerHealth))
					PortHTTPS = str(bean1.getSSLListenPort())
					JVMUSE = str(100 - int(bean2.getHeapFreePercent()))
				else:
					EndHealth = 'SHUTDOWN'
					PortHTTPS = 'NONE'
					JVMUSE = 'NONE'
				serverConfig()
				PortHTTP = str(Server.getListenPort())
				HTML_SERVER(ServerName,ServerState,EndHealth,PortHTTP,PortHTTPS,JVMUSE)
			CreateHTML = open(FileHTML,"a")
			CreateHTML.write('<tr><th colspan="6">APLICACIONES</th></tr><tr><th colspan="2">APPLICATION NAME</th><th colspan="2">STATE</th><th colspan="2">SERVER</th></tr>')
			CreateHTML.close()
			myapps=cmo.getAppDeployments()
			servers=cmo.getServers()
			for app in myapps:
				serverConfig()
				bean=getMBean('/AppDeployments/'+app.getName()+'/Targets/')
				targetsbean=bean.getTargets()
				domainRuntime()
				cd('AppRuntimeStateRuntime/AppRuntimeStateRuntime')
				for target in targetsbean:
					appstatus=cmo.getCurrentState(app.getName(),target.getName())
					HTML_APP(app.getName(),appstatus,target.getName())
			Servers=domainRuntimeService.getServerRuntimes()
			CreateHTML = open(FileHTML,"a")
			CreateHTML.write('<tr><th colspan="6">DATASOURCES</th></tr><tr><th colspan="2">DATASOURCE NAME</th><th colspan="2">STATE</th><th colspan="2">SERVER</th></tr>')
			CreateHTML.close()
			if (len(Servers) > 0):
				for DServer in Servers:
					jdbcServiceRT = DServer.getJDBCServiceRuntime()
					dataSources = jdbcServiceRT.getJDBCDataSourceRuntimeMBeans()
					if (len(dataSources) > 0):
						for dataSource in dataSources:
							HTML_JDBC(dataSource.getName(),dataSource.getState(),DServer.getName())
					else: 
						HTML_JDBC(JDServer,JDServer,ServerName)
		except:
			print ('Se omite directorio: ' + str(NDomain))
		  
CreateHTML = open(FileHTML,"a");CreateHTML.write('</tr></tbody></table></div></div>');CreateHTML.close() 
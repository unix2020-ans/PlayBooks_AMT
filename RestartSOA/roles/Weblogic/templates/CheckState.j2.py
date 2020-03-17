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
	CreateHTML = open(FileHTML,"a")
	CreateHTML.write('<tr><th colspan="2">DOMINIO</th><th colspan="2">PUERTO ADMIN</th><th colspan="2">DEFAULT</th></tr><tr><td colspan="2">'+Domain+'</td><td colspan="2">'+Port+'</td><td colspan="2">DEFECTO</td></tr><tr><th colspan="6">SERVERS</th></tr><tr><th>SERVER NAME</th><th colspan="2">STATE1</th><th>STATE2</th><th>PORT HTTP</th><th>PORT SSL</th></tr>')
	CreateHTML.close()

def HTML_SERVER(Server_N,State1,State2,HTTP,SSL):
	CreateHTML = open(FileHTML,"a")
	CreateHTML.write('<tr><td>'+ Server_N +'</td><td  colspan="2">'+ State1 +'</td><td>'+ State2 +'</td><td>'+ HTTP +'</td><td>'+ SSL +'</td></tr>')
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

Domains = "{{ DOMAIN_SOA.stdout }}"
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

CDomains = (Domains+'/servers/')
DCDomains = (Domains)
Port = os.popen("grep 'ADMIN_URL=' "+ DCDomains+"/bin/stopWebLogic.sh | sed -n 2p | sed 's/ADMIN_URL=//g'| awk -F : '{print $3}'").read().rstrip('\n').rstrip('"')
LISTENPORT = os.popen("grep 'ADMIN_URL=' "+ DCDomains+"/bin/stopWebLogic.sh | sed -n 2p | sed 's/ADMIN_URL=//g'| awk -F : '{print $2}' | sed 's=//==g'").read().rstrip('\n')
NAME_SERVER = os.popen("grep admin-server-name "+ DCDomains+"/config/config.xml | sed 's/<admin-server-name>//g' | sed 's=</admin-server-name>==g' | sed -n 1p | awk '{print $1}'").read().rstrip('\n')
HTML(FileHTML,Domains,Port)
CDServer = os.popen("ls -l " + CDomains + "| grep -v domain_bak| awk '{print $9}' | sed 1d | sed -n 1p").read().rstrip('\n')
FileCDS = (CDomains + '/' + CDServer + '/security/' + File)
Username = os.popen('cat ' + FileCDS + "| grep 'username=' | awk -F username= '{print $2}'").read().replace('\\','')
Pass = os.popen('cat ' + FileCDS + "| grep 'password=' |awk -F password= '{print $2}'").read().replace('\\','')
UserD = decrypt(DCDomains, Username)
PassD = decrypt(DCDomains, Pass)
connect( UserD , PassD , url='t3://'+LISTENPORT+':'+Port+'')
serverConfig()
servers=cmo.getServers()
for Server in servers:
	ServerName=Server.getName()
	domainRuntime()
	bean=getMBean('/ServerLifeCycleRuntimes/'+ServerName)
	bean1=getMBean('/ServerRuntimes/'+ServerName)
	ServerState=str(bean.getState())
	if ServerState == 'RUNNING':
		ServerHealth=str(bean1.getHealthState())
		EndHealth = str(HealthServer(ServerHealth))
		PortHTTPS = str(bean1.getSSLListenPort())
	else:
		EndHealth = 'SHUTDOWN'
		PortHTTPS = 'NONE'
	serverConfig()
	PortHTTP = str(Server.getListenPort())
	HTML_SERVER(ServerName,ServerState,EndHealth,PortHTTP,PortHTTPS)
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
Servers=domainRuntimeService.getServerRuntimes();
CreateHTML = open(FileHTML,"a")
CreateHTML.write('<tr><th colspan="6">DATASOURCES</th></tr><tr><th colspan="2">APPLICATION NAME</th><th colspan="2">STATE</th><th colspan="2">SERVER</th></tr>')
CreateHTML.close()
if (len(Servers) > 0):
	for DServer in Servers:
		jdbcServiceRT = DServer.getJDBCServiceRuntime();
		dataSources = jdbcServiceRT.getJDBCDataSourceRuntimeMBeans();
		if (len(dataSources) > 0):
			for dataSource in dataSources:
				HTML_JDBC(dataSource.getName(),dataSource.getState(),DServer.getName())
		else: 
			HTML_JDBC(JDServer,JDServer,JDServer)  
for Server in servers:
	ServerName=Server.getName()
	domainRuntime()
	bean=getMBean('/ServerLifeCycleRuntimes/'+ServerName)
	bean1=getMBean('/ServerRuntimes/'+ServerName)
	ServerState=str(bean.getState())
	if ServerState == 'RUNNING' and ServerName != str(NAME_SERVER):
		print('Deteniendo Manejado: ' + ServerName)
		shutdown(ServerName , 'Server', force="true")
		start(name=ServerName , block="true")
	else:
		start(name=ServerName , block="true")
	
CreateHTML = open(FileHTML,"a");CreateHTML.write('</tr></tbody></table></div></div></body></html>');CreateHTML.close() 
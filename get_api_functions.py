#~ import os
#~ arr = os.listdir('/home/serveradmin/bin/packages/PyCharm/odoo_12_BNC/docker-hotelscentric/additional_addons/Agentscentric')
#~ fc_list = (list(filter(lambda r: r == 'controllers', arr)))



import os
from fnmatch import fnmatch
import re
import pandas as pd

#~ root = '/home/serveradmin/bin/packages/PyCharm/odoo_12_BNC/docker-hotelscentric/additional_addons/Agentscentric/controllers'
#~ root = '/home/serveradmin/bin/packages/PyCharm/odoo_12_BNC/odoo/addons/sale_quotation_builder/controllers'
#~ root = '/home/serveradmin/bin/packages/PyCharm/odoo_12_BNC/odoo/addons/web_editor/controllers'

header_root = '/home/serveradmin/bin/packages/PyCharm/odoo_12_BNC/docker-hotelscentric/additional_addons/'

pattern = "*.py"

route_list = []
function_list = []
module_list = []

for root, dirs, fefe in os.walk("/home/serveradmin/bin/packages/PyCharm/odoo_12_BNC/docker-hotelscentric/additional_addons"):
	# /home/serveradmin/bin/packages/PyCharm/odoo_12_BNC/docker-hotelscentric/additional_addons/pos_multi_session_sync/controllers
	root_chk = dirs and list(filter(lambda r: 'controllers' in r, dirs)) and root or False
	if root_chk:
		root_path = u'{}/controllers'.format(root_chk)
		for path, subdirs, files in os.walk(root_path):
			for name in files:
				if fnmatch(name, pattern):
					if name not in ['__init__.py','manifest.py']:
						print 'root_path ===',root_path
						with open('{}/{}'.format(path,name), "r") as f:
							searchlines = f.readlines()
						for i, line in enumerate(searchlines):
							route_name = ''
							function_name = ''
							module_name = ''
													
							match_root = root.replace(header_root, "")
							module_name = match_root and match_root.split('/') and match_root.split('/')[0] or ''							
							
							if "@http.route" in line: 
								print 'line =====',line
								check_comment = line.strip().find('#')
								print 'check_comment ====',check_comment
								if check_comment == -1: # Check with non commented lines
									print 'bbbbbbbb'
									lindex = line.find('(')
									rindex = line.rfind(')')
									#~ if True:
										#~ print ('\n check_combination0 ====',check_combination0)
										#~ if check_combination0:
											#~ route_name = check_combination0 and tuple(check_combination0.groups()) or False
											#~ route_name = route_name and route_name[0] or False
									element = line[lindex:rindex+1].strip()
									if rindex == -1:
										element = line									
									check_combination1 = re.search("\(\[([^]]*)", element) # check combination ([
									if check_combination1:
										route_name = tuple(check_combination1.groups())
										#~ print 'route_name===',route_name
										route_name = route_name and route_name[0] or ''
									else:
										check_combination2 = element.split(',', 1)[0] # ('/im_livechat/loader/<int:channel_id>'
										quoted_strings1 = re.findall("'.*?'", check_combination2)
										quoted_strings2 = re.findall('".*?"', check_combination2)
										if quoted_strings1:
											route_name = quoted_strings1 and quoted_strings1[0] or ''
										elif quoted_strings2:
											route_name = quoted_strings2 and quoted_strings2[0] or ''
										print 'route_nameeeeeee===',route_name	
									for j in searchlines[i:i+10]:
										if 'def ' in j:
											function_name = j.split()[1].partition('(')[0]
											print 'function_name ===',function_name
											if function_name:
												function_list.append(function_name)
												#~ if function_name == 'bng_get_partner_verified_bank_accounts':
													#~ sssss
												break
									route_list.append(route_name)
									module_list.append(module_name)

comb_dict = {'Module':module_list, 'Route Name':route_list, 'Function Name':function_list}

print 'module_list',len(module_list)
print 'route_list',len(route_list)
print 'function_list',len(function_list)

df = pd.DataFrame(comb_dict) 

df.loc[:, ~df.columns.str.contains('^Unnamed')]

df.to_csv('file1.csv', header=True,columns=["Module","Route Name","Function Name"], index=False)
				
				
				#~ i = 0
				#~ for line in searchfile:
					#~ if "@http.route" in line: 
						#~ for l in line[0:0+3]: 
							#~ print l
						#~ print line, searchfile[i:i+3]
				#~ i += 1
				#~ searchfile.close()	
				
#~ \(\[([^]]*)]\)$
				


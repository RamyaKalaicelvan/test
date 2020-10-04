import os
from fnmatch import fnmatch
import re
import pandas as pd
import logging

_logger = logging.getLogger(__name__)


header_root = '/home/serveradmin/bin/packages/PyCharm/odoo_12_BNC/docker-hotelscentric/additional_addons/'

pattern = "*.py"

route_list = []
function_list = []
module_list = []

for root, dirs, nofiles in os.walk("/home/serveradmin/bin/packages/PyCharm/odoo_12_BNC/docker-hotelscentric/additional_addons"):
	root_chk = dirs and list(filter(lambda r: 'controllers' in r, dirs)) and root or False
	if root_chk:
		root_path = u'{}/controllers'.format(root_chk)
		for path, subdirs, files in os.walk(root_path):
			for name in files:
				if fnmatch(name, pattern):
					if name not in ['__init__.py','manifest.py']:
						with open('{}/{}'.format(path,name), "r") as f:
							searchlines = f.readlines()
						for i, line in enumerate(searchlines):
							route_name = ''
							function_name = ''
							module_name = ''
													
							match_root = root.replace(header_root, "")
							module_name = match_root and match_root.split('/') and match_root.split('/')[0] or ''							
							
							try:
								if "@http.route" in line:
									check_comment = line.strip().find('#')
									if check_comment == -1: # Check with non commented lines
										lindex = line.find('(')
										rindex = line.rfind(')')
										element = line[lindex:rindex+1].strip()
										if rindex == -1:
											element = line									
										check_combination1 = re.search("\(\[([^]]*)", element) # check combination ([
										if check_combination1:
											route_name = tuple(check_combination1.groups())
											route_name = route_name and route_name[0] or ''
										else:
											check_combination2 = element.split(',', 1)[0] # ('/im_livechat/loader/<int:channel_id>'
											quoted_strings1 = re.findall("'.*?'", check_combination2)
											quoted_strings2 = re.findall('".*?"', check_combination2)
											if quoted_strings1:
												route_name = quoted_strings1 and quoted_strings1[0] or ''
											elif quoted_strings2:
												route_name = quoted_strings2 and quoted_strings2[0] or ''
										for j in searchlines[i:i+10]:
											if 'def ' in j:
												function_name = j.split()[1].partition('(')[0]
												if function_name:
													function_list.append(function_name)
													break
										route_list.append(route_name)
										module_list.append(module_name)

							except Exception as e:
								print 'Something went wrong : ',str(e)
								_logger.info("Something went wron: %s", e)

comb_dict = {'Module':module_list, 'Route Name':route_list, 'Function Name':function_list}

if module_list and route_list and function_list:
	if len(module_list) == len(route_list) == len(function_list):			
		print 'module_list',len(module_list)
		print 'route_list',len(route_list)
		print 'function_list',len(function_list)

		df = pd.DataFrame(comb_dict) 

		df.loc[:, ~df.columns.str.contains('^Unnamed')]

		df.to_csv('api_list.csv', header=True,columns=["Module","Route Name","Function Name"], index=False)
				


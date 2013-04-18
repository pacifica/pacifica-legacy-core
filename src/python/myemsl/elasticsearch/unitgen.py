#/usr/bin/python
#coding=utf8

import simplejson as json

def merge_mods(newrow, oldtype):
	if oldtype.get('mods'):
		if newrow.get('mods') == None:
			newrow['mods'] = []
		already_in = {}
		for i in newrow['mods']:
			already_in[i['symb']] = 1
		to_add = []
		for i in oldtype['mods']:
			if already_in.get(i['symb']) == None:
				to_add.append(i)
		newrow['mods'] = newrow['mods'] + to_add

def unitgen():
	siunmod = [
		{"usymb":"(si:s)", 'symb':"s", "name":"second", "namep":"seconds", "type":"time"},
		{"usymb":"(si:°C)", "symb":"°C", "name":"degree Celsius", "namep":"degrees Celsius", "type":"thermodynamic temperature"},
		{"usymb":"(us:in)", "symb":"in", "name":"inch", "namep":"inches", "type":"length"},
		{"usymb":"(us:ft)", "symb":"ft", "name":"foot", "namep":"feet", "type":"length"},
		{"usymb":"(cs:B)", "symb":"B", "name":"byte", "namep":"bytes", "type":"size"},
		{"usymb":"(cs:b)", "symb":"b", "name":"bit", "namep":"bits", "type":"size"}
	]
	simod = [
		{"usymb":"(si:m)", "symb":"m", "name":"meter", "namep":"meters", "type":"length"},
		{"usymb":"(si:g)", "symb":"g", "name":"gram", "namep":"grams", "type":"mass"},
		{"usymb":"(si:A)", "symb":"A", "name":"ampere", "namep":"amperes", "type":"electric current"},
		{"usymb":"(si:K)", "symb":"K", "name":"kelvin", "namep":"kelvin", "type":"thermodynamic temperature"},
		{"usymb":"(si:mol)", "symb":"mol", "name":"mole", "namep":"moles", "type":"amount of substance"},
		{"usymb":"(si:cd)", "symb":"cd", "name":"candela", "namep":"candelas", "type":"luminous intensity"},
		{"usymb":"(si:Hz)", "symb":"Hz", "name":"hertz", "namep": "hertz", "type":"frequency"},
		{"usymb":"(si:rad)", "symb":"rad", "name":"radian", "namep":"radians", "type":"angle"},
		{"usymb":"(si:sr)", "symb":"sr", "name":"steradian", "namep":"steradians", "type":"solid angle"},
		{"usymb":"(si:N)", "symb":"N", "name":"newton", "namep":"newtons", "type":"force"},
		{"usymb":"(si:Pa)", "symb":"Pa", "name":"pascal", "namep":"pascals", "type":"pressure"},
		{"usymb":"(si:J)", "symb":"J", "name":"joule", "namep":"joules", "type":"energy"},
		{"usymb":"(si:W)", "symb":"W", "name":"watt", "namep":"watts", "type":"power"},
		{"usymb":"(si:C)", "symb":"C", "name":"coulomb", "namep":"coulombs", "type":"electric charge"},
		{"usymb":"(si:V)", "symb":"V", "name":"volt", "namep":"volts", "type":"electrical potential difference"},
		{"usymb":"(si:F)", "symb":"F", "name":"farad", "namep":"farads", "type":"electric capacitance"},
		{"usymb":"(si:Ω)", "symb":"Ω", "name":"ohm", "namep":"ohms", "type":"electric resistance"},
		{"usymb":"(si:S)", "symb":"S", "name":"siemens", "namep":"siemens", "type":"electrical conductance"},
		{"usymb":"(si:Wb)", "symb":"Wb", "name":"weber", "namep":"webers", "type":"magnetic flux"},
		{"usymb":"(si:T)", "symb":"T", "name":"tesla", "namep":"teslas", "type":"magnetic field strength"},
		{"usymb":"(si:H)", "symb":"H", "name":"henry", "namep":"henries", "type":"inductance"},
		{"usymb":"(si:lm)", "symb":"lm", "name":"lumen", "namep":"lumens", "type":"luminous flux"},
		{"usymb":"(si:lx)", "symb":"lx", "name":"lux", "namep":"lux", "type":"illuminance"},
		{"usymb":"(si:Bq)", "symb":"Bq", "name":"becquerel", "namep":"bacquerels", "type":"radioactivity"},
		{"usymb":"(si:Gy)", "symb":"Gy", "name":"gray", "namep":"gray", "type":"absorbed dose of ionizing radiation"},
		{"usymb":"(si:Sv)", "symb":"Sv", "name":"sievert", "namep":"sieverts", "type":"equivalent dose of ionizing radiation"},
		{"usymb":"(si:kat)", "symb":"kat", "name":"katal", "namep":"katals", "type":"catalytic activity"},
		{"usymb":"(si:L)", "symb":"L", "name":"liter", "namep":"liters", "type":"volume"},
		{"usymb":"(si:Å)", "symb":"Å", "name":"angstrom", "namep":"angstroms", "type":"length"}
	]
	neg = '⁻'
	sup = [
		'',
		'¹',
		'²',
		'³',
		'⁴'
	]
	simodmods = {
		"Y":{"power":24, "name":"yotta"},
		"Z":{"power":21, "name":"zetta"},
		"E":{"power":18, "name":"exa"},
		"P":{"power":15, "name":"peta"},
		"T":{"power":12, "name":"tera"},
		"G":{"power":9, "name":"giga"},
		"M":{"power":6, "name":"mega"},
		"k":{"power":3, "name":"kilo"},
		"h":{"power":2, "name":"hecto"},
		"da":{"power":1, "name":"deka"},
		"":{"power":0, "name":""},
		"d":{"power":-1, "name":"deci"},
		"c":{"power":-2, "name":"centi"},
		"m":{"power":-3, "name":"milli"},
		"µ":{"power":-6, "name":"micro"},
		"n":{"power":-9, "name":"nano"},
		"p":{"power":-12, "name":"pico"},
		"f":{"power":-15, "name":"femto"},
		"a":{"power":-18, "name":"atto"},
		"z":{"power":-21, "name":"zepto"},
		"y":{"power":-24, "name":"yocto"}
	}
	bytemods = {
		"Y":{"power":24, "name":"yotta", "name2":"yobi"},
		"Z":{"power":21, "name":"zetta", "name2":"zebi"},
		"E":{"power":18, "name":"exa", "name2":"exbi"},
		"P":{"power":15, "name":"peta", "name2":"pebi"},
		"T":{"power":12, "name":"tera", "name2":"tebi"},
		"G":{"power":9, "name":"giga", "name2":"gibi"},
		"M":{"power":6, "name":"mega", "name2":"mebi"},
		"k":{"power":3, "name":"kilo", "name2":"kibi"},
		"":{"power":0},
	}
	types = {}
	for j in simod:
		for i in simodmods.keys():
			t = j['type']
			if types.get(t) == None:
				types[t] = []
			row = {"type":t, "usymb":('(si:' + i + j['symb'] + ')'), "symb":(i + j['symb']), "name":(simodmods[i]['name'] + j['name']), "namep":(simodmods[i]['name'] + j['namep'])}
			if simodmods[i]['power'] != 0:
				row['mods'] = [{'symb':i, 'name':simodmods[i]['name']}]
			types[t].append(row)
	for i in siunmod:
		if i['symb'] == "s":
			list = dict([(k, v) for k,v in simodmods.iteritems() if v['power'] <= 0])
			for symb, j in list.iteritems():
				t = i['type']
				if types.get(t) == None:
					types[t] = []
				types[t].append({"type":t, "usymb":('(si:' + symb + i['symb'] + ')'), "symb":(symb + i['symb']), "name":(j['name'] + i['name']), "namep":(j['name'] + i['namep'])})
		if i['usymb'] == "(cs:B)" or i['usymb'] == "(cs:b)":
			for symb, j in bytemods.iteritems():
				t = i['type']
				if types.get(t) == None:
					types[t] = []
				if j['power'] != 0:
					types[t].append({"type":t, "usymb":('(cs:' + symb + 'i' + i['symb'] + ')'), "symb":(symb + 'i' + i['symb']), "name":(j['name2'] + i['name']), "namep":(j['name2'] + i['namep']), 'mods':[{'symb':symb, 'name':j['name']}]})
					types[t].append({"type":t, "usymb":('(css:' + symb + i['symb'] + ')'), "symb":(symb + i['symb']), "name":(j['name'] + i['name'] + '(base10)'), "namep":(j['name'] + i['namep'] + '(base10)'), 'mods':[{'symb':symb, 'name':j['name']}]})
				else:
					types[t].append({"type":t, "usymb":('(cs:' + symb + i['symb'] + ')'), "symb":(symb + i['symb']), "name":(i['name']), "namep":(i['namep'])})
		else:
			t = i['type']
			if types.get(t) == None:
				types[t] = []
			types[t].append({"type":t, "usymb":i['usymb'], "symb":i['symb'], "name":i['name'], "namep":i['namep']})
	t = 'area'
	if types.get(t) == None:
		types[t] = []
	for i in types['length']:
		row = {"type":t, "usymb":(i['usymb'] + sup[2]), "symb":(i['symb'] + sup[2]), "name":("square " + i['name']), "namep":("square " + i['namep'])}
		merge_mods(row, i)
		types[t].append(row)
	t = 'volume'
	if types.get(t) == None:
		types[t] = []
	for i in types['length']:
		row = {"type":t, "usymb":(i['usymb'] + sup[3]), "symb":(i['symb'] + sup[3]), "name":("cubic " + i['name']), "namep":("cubic " + i['namep'])}
		merge_mods(row, i)
		types[t].append(row)
#newton/second, grays/second
	for (t, subtype) in [['speed', 'length'], ['volumetric flow', 'volume'], ['kinematic viscosity', 'area']]:
		if types.get(t) == None:
			types[t] = []
		for i in types[subtype]:
			row = {"type":t, "usymb":(i['usymb'] + "/(si:s)"), "symb":(i['symb'] + "/s"), "name":(i['name'] + " per second"), "namep":(i['namep'] + " per second")}
			merge_mods(row, i)
			types[t].append(row)
	for (t, subtype) in [['acceleration', 'length']]:
		if types.get(t) == None:
			types[t] = []
		for i in types[subtype]:
			row = {"type":t, "usymb":(i['usymb'] + "/(si:s)" + sup[2]), "symb":(i['symb'] + "/s" + sup[2]), "name":(i['name'] + " per second squared"), "namep":(i['namep'] + " per second squared")}
			merge_mods(row, i)
			types[t].append(row)
	for (t, subtype) in [['jerk', 'length']]:
		if types.get(t) == None:
			types[t] = []
		for i in types[subtype]:
			row = {"type":t, "usymb":(i['usymb'] + "/(si:s)" + sup[3]), "symb":(i['symb'] + "/s" + sup[3]), "name":(i['name'] + " per second cubed"), "namep":(i['namep'] + " per second cubed")}
			merge_mods(row, i)
			types[t].append(row)
	for (t, subtype) in [['snap', 'length']]:
		if types.get(t) == None:
			types[t] = []
		for i in types[subtype]:
			row = {"type":t, "usymb":(i['usymb'] + "/(si:s)" + sup[4]), "symb":(i['symb'] + "/s" + sup[4]), "name":(i['name'] + " per quartic second"), "namep":(i['namep'] + " per quartic second")}
			merge_mods(row, i)
			types[t].append(row)
	return types

if __name__ == '__main__':
	types = unitgen()
	print json.dumps(types, indent=4)
	print sum([len(types[i]) for i in types.keys()])

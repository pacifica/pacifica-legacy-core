#!/usr/bin/python

def prefix_tree_make_list(list):
	end = False
	if len(list) <= 0:
		return [0, True, None]
	mlen = min([len(i) for i in list])
	if mlen == 0:
		end = True
		list = [x for x in list if x]
		if len(list) <= 0:
			return [0, True, None]
		mlen = min([len(i) for i in list])
	d = {}
	for str in list:
		prefix = str[:mlen]
		tlist = d.get(prefix)
		if not tlist:
			tlist = []
			d[prefix] = tlist
		tlist.append(str[mlen:])
	nd = {}
	for i in d:
		nd[i] = prefix_tree_make_list(d[i])
	return [mlen, end, nd]

def prefix_tree_make_dict(d):
	list = d.keys()
	tree = prefix_tree_make_list(list)
	prefix_annotate_tree('', tree, d)
	return tree

def prefix_annotate_tree(prefix, tree, d):
	if tree[1]:
		tree.append(d[prefix])
	if tree[2] == None:
		return
	for (k, entry) in tree[2].iteritems():
		tprefix = prefix + k
		prefix_annotate_tree(tprefix, entry, d)

def prefix_tree_find_dir(dir, tree):
	prefix = dir[:tree[0]]
	rest = dir[tree[0]:]
	matched_prefix = prefix
	while True:
		if tree[2] == None:
			return None
		entry = tree[2].get(prefix)
		if not entry:
			return None
		if entry[1]:
			if rest == '' or rest[0] == '/':
				return (matched_prefix, entry[3])
		tree = entry
		prefix = rest[:entry[0]]
		matched_prefix += prefix
		rest = rest[entry[0]:]


def main():
	d = {
		'abcdefg': 'foo',
		'abc': 'bar',
	}
	tree = prefix_tree_make_dict(d)
	print prefix_tree_find_dir('foobarnone', tree) == None
	print prefix_tree_find_dir('abcdefg', tree)[1] == 'foo'
	print prefix_tree_find_dir('abcd', tree) == None
	print prefix_tree_find_dir('abc', tree)[1] == 'bar'
	print prefix_tree_find_dir('abc/bar', tree)[1] == 'bar'
	print prefix_tree_find_dir('abcd/bar', tree) == None
	print prefix_tree_find_dir('abcdefg/bar', tree)[1] == 'foo'
	print prefix_tree_find_dir('abcdefgh/bar', tree) == None

if __name__ == '__main__':
	main()


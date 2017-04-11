import graph_tool.all as gt
import graph_tool.centrality
import os
import operator
import matplotlib
import numpy as np
import scikits.statsmodels.tools as sm
import matplotlib.pyplot as plt

NETWORKS_DIR='networks'
OUTPUT_DIR='output'

def plot_cdf(sample):
	ecdf = sm.tools.ECDF(sample)
	x = np.linspace(min(sample), max(sample))
	y = ecdf(x)
	plt.plot(x, y, 'bo')
	plt.gca().set_xscale('log')
	plt.gca().set_yscale('log')
	plt.gca().set_aspect('equal', adjustable='box')

	plt.show()

def save_vertex_result(lst, path):
	txt = ''
	for i in lst:
		txt += str(i[0]) + ';' + str(i[1]) + '\n'
		
	f = open(os.path.join(OUTPUT_DIR, path), 'w')
	f.write(txt)
	f.close()

def proccess_graph(obj):
	print 'Building graph...'
	if obj['type'] == 'gml':
		g = gt.load_graph(os.path.join(NETWORKS_DIR, obj['path']))
	elif obj['type'] == 'data':
		g = gt.Graph(directed=True)
		f = open(os.path.join(NETWORKS_DIR, obj['path']))
		lines = f.readlines()

		for line in lines:
			if '#' in line:
				continue
			g.add_edge(int(line.split()[0]), int(line.split()[1]))
	else:
		g = Graph(directed=True)

	print str(len(list(g.vertices()))) + ' vertices / ' + str(len(list(g.edges()))) + ' edges'
	return g

def degree_centrality(g, name):
	print 'calculating degree centrality...'

	# in and out degrees
	in_dg = {}
	out_dg = {}
	N = len(list(g.vertices()))
	for v in g.vertices():
		in_dg[v] = float(v.in_degree())/(N-1)
		out_dg[v] = float(v.out_degree())/(N-1)

	########### Graph View for degree in ###########
	vp = g.new_vertex_property("double")
	g.vp.degree_in = vp
	for v in in_dg:
		g.vp.degree_in[v] = in_dg[v]

	gt.graph_draw(g, vertex_fill_color=vp,
               vertex_size=gt.prop_to_size(vp, mi=5, ma=15),
               vcmap=matplotlib.cm.gist_heat,
               vorder=vp,output=os.path.join(OUTPUT_DIR, name+'_degree_in.png'))
	########### Graph View for degree out ###########
	vp = g.new_vertex_property("double")
	g.vp.degree_out = vp
	for v in in_dg:
		g.vp.degree_out[v] = out_dg[v]

	gt.graph_draw(g, vertex_fill_color=vp,
               vertex_size=gt.prop_to_size(vp, mi=5, ma=15),
               vcmap=matplotlib.cm.gist_heat,
               vorder=vp,output=os.path.join(OUTPUT_DIR, name+'_degree_out.png'))
	################################################

	sorted_in = sorted(in_dg.items(), key=operator.itemgetter(1))
	sorted_out = sorted(out_dg.items(), key=operator.itemgetter(1))
	sorted_in.reverse()
	sorted_out.reverse()

	save_vertex_result(sorted_in, name + '_degree_in.csv')
	save_vertex_result(sorted_out, name + '_degree_out.csv')

	# CDF degree in
	sample = [x[1] for x in sorted_in]
	plot_cdf(sample)

	# CDF degree out
	sample = [x[1] for x in sorted_out]
	plot_cdf(sample)


def betweeness_centrality(g, name):
	print 'calculating betweeness centrality...'
	vp, ep = graph_tool.centrality.betweenness(g)

	gt.graph_draw(g, vertex_fill_color=vp,
               vertex_size=gt.prop_to_size(vp, mi=5, ma=15),
               #edge_pen_width=gt.prop_to_size(ep, mi=0.5, ma=5),
               vcmap=matplotlib.cm.gist_heat,
               vorder=vp,output=os.path.join(OUTPUT_DIR, name+'_betweeness.png'))

	bt = {}
	for v in g.vertices():
		bt[v] = vp[v]

	sorted_bt = sorted(bt.items(), key=operator.itemgetter(1))
	sorted_bt.reverse()

	save_vertex_result(sorted_bt, name + '_betweeness.csv')

	# ECDF
	sample = [x[1] for x in sorted_bt]
	plot_cdf(sample)

def closeness_centrality(g, name):
	print 'calculating closeness centrality...'
	c = gt.closeness(g,harmonic=True)
	gt.graph_draw(g, vertex_fill_color=c,
               vertex_size=gt.prop_to_size(c, mi=5, ma=15),
               vcmap=matplotlib.cm.gist_heat,
               vorder=c, output=os.path.join(OUTPUT_DIR, name+'_closeness.png'))

	cl = {}
	for v in g.vertices():
		cl[v] = c[v]

	sorted_cl = sorted(cl.items(), key=operator.itemgetter(1))
	sorted_cl.reverse()

	save_vertex_result(sorted_cl, name + '_closeness.csv')

	# ECDF
	sample = [x[1] for x in sorted_cl]
	plot_cdf(sample)

def katz_centrality(g, name):
	print 'calculating katz centrality...'
	if "value" in g.edge_properties:
		w = g.edge_properties["value"]
	else:
		w = None

	k = gt.katz(g, weight=w)
	gt.graph_draw(g, vertex_fill_color=k,
               vertex_size=gt.prop_to_size(k, mi=5, ma=15),
               vcmap=matplotlib.cm.gist_heat,
               vorder=k, output=os.path.join(OUTPUT_DIR, name+'_katz.png'))

	kt = {}
	for v in g.vertices():
		kt[v] = k[v]

	sorted_kt = sorted(kt.items(), key=operator.itemgetter(1))
	sorted_kt.reverse()

	save_vertex_result(sorted_kt, name + '_katz.csv')

	# ECDF
	sample = [x[1] for x in sorted_kt]
	plot_cdf(sample)

def pagerank_centrality(g, name):
	print 'calculating pagerank centrality...'
	pr = gt.pagerank(g)
	gt.graph_draw(g, vertex_fill_color=pr,
               vertex_size=gt.prop_to_size(pr, mi=5, ma=15),
               vorder=pr, vcmap=matplotlib.cm.gist_heat,
               output=os.path.join(OUTPUT_DIR, name+'_pagerank.png'))

	prnk = {}
	for v in g.vertices():
		prnk[v] = pr[v]

	sorted_pg = sorted(prnk.items(), key=operator.itemgetter(1))
	sorted_pg.reverse()

	save_vertex_result(sorted_pg, name + '_pagerank.csv')

	# ECDF
	sample = [x[1] for x in sorted_pg]
	plot_cdf(sample)


def main():
	names = {}
	names['celegansneural'] = {'type': 'gml', 'path': 'celegansneural/celegansneural.gml'}
	names['gnutella'] = {'type': 'data', 'path': 'gnutella/gnutella.data'}
	names['political'] = {'type': 'gml', 'path': 'political/political.gml'}

	for name in names:
		print '############### ' + name + ' ###############'
		g = proccess_graph(names[name])

		degree_centrality(g, name)
		betweeness_centrality(g, name)
		closeness_centrality(g, name)
		katz_centrality(g, name)
		pagerank_centrality(g, name)

		print '\n\n'

main()
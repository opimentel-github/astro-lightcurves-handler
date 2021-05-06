#!/usr/bin/env python3
import sys
sys.path.append('../') # or just install the module
sys.path.append('../../flaming-choripan') # or just install the module
sys.path.append('../../astro-lightcurves-handler') # or just install the module

if __name__== '__main__':
	### parser arguments
	import argparse
	from flamingchoripan.prints import print_big_bar

	parser = argparse.ArgumentParser('usage description')
	parser.add_argument('-method',  type=str, default='spm-mcmc-fstw', help='method')
	main_args = parser.parse_args()
	print_big_bar()

	###################################################################################################################################################
	import numpy as np
	from flamingchoripan.files import load_pickle, save_pickle, get_dict_from_filedir

	filedir = f'../../surveys-save/survey=alerceZTFv7.1~bands=gr~mode=onlySNe~method={main_args.method}.splcds'
	filedict = get_dict_from_filedir(filedir)
	rootdir = filedict['_rootdir']
	cfilename = filedict['_cfilename']
	survey = filedict['survey']
	lcdataset = load_pickle(filedir)
	print(lcdataset)

	###################################################################################################################################################
	import flamingchoripan.lists as lists
	from flamingchoripan.cuteplots.utils import save_fig
	import matplotlib.pyplot as plt
	from lchandler.plots.lc import plot_lightcurve
	from flamingchoripan.files import save_time_stamp

	figsize = (12,5)
	lcset_names = lcdataset.get_lcset_names()
	for lcset_name in lcset_names:
		lcset = lcdataset[lcset_name]
		for lcobj_name in lcset.get_lcobj_names():
			fig, ax = plt.subplots(1,1, figsize=figsize)
			lcobj = lcset[lcobj_name]
			c = lcset.class_names[lcobj.y]
			for kb,b in enumerate(lcset.band_names):
				plot_lightcurve(ax, lcobj, b, label=f'{b} obs')
			title = f'survey={lcset.survey}-{"".join(lcset.band_names)} - obj={lcobj_name} [{lcset.class_names[lcobj.y]}]'
			ax.set_title(title)
			ax.set_xlabel('time [days]')
			ax.set_ylabel('observations [flux]')
			ax.grid(alpha=0.5)
			ax.legend()
			save_filedir = f'../save/{cfilename}/{lcset_name}/{c}/{lcobj_name}.png'
			save_fig(save_filedir, fig)
			save_time_stamp(f'../save/{cfilename}')
			#break



from model_config import Modelconfig, Modelpara
from main_computation import update_p, select_lamu 
from data_preprocess import data_prepare
from functools import partial
import numpy as np
import multiprocessing as mp
import os
from sys import getsizeof
from six.moves import cPickle as pkl
import glob
import matplotlib.pyplot
matplotlib.pyplot.switch_backend('agg')
import matplotlib.pyplot as plt

def CDN_fmri(folder_name, data_file, stimuli_folder, dt, lam, mu=[0], lam_1=[0], tol=1e-2, max_iter=100, N=50, fold=0.5, data_dir=None, x_real=None, A_real=None, B_real=None, C_real=None):
    """
    folder_name: string, used to save all data and analysis results
                 after running this function, you will get a structure like the following: 
                             folder_name
                                       / data: save all data files 
                                       / para: save results for tuning 
                                       / results: save all results with pictures 
    data_file: string, file name of BOLD signal
    stimuli_folder: string, folder name of stimuli
    dt: TR of fMRI data
    lam, mu, lam_1: tuning parameters
    tol, max_iter: parameter for algorithm convergence
    N: num of basis - 1, 
    fold: scalar (integral evaluation stepsize = fold*dt)
    data_dir: precomputed data if any 
    x_real, A_real, B_real, C_real: the real parameters which are used to verify simulations 
    """
    if folder_name[-1] != '/':
        folder_name = folder_name + '/'

    pickle_file_config = folder_name + 'results/'
    pickle_file_data= folder_name + 'data/'
    pickle_file_para= folder_name +'para/'
    if not os.path.exists(pickle_file_data):
        os.makedirs(pickle_file_data)
    if not os.path.exists(pickle_file_config):
        os.makedirs(pickle_file_config)
    if not os.path.exists(pickle_file_para):
        os.makedirs(pickle_file_para)
    if data_dir:
        precomp = False
    else:
        precomp = True

    data_prepare(data_file, stimuli_folder, pickle_file_data, dt, N, fold, precomp, x_real, A_real, B_real, C_real)
    if not data_dir:
        data_dir = pickle_file_data
    config = select_lamu(lam, mu, lam_1, folder_name, pickle_file_para, data_dir)
    with open(folder_name+'results/result.pkl') as f:
        save = pkl.load(f)
    t = save['t']
    print t.shape
    n1 = save['n1'] 
    row_n = config.y.shape[1]
    # cut off begining and end
    t = t[(n1+1):(row_n-n1)]
    estimated_x = save['estimated_x']
    estimated_y = save['estimated_y']
    print t.shape, estimated_x.shape, n1
    y = config.y

    for i in range(config.y.shape[0]):
        f, axarr = plt.subplots(2, 1)
        axarr[0].plot(t, estimated_x[i,(n1+1):(row_n-n1)], color='xkcd:purple', label='estimated', linewidth=2)
        axarr[0].set_xlabel('Time (Sec)')
        if x_real:
            axarr[0].plot(t,x_real[i,(n1+1):(row_n-n1)], color='xkcd:blue', label='real', linewidth=2)


        axarr[1].plot(t, estimated_y[i,(n1+1):(row_n-n1)], color='xkcd:purple', label='estimated', linewidth=2)
        axarr[1].plot(t, y[i,(n1+1):(row_n-n1)], color='xkcd:blue', label='real', linewidth=2)
        axarr[1].set_xlabel('Time (Sec)')
        plt.subplots_adjust(hspace=0.25)
        f.savefig(folder_name + 'results/estimated_' + str(i)+ '.svg')
        plt.close()

    return config.lamu 








def CDN_multi_sub(folder_name, data_file, stimuli_folder, dt, lam, mu=[0], lam_1=[0], N=50, fold=0.5, x_real=None, A_real=None, B_real=None, C_real=None, tol=1e-2, share_stimuli=True, max_iter=100, share_tuning=True):
    """
    folder_name: list of folders, for each folder, one subject estimated is saved. 
    data_file: list of files name, BOLD signal for corresponding subject
    stimuli_folder: list of stimuli foders for all subject
                    if the subjects share the same stimuli, let every entry of stimuli_folder be the same
    lam, mu, lam_1: tuning parameters
    tol: convergence parameters
    share_stimuli: bool variable, if the subjects have the same stimuli, set this as True
    share_tuning: bool variable, if you want only want to do tuning parameter selection for one subject and other subjects
                  use this selected parameter, set this as True. 
    Other parameters: see function CDN_fMRI
    """
    n1, n2, n3 = len(folder_name), len(data_file), len(stimuli_folder)
    if set([n1,n2,n3]) != 1:
        raise Exception('Please check the input files, you need the same length for folder_name, data_file and stimuli_folder')
    data_dir = None 
    config = CDN_fmri(folder_name[0], data_file[0], stimuli_folder[0], dt, lam, mu, lam_1, tol, max_iter, N, fold, x_real=x_real, A_real=A_real, B_real=B_real, C_real=C_real)
    if share_stimuli:
        data_dir = folder_name[0] + 'data/'
    if share_tuning:
        lam, mu, lam_1 = [config.lamu[0]], [config.lamu[1]], [config.lamu[2]]
    for i in range(1, len(folder_name)):
        config = CDN_fmri(folder_name[i], data_file[i], stimuli_folder[i], dt, lam, mu, lam_1, tol, max_iter, N, fold, data_dir=data_dir, x_real=x_real, A_real=A_real, B_real=B_real, C_real=C_real)



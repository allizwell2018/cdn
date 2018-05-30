import numpy as np
import math 
from six.moves import cPickle as pkl 
<<<<<<< 35ad562cb6467d5e7f9fb09a96095b61805d300f
function (x, param = NULL, verbose = TRUE) 
{
    if (is.null(param)) {
        if (verbose == TRUE) {
            warning("Default parameters for HRF are used")
        }
        param <- list()
        param$a1 <- 6
        param$a2 <- 12
        param$b1 <- 0.9
        param$b2 <- 0.9
        param$c <- 0.35
    }
    d1 <- param$a1 * param$b1
    d2 <- param$a2 * param$b2
    (x/d1)^param$a1 * exp(-(x - d1)/param$b1) - param$c * (x/d2)^param$a2 * 
        exp(-(x - d2)/param$b2)
}
def CanonicalHRF(x):
	a1, a2, b1, b2 = 6, 12, 0.9, 0.9 
	d1 = a1*b1
	d2 = a2*b2
	c = 
def data_prepare(y_name, u_name, file_name, dt, N=50, fold=0.5, precomp=True, x_real=None, y_real=None, A_real=None, B_real=None, C_real=None, sim_data=None):
	"""
	preprocess the data for CDN analysis, the function is prepared for single subject processing 

	Parameters
	------------
	y_name: file name of fMRI BOLD signal with string format
	u_name: folder name of fMRI stimuli which includes only stimuli file indexed from *.ev1 to *.evJ where J is the number of stimuli
            We require the colum of the file is the time dimension where row is the space dimension
    file_name: list of two strings (the file name we use to save our observed data and precomputed data)
    dt: TR of fMRI signal
    N: number of basis
=======
from scipy.integrate import simps 

def canonicalHRF(x):
    """
    CanonicalHRF

    Parameters
    ------------
    x: numpy array, time points

    Returns
    ------------
    numpy array, evalated value at x time points 

    """
    a1, a2, b1, b2, c = 6, 12, 0.9, 0.9, 0.35 
    d1 = a1*b1
    d2 = a2*b2
    return ((x/d1)**a1) * math.exp(-(x - d1)/b1) - c*((x/d2)**a2)*math.exp(-(x - d2)/b2)


def pos(x):
    return x*(x>0)

# add cubic spline in the future 
def basis(x, h, i):
    """
    creating piecewise linear basis

    Returns
    ----------
    list of basis values

    """
    n = len(x)
    ans = [0]*n
    for j in range(n):
        tmp = x[j]
        if tmp > (i - 1)*h and tmp < i*h:
            ans[j] = -(tmp-(i-1)*h)/h
        elif tmp >= i*h and tmp < (i+1)*h:
            ans[j] = -((i+1)*h - tmp)/h
        else:
            ans[j] = 0 
    return np.array(ans) 
def pro(file_name, t):
    """
    transfer stimulus to function and return stimulus value

    Parameters
    ------------
    file_name: stimulus file name
    t: time poins

    Returns
    ------------
    list of stimulus values at t
    """
    tmp = np.loadtxt(file_name)
    a = tmp[:,0]
    b = tmp[:,0] + tmp[:,1] 
    n = a.shape[0]
    i = 0
    ans = [0]*len(t)
    for j, ts in enumerate(t):
        if ts < a[0] or ts > b[n]:
            continue
        else:
            while i < n:
                if a[i] <= ts and ts <= b[i]:
                    ans[j] = tmp[i,2]
                    break
                elif b[i] < ts and ts < a[i+1]:
                    break 
                else:
                    i += 1
    return np.array(ans) 


def data_prepare(y_name, u_name, folder_name, dt, N=50, fold=0.5, precomp=True, x_real=None, A_real=None, B_real=None, C_real=None, sim_data=None):
    """
    preprocess the data for CDN analysis, the function is prepared for single subject processing 

    Parameters
    ------------
    y_name: file name of fMRI BOLD signal with string format
    u_name: folder name of fMRI stimuli which includes only stimuli file indexed from *.ev0 to *.ev(J-1) where J is the number of stimuli
            We require the colum of the file is the time dimension where row is the space dimension
    file_name: list of two strings (the file name we use to save our observed data and precomputed data)
    dt: TR of fMRI signal
    N: number of basis - 1
>>>>>>> finish wrapper
    fold: scalar (integral evaluation stepsize = fold*dt)
    precomp: bool (Whether to do precomputation for this subject). This variable is only useful when we do multi-subjects computation. 
    x_real: file name of neuronal signal
    y_real: file name of real fMRI BOLD signal
    A_real, B_real, C_real: numpy matrices (real parameters) 
    sim_data: file name of simulated data which is provided for verification of algorithm. If this is provided, other related parameters will be overrided except N.
<<<<<<< 35ad562cb6467d5e7f9fb09a96095b61805d300f
	

	Returns
	------------
	None, preprocessed data will be saved into a file
	"""
	if not sim_data:
		with open(sim_data) as f:
			save = pkl.load(f)['simulation']
			y_name = save['y']
			u_name = save['u']
			fold = save['fold']
			x_real = save['x_real']
			y_real = save['y_real']
			A_real = save['A_real']
			B_real = save['B_real']
			C_real = save['C_real']
	else:
		# n_area * row_n
		y = np.loadtxt(y_name).T
		u = np.loadtxt(u_name).T 
	n_are, row_n = y.shape
	J = u.shape[0]
	h = dt*fold
    t_T = dt*(row_n-1)
    dt_1 = t_T/N
    
    t_0 = [i*dt for i in range(row_n)]
=======
    

    Returns
    ------------
    None, preprocessed data will be saved into a file
    """
    if not sim_data:
        with open(sim_data) as f:
            save = pkl.load(f)['simulation']
            y = save['y']
            u_name = save['u']
            fold = save['fold']
            x_real = save['x_real']
            y_real = save['y_real']
            A_real = save['A_real']
            B_real = save['B_real']
            C_real = save['C_real']
    else:
        # n_area * row_n
        y = np.loadtxt(y_name).T
        #u = np.loadtxt(u_name).T 
    n_area, row_n = y.shape
        with open(folder_name+'observed.pkl'):
            save = {}
            save['y'] = y
            save['n_area'] = n_area
            save['A_real'] = A_real
            save['B_real'] = B_real
            save['C_real'] = C_real
            save['x_real'] = x_real
            pkl.dump(save, f, pickle.HIGHEST_PROTOCOL)
    if not precomp:
        return 

    J = u.shape[0]
    h = dt*fold
    t_T = dt*(row_n-1)
    dt_1 = t_T/N
    p = N+1 
    t_0 = np.array([i*dt for i in range(row_n)])
>>>>>>> finish wrapper
    l_t_0 = row_n

    # cut off begining and end time sequences

    r_n = math.floor(2*dt_1/(dt*fold))
    l_t = int((dt*(row_n-1)-2*r_n*dt*fold)/(dt*fold))
<<<<<<< 35ad562cb6467d5e7f9fb09a96095b61805d300f
    t = [r_n*dt*fold + i*dt*fold for i in range(l_t)]
    hrf_l = int(30/(dt*fold))
    t_1 = [dt*fold*i for i in range(hrf_l)]

    
t_1<-seq(0,dt*12,by=dt*fold)
hrf<-canonicalHRF(t_1)
l_t_1<-length(t_1)
sim_n<-5
n_area<-6



	
=======
    t = np.array([r_n*dt*fold + i*dt*fold for i in range(l_t)])
    hrf_l = int(30/(dt*fold))
    t_1 = np.array([dt*fold*i for i in range(hrf_l)])
    hrf = canonicalHRF(t_1)

    # begin computation

    Phi = np.zeros((p,l_t))
    for i in range(p):
        Phi[i,:] = basis(t, i=i)

    Phi_d = np.zeros((p,l_t))
    for i in range(p):
        for j in range(l_t-1):
            Phi_d[i,j] = (Phi[i,j+1]-Phi[i,j])/h
        Phi_d[i,l_t-1] = (Phi[i,j]-Phi[i,j-1])/h
    
    P1 = np.zeros((p,p))
    for i in range(p):
        for j in range(p):
            P1[i,j] = simps(Phi_d[i,:]*Phi_d[j,:], t)

    P2 = np.zeros((p,p))
    for i in range(p):
        for j in range(p):
            P2[i,j] = simps(Phi[i,:]*Phi_d[j,:], t)

    P5 = np.zeros((p,p))
    for i in range(p):
        for j in range(p):
            P5[i,j] = simps(Phi[i,:]*Phi[j,:], t)

    P8 = np.zeros((1,p))
    for i in range(p):
        P8[0,i] = simps(Phi_d[i,:], t)

    P9 = np.zeros((1,p))
    for i in range(p):
        P9[0,i] = simps(Phi[i,:], t)

    P12 = np.zeros((l_t_0,p))
    for i in range(l_t_0):
        for j in range(p):
            P12[j,i] = simps(hrf*basis(j*dt-t_1,i=i), t_1) 

    P12_1 = np.zeros((l_t+2, p))
    for j in range(l_t+1):
        for i in range(p):
            P12_1[j,i] = simps(hrf*basis((j-1)*dt*fold-t_1,i=i), t_1)

    P12_2 = np.zeros((l_t, p))
    for j in range(l_t):
        for i in range(p):
            P12_2[j,i] = (P12_1[j+2,i]+P12_1[j,i]-2*P12_1[j+1,i])
    P12_2 = P12_2/((dt*fold)**2)
    
    #Omega second derivative
    Omega = np.zeros((p,p))
    for i in range(p):
        for j in range(p):
            Omega[i,j] = simps(P12_2[:,i]*P12_2[:,j], t)


    #####################stimuli related computation
    U = np.zeros((J, l_t))
    for i in range(J):
        U[i,:] = pro(u_name + '/ev'+str(i)+'.txt', t)

    U_Phi = np.zeros((p,l_t, J))
    for j in range(J):
        for i in range(p):
            for k in range(l_t):
                U_Phi[i,k,j] = U[j,k]*Phi[i,k]

    P3 = np.zeros((p,p,J))
    for j in range(J):
        for i in range(p):
            for k in range(p):
                P3[i,k,j] = simps(Phi[i,:]*Phi_d[k,:]*U[j,:], t)

    P4 = np.zeros((J,p))
    for j in range(J):
        for i in range(p):
            P4[j,i] = simps(U[j,:]*Phi_d[i,:], t)

    P6 = np.zeros((p,p,J))
    for j in range(J):
        for i in range(p):
            for k in range(p):
                P6[i,k,j] = simps(Phi[i,:]*Phi[k,:]*U[j,:], t)

    P7 = np.zeros((J,p))
    for j in range(J):
        for i in range(p):
            P7[j,i] = simps(U[j,:]*Phi[i,:], t)

    P10 = np.zeros((p,p,J,J))
    for j in range(J):
        for k in range(J):
            for i in range(p):
                for l in range(p):
                    P10[i,l,j,k] = simps(Phi[i,:]*U[j,:]*Phi[l,:]*U[k,:], t)
    #TBD rm this 
    P11 = np.zeros((J,p))
    for j in range(J):
        for i in range(p):
            P11[j,i] = simps(Phi[i,:]*U[j,:])

    P13 = np.zeros((J,p,J))
    for j in range(J):
        for k in range(J):
            for i in range(p):
                P13[k,i,j] = simps(U[k,:]*Phi[i,:]*U[j,:], t)

    P14 = np.zeros((J,J))
    for j in range(J):
        for k in range(J):
            P14[j,k] = simps(U[j,:]*U[k,:], t)

    P15 = np.zeros((1,J))
    for j in range(J):
        P15[0,j] = simps(U[j,:], t)

    t_U = np.zeros((J, l_t-1))
    for i in range(1, l_t):
        tmp_U = np.zeros((J,1))
        for l in range(J):
            tmp_U[l,0] = pro(u_name + '/ev'+str(l)+'.txt', ((i-1)*h+h/2))
        t_U[:,i-1] = tmp_U

    # without truncation 
    t_tmp = t
    t = t_0
    l_t = len(t)
    Phi_1 = np.zeros((p,l_t))
    for i in range(p):
        Phi_1[i,:] = basis(t, i=i)

    Phi_d_1 = np.zeros((p,l_t))
    for i in range(p):
        for j in range(l_t-1):
            Phi_d_1[i,j] = (Phi_1[i,j+1]-Phi_1[i,j])/h
        Phi_d_1[i,l_t-1] = (Phi_1[i,j]-Phi_1[i,j-1])/h

    U_1 = np.zeros((J, l_t))
    for i in range(J):
        U_1[i,:] = pro(u_name + '/ev'+str(i)+'.txt', t)

    U_Phi_1 = np.zeros((p,l_t, J))
    for j in range(J):
        for i in range(p):
            for k in range(l_t):
                U_Phi_1[i,k,j] = U_1[j,k]*Phi_1[i,k]

    t_U_1 = np.zeros((J, l_t-1))
    for i in range(1, l_t):
        tmp_U = np.zeros((J,1))
        for l in range(J):
            tmp_U[l,0] = pro(u_name + '/ev'+str(l)+'.txt', ((i-1)*h+h/2))
        t_U_1[:,i-1] = tmp_U

    with open(folder_name+'precomp.pkl'):
        save = {
        'P1':P1,'P2':P2,'P3':P3,'P4':P4,
        'P5':P5,'P6':P6,'P7':P7,'P8':P8,'P9':P9,'P10':P10,
        'P11':P11,'P12':P12,'P13':P13,'P14':P14,'P15':P15,
        'Q1':Phi_d,'Q2':Phi,'Q3':U_Phi,'Q4': U,
        'Omega': Omega,
        't_1': t_1,
        'hrf':hrf,
        't':t_tmp,
        'Q1_all': Q1_all,
        'Q2_all': Q2_all,
        'Q3_all': U_Phi_1,
        'Q4_all': U_1,
        't_all':t,
        't_U_1': t_U_1,
        'row_n':row_n,
        'J':J, 'N':N, 'p':p, 'dt':dt, 'fold':fold,
        }
        pkl.dump(save, f, pickle.HIGHEST_PROTOCOL)

        


  
  
>>>>>>> finish wrapper

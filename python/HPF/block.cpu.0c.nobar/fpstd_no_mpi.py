import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d
from mpl_toolkits.axes_grid1 import make_axes_locatable
import os, time, datetime
from scipy.constants import c,mu_0, epsilon_0
from .plotfunc import plot2D3D

savepath = '/home/ldg/pyscript/graph_no_mpi/'
if not os.path.exists(savepath) : os.mkdir(savepath)

import platform
if platform.system() == 'Windows' : newline='\r\n'
elif platform.system() == 'Linux' : newline='\n'

IE = 44
JE = 44
KE = 180

npml = 10

IEp = IE + 2 * npml
JEp = JE + 2 * npml
KEp = KE + 2 * npml

totalSIZE  = IEp * JEp * KEp
totalSHAPE = (IEp, JEp, KEp)

ic = int(IEp/2)
jc = int(JEp/2)
kc = int(KEp/2)

S = 1./4
nm = 1e-9
dx, dy, dz = 10*nm, 10*nm, 10*nm


# maxdt = (2./c) / np.sqrt( (np.pi/dx)**2 + (np.pi/dy)**2 + (2/dz)**2 )
dt = S * min(dx,dy,dz)/c
# print((S * min(dx,dy,dz)/c - dt) > 0 )
dtype = np.complex128

#########################################################################################
################################# PML PARAMETER SETTING  ################################
#########################################################################################

kappa_x = np.ones(IEp, dtype=dtype)
kappa_y = np.ones(JEp, dtype=dtype)
kappa_z = np.ones(KEp, dtype=dtype)

sigma_x = np.zeros(IEp, dtype=dtype)
sigma_y = np.zeros(JEp, dtype=dtype)
sigma_z = np.zeros(KEp, dtype=dtype)

kappa_mx = np.ones(IEp, dtype=dtype)
kappa_my = np.ones(JEp, dtype=dtype)
kappa_mz = np.ones(KEp, dtype=dtype)

sigma_mx = np.zeros(IEp, dtype=dtype)
sigma_my = np.zeros(JEp, dtype=dtype)
sigma_mz = np.zeros(KEp, dtype=dtype)

##### Grading of PML region #####

rc0 = 1.e-16		# reflection coefficient
gradingOrder = 3.
impedence = np.sqrt(mu_0/epsilon_0)
boundarywidth_x = npml * dx
boundarywidth_y = npml * dy
boundarywidth_z = npml * dz

sigmax_x = -(gradingOrder+1)*np.log(rc0)/(2*impedence*boundarywidth_x)
sigmax_y = -(gradingOrder+1)*np.log(rc0)/(2*impedence*boundarywidth_y)
sigmax_z = -(gradingOrder+1)*np.log(rc0)/(2*impedence*boundarywidth_z)

kappamax_x = 5.
kappamax_y = 5.
kappamax_z = 5.

sigmax_mx = sigmax_x * impedence**2
sigmax_my = sigmax_y * impedence**2
sigmax_mz = sigmax_z * impedence**2

kappamax_mx = kappamax_x
kappamax_my = kappamax_y
kappamax_mz = kappamax_z

space_eps = np.ones(totalSHAPE,dtype=dtype) * epsilon_0
space_mu  = np.ones(totalSHAPE,dtype=dtype) * mu_0

####################################################################################
################################## APPLYING PML ####################################
####################################################################################

def Apply_PML_3D(**kwargs):
	
	npml = 10

	for key, value in list(kwargs.items()):
		if key == 'x': x = value
		elif key == 'y': y = value
		elif key == 'z': z = value
		elif key == 'pml': npml = value

	for i in range(npml):

		if x == '-' :
			
			sigma_x[i]  = sigmax_x * (dtype(npml-i)/npml)**gradingOrder
			kappa_x[i]  = 1 + ((kappamax_x - 1) * ((dtype(npml-i)/npml)**gradingOrder))
			sigma_mx[i] = sigma_x[i] * impedence**2
			kappa_mx[i] = kappa_x[i]

		elif x == '+' :

			sigma_x[-i-1]  = sigmax_x * (dtype(npml-i)/npml)**gradingOrder
			kappa_x[-i-1]  = 1 + ((kappamax_x - 1) * ((dtype(npml-i)/npml)**gradingOrder))
			sigma_mx[-i-1] = sigma_x[-i-1] * impedence**2
			kappa_mx[-i-1] = kappa_x[-i-1]
			
		elif x == '+-' :

			sigma_x[i]  = sigmax_x * (dtype(npml-i)/npml)**gradingOrder
			kappa_x[i]  = 1 + ((kappamax_x-1)*((dtype(npml-i)/npml)**gradingOrder))
			sigma_mx[i] = sigma_x[i] * impedence**2
			kappa_mx[i] = kappa_x[i]

			sigma_x[-i-1]  = sigma_x[i]
			kappa_x[-i-1]  = kappa_x[i]
			sigma_mx[-i-1] = sigma_mx[i]
			kappa_mx[-i-1] = kappa_mx[i]
			
	for j in range(npml):

		if y == '-' :
			
			sigma_y[j]  = sigmax_y * (dtype(npml-j)/npml)**gradingOrder
			kappa_y[j]  = 1 + ((kappamax_y - 1) * ((dtype(npml-j)/npml)**gradingOrder))
			sigma_my[j] = sigma_y[j] * impedence**2
			kappa_my[j] = kappa_y[j]

		elif y == '+' :

			sigma_y[-j-1]  = sigmax_y * (dtype(npml-j)/npml)**gradingOrder
			kappa_y[-j-1]  = 1 + ((kappamax_y - 1) * ((dtype(npml-j)/npml)**gradingOrder))
			sigma_my[-j-1] = sigma_y[-j-1] * impedence**2
			kappa_my[-j-1] = kappa_y[-j-1]
			
		elif y == '+-' :

			sigma_y[j]  = sigmax_y * (dtype(npml-j)/npml)**gradingOrder
			kappa_y[j]  = 1 + ((kappamax_y-1)*((dtype(npml-j)/npml)**gradingOrder))
			sigma_my[j] = sigma_y[j] * impedence**2
			kappa_my[j] = kappa_y[j]

			sigma_y[-j-1]  = sigma_y[j]
			kappa_y[-j-1]  = kappa_y[j]
			sigma_my[-j-1] = sigma_my[j]
			kappa_my[-j-1] = kappa_my[j]

	for k in range(npml):

		if z == '-' :
			
			sigma_z[k]  = sigmax_z * (dtype(npml-k)/npml)**gradingOrder
			kappa_z[k]  = 1 + ((kappamax_z - 1) * ((dtype(npml-k)/npml)**gradingOrder))
			sigma_mz[k] = sigma_z[k] * impedence**2
			kappa_mz[k] = kappa_z[k]

		elif z == '+' :

			sigma_z[-k-1]  = sigmax_z * (dtype(npml-k)/npml)**gradingOrder
			kappa_z[-k-1]  = 1 + ((kappamax_z - 1) * ((dtype(npml-k)/npml)**gradingOrder))
			sigma_mz[-k-1] = sigma_z[-k-1] * impedence**2
			kappa_mz[-k-1] = kappa_z[-k-1]
			
		elif z == '+-' :

			sigma_z[k]  = sigmax_z * (dtype(npml-k)/npml)**gradingOrder
			kappa_z[k]  = 1 + ((kappamax_z-1)*((dtype(npml-k)/npml)**gradingOrder))
			sigma_mz[k] = sigma_z[k] * impedence**2
			kappa_mz[k] = kappa_z[k]

			sigma_z[-k-1]  = sigma_z[k]
			kappa_z[-k-1]  = kappa_z[k]
			sigma_mz[-k-1] = sigma_mz[k]
			kappa_mz[-k-1] = kappa_mz[k]

def Apply_PEC_3D(**kwargs):
		
	for key, value in list(kwargs.items()):

		if key == 'x': x = value
		elif key == 'y': y = value
		elif key == 'z': z = value
		elif key == 'pml': npml = value

	if x == '-': kappa_x[0]  = 1.e16
	elif x == '+': kappa_x[-1] = 1.e16
	elif x == '+-': 
		kappa_x[0]  = 1.e16
		kappa_x[-1] = 1.e16		

	if y == '-': kappa_y[0]  = 1.e16
	elif y == '+': kappa_y[-1] = 1.e16
	elif y == '+-':
		kappa_y[0]  = 1.e16
		kappa_y[-1] = 1.e16		
	
	if z == '-': kappa_z[0]  = 1.e16
	elif z == '+': kappa_z[-1] = 1.e16
	elif z == '+-':
		kappa_z[0]  = 1.e16
		kappa_z[-1] = 1.e16		

apply_PML = True
apply_PEC = True

if apply_PML == True : Apply_PML_3D(x='',y='',z='+-')
#if apply_PEC == True : Apply_PEC_3D()

px = (2 * epsilon_0 * kappa_x) + (sigma_x * dt)
py = (2 * epsilon_0 * kappa_y) + (sigma_y * dt)
pz = (2 * epsilon_0 * kappa_z) + (sigma_z * dt)

mx = (2 * epsilon_0 * kappa_x) - (sigma_x * dt)
my = (2 * epsilon_0 * kappa_y) - (sigma_y * dt)
mz = (2 * epsilon_0 * kappa_z) - (sigma_z * dt)

mpx = (2 * mu_0 * kappa_mx) + (sigma_mx * dt)
mpy = (2 * mu_0 * kappa_my) + (sigma_my * dt)
mpz = (2 * mu_0 * kappa_mz) + (sigma_mz * dt)

mmx = (2 * mu_0 * kappa_mx) - (sigma_mx * dt)
mmy = (2 * mu_0 * kappa_my) - (sigma_my * dt)
mmz = (2 * mu_0 * kappa_mz) - (sigma_mz * dt)

#if not os.path.exists('./coefficient/') : os.mkdir('./coefficient/')
#
#np.savetxt('./coefficient/kappa_x.txt', kappa_x, fmt='%.3e',newline=newline, header='kappa_x :%s' %(newline))
#np.savetxt('./coefficient/kappa_y.txt', kappa_y, fmt='%.3e',newline=newline, header='kappa_y :%s' %(newline))
#np.savetxt('./coefficient/kappa_z.txt', kappa_z, fmt='%.3e',newline=newline, header='kappa_z :%s' %(newline))
#
#np.savetxt('./coefficient/sigma_x.txt', sigma_x, fmt='%.3e',newline=newline, header='sigma_x :%s' %(newline))
#np.savetxt('./coefficient/sigma_y.txt', sigma_y, fmt='%.3e',newline=newline, header='sigma_y :%s' %(newline))
#np.savetxt('./coefficient/sigma_z.txt', sigma_z, fmt='%.3e',newline=newline, header='sigma_z :%s' %(newline))
#
#np.savetxt('./coefficient/kappa_mx.txt', kappa_mx, fmt='%.3e',newline=newline, header='kappa_mx :%s' %(newline))
#np.savetxt('./coefficient/kappa_my.txt', kappa_my, fmt='%.3e',newline=newline, header='kappa_my :%s' %(newline))
#np.savetxt('./coefficient/kappa_mz.txt', kappa_mz, fmt='%.3e',newline=newline, header='kappa_mz :%s' %(newline))
#
#np.savetxt('./coefficient/sigma_mx.txt', sigma_mx, fmt='%.3e',newline=newline, header='sigma_mx :%s' %(newline))
#np.savetxt('./coefficient/sigma_my.txt', sigma_my, fmt='%.3e',newline=newline, header='sigma_my :%s' %(newline))
#np.savetxt('./coefficient/sigma_mz.txt', sigma_mz, fmt='%.3e',newline=newline, header='sigma_mz :%s' %(newline))
#
#np.savetxt('./coefficient/px.txt', px, fmt='%.3e',newline=newline, header='px :%s' %(newline))
#np.savetxt('./coefficient/py.txt', py, fmt='%.3e',newline=newline, header='py :%s' %(newline))
#np.savetxt('./coefficient/pz.txt', pz, fmt='%.3e',newline=newline, header='pz :%s' %(newline))
#
#np.savetxt('./coefficient/mx.txt', mx, fmt='%.3e',newline=newline, header='mx :%s' %(newline))
#np.savetxt('./coefficient/my.txt', my, fmt='%.3e',newline=newline, header='my :%s' %(newline))
#np.savetxt('./coefficient/mz.txt', mz, fmt='%.3e',newline=newline, header='mz :%s' %(newline))
#
#np.savetxt('./coefficient/mpx.txt', mpx, fmt='%.3e',newline=newline, header='mpx :%s' %(newline))
#np.savetxt('./coefficient/mpy.txt', mpy, fmt='%.3e',newline=newline, header='mpy :%s' %(newline))
#np.savetxt('./coefficient/mpz.txt', mpz, fmt='%.3e',newline=newline, header='mpz :%s' %(newline))
#
#np.savetxt('./coefficient/mmx.txt', mmx, fmt='%.3e',newline=newline, header='mmx :%s' %(newline))
#np.savetxt('./coefficient/mmy.txt', mmy, fmt='%.3e',newline=newline, header='mmy :%s' %(newline))
#np.savetxt('./coefficient/mmz.txt', mmz, fmt='%.3e',newline=newline, header='mmz :%s' %(newline))

##########################################################################################
################################### MATERIAL SETTING  ###################################
#########################################################################################

def rectangle_3D(backend_lower_left,front_upper_right, eps_r, mu_r, conductivity):
	"""Put 3D Cubic in main space.

	PARAMETERS
	--------------
	backend_lower_left : int tuple
		coordinates of backend_lower_left

	front_upper_right : int tuple
		coordinates of front_upper_right

	eps_r : float or tuple
		relative epsilon of rectanguler slab
		anisotropic magnetic materials can be applied by tuple.

	mu_r : float or tuple
		relative epsilon of rectanguler slab
		anisotropic dielectric materials can be applied by tuple.
		
	
	Returns
	-------------
	None
	"""
	assert eps_r != 0, "Relative dielctric constant of material should be bigger than 0"
	assert mu_r  != 0, "Relative magnetic constantof matherial should be bigger than 0"

	if type(eps_r) == int : eps_r = dtype(eps_r)
	elif type(eps_r) == dtype:
		eps_rx = eps_r
		eps_ry = eps_r
		eps_rz = eps_r
	elif type(eps_r) == tuple:
		eps_rx = eps_r[0]
		eps_ry = eps_r[1]
		eps_rz = eps_r[2]

	if type(mu_r) == dtype:
		mu_rx = mu_r
		mu_ry = mu_r
		mu_rz = mu_r
	elif type(mu_r) == int:
		mu_rx = dtype(mu_r)
		mu_ry = dtype(mu_r)
	elif type(mu_r) == tuple:
		mu_rx = mu_r[0]
		mu_ry = mu_r[1]
		mu_rz = mu_r[2]

	if type(conductivity) == int:
		conductivity_x = dtype(conductivity)
		conductivity_y = dtype(conductivity)
		conductivity_z = dtype(conductivity)

	elif type(conductivity) == dtype:
		conductivity_x = conductivity
		conductivity_y = conductivity
		conductivity_z = conductivity

	elif type(conductivity) == tuple:
		conductivity_x = conductivity[0] / eps_rx
		conductivity_y = conductivity[1] / eps_ry
		conductivity_z = conductivity[2] / eps_rz

	xcoor = backend_lower_left[0]
	ycoor = backend_lower_left[1]
	zcoor = backend_lower_left[2]
	
	height = front_upper_right[0] - backend_lower_left[0]
	depth  = front_upper_right[1] - backend_lower_left[1]
	width  = front_upper_right[2] - backend_lower_left[2]

	#### applying isotropic slab ####
	for i in range(height):
		for j in range(depth):
			for k in range(width):
				space_eps[xcoor+i,ycoor+j,zcoor+k] = eps_r * epsilon_0
				space_mu [xcoor+i,ycoor+j,zcoor+k] = mu_r  * mu_0

	return None

# rectangle_3D((0,0,60),(40,40,80),4,1,0)
# rectangle_3D((0,0,80),(40,40,100),9,1,0)

###########################################################################################
############################## FIELD AND COEFFICIENT ARRAYS ###############################
###########################################################################################

Ex = np.zeros(totalSHAPE, dtype=dtype)
Ey = np.zeros(totalSHAPE, dtype=dtype)
Ez = np.zeros(totalSHAPE, dtype=dtype)

Dx = np.zeros(totalSHAPE, dtype=dtype)
Dy = np.zeros(totalSHAPE, dtype=dtype)
Dz = np.zeros(totalSHAPE, dtype=dtype)

Hx = np.zeros(totalSHAPE, dtype=dtype)
Hy = np.zeros(totalSHAPE, dtype=dtype)
Hz = np.zeros(totalSHAPE, dtype=dtype)

Bx = np.zeros(totalSHAPE, dtype=dtype)
By = np.zeros(totalSHAPE, dtype=dtype)
Bz = np.zeros(totalSHAPE, dtype=dtype)

kx = np.fft.fftfreq(IEp,dx) * 2. * np.pi
ky = np.fft.fftfreq(JEp,dy) * 2. * np.pi
kz = np.fft.fftfreq(KEp,dz) * 2. * np.pi

nax   = np.newaxis
ones  = np.ones (totalSHAPE, dtype=dtype)
zeros = np.zeros(totalSHAPE, dtype=dtype)

ikx = 1j * kx[:,nax,nax] * ones
iky = 1j * ky[nax,:,nax] * ones
ikz = 1j * kz[nax,nax,:] * ones

ikx = ikx.astype(dtype)
iky = iky.astype(dtype)
ikz = ikz.astype(dtype)

assert ikx.dtype == dtype, "dtype of ikx must be equal to %s" %dtype
assert iky.dtype == dtype, "dtype of iky must be equal to %s" %dtype
assert ikz.dtype == dtype, "dtype of ikz must be equal to %s" %dtype

print(("Size of each field array : %.2f M bytes." %(ones.nbytes/1024/1024)))

CDx1 = (my[nax,:,nax] * ones) / (py[nax,:,nax] * ones)
CDx2 =    2. * epsilon_0 * dt / (py[nax,:,nax] * ones)

CEx1 = (mz[nax,nax,:] * ones) / (pz[nax,nax,:] * ones)
CEx2 = (px[:,nax,nax] * ones) / (pz[nax,nax,:] * ones) / space_eps
CEx3 = (mx[:,nax,nax] * ones) / (pz[nax,nax,:] * ones) / space_eps * (-1)

CDy1 = (mz[nax,nax,:] * ones) / (pz[nax,nax,:] * ones)
CDy2 =    2. * epsilon_0 * dt / (pz[nax,nax,:] * ones)

CEy1 = (mx[:,nax,nax] * ones) / (px[:,nax,nax] * ones)
CEy2 = (py[nax,:,nax] * ones) / (px[:,nax,nax] * ones) / space_eps
CEy3 = (my[nax,:,nax] * ones) / (px[:,nax,nax] * ones) / space_eps * (-1)

CDz1 = (mx[:,nax,nax] * ones) / (px[:,nax,nax] * ones)
CDz2 =    2. * epsilon_0 * dt / (px[:,nax,nax] * ones)

CEz1 = (my[nax,:,nax] * ones) / (py[nax,:,nax] * ones)
CEz2 = (pz[nax,nax,:] * ones) / (py[nax,:,nax] * ones) / space_eps
CEz3 = (mz[nax,nax,:] * ones) / (py[nax,:,nax] * ones) / space_eps * (-1)

CBx1 = (mmy[nax,:,nax] * ones) / (mpy[nax,:,nax] * ones)
CBx2 =          2. * mu_0 * dt / (mpy[nax,:,nax] * ones) * (-1)

CHx1 = (mmz[nax,nax,:] * ones) / (mpz[nax,nax,:] * ones)
CHx2 = (mpx[:,nax,nax] * ones) / (mpz[nax,nax,:] * ones) / space_mu
CHx3 = (mmx[:,nax,nax] * ones) / (mpz[nax,nax,:] * ones) / space_mu * (-1)

CBy1 = (mmz[nax,nax,:] * ones) / (mpz[nax,nax,:] * ones)
CBy2 =          2. * mu_0 * dt / (mpz[nax,nax,:] * ones) * (-1)

CHy1 = (mmx[:,nax,nax] * ones) / (mpx[:,nax,nax] * ones)
CHy2 = (mpy[nax,:,nax] * ones) / (mpx[:,nax,nax] * ones) / space_mu
CHy3 = (mmy[nax,:,nax] * ones) / (mpx[:,nax,nax] * ones) / space_mu * (-1)

CBz1 = (mmx[:,nax,nax] * ones) / (mpx[:,nax,nax] * ones)
CBz2 =          2. * mu_0 * dt / (mpx[:,nax,nax] * ones) * (-1)

CHz1 = (mmy[nax,:,nax] * ones) / (mpy[nax,:,nax] * ones)
CHz2 = (mpz[nax,nax,:] * ones) / (mpy[nax,:,nax] * ones) / space_mu
CHz3 = (mmz[nax,nax,:] * ones) / (mpy[nax,:,nax] * ones) / space_mu * (-1)

assert CDx1.dtype == dtype, "dtype of coefficient array must be equal to %s" %(dtype)
assert CEx1.dtype == dtype, "dtype of coefficient array must be equal to %s" %(dtype)
assert CBx1.dtype == dtype, "dtype of coefficient array must be equal to %s" %(dtype)
assert CHx1.dtype == dtype, "dtype of coefficient array must be equal to %s" %(dtype)

###########################################################################################
######################################## SOURCE ###########################################
###########################################################################################

wavelength = np.arange(400,800,.5) * nm
wlc   = (wavelength[0] + wavelength[-1])/2
freq  = c / wavelength
freqc = (freq[0] + freq[-1]) / 2

w0 = 2 * np.pi * freqc
ws = 0.2 * w0

ts = 1./ws
tc = 1000. * dt

src_zpos =  20 + npml
trs_zpos = -20 - npml

###########################################################################################
###################################### TIME LOOP  #########################################
###########################################################################################

nsteps = 2501
tstart = datetime.datetime.now()
localsize = 512

Ex_inp = np.zeros(nsteps, dtype=dtype)
Ex_src = np.zeros(nsteps, dtype=dtype)
Ex_ref = np.zeros(nsteps, dtype=dtype)
Ex_trs = np.zeros(nsteps, dtype=dtype)

ft  = np.fft.fftn
ift = np.fft.ifftn

print("Simulation Start")

timeloop = True

if timeloop == True : 

	for step in range(nsteps):
		
		pulse = np.exp((-.5) * (((step*dt-tc)*ws)**2)) * np.cos(w0*(step*dt-tc))
	
		# Adding source
		Ex[:,:,src_zpos] += pulse

		Ex_inp[step] = Ex[:,:,src_zpos].mean()
		Ex_ref[step] = Ex[:,:,src_zpos].mean() - pulse
		Ex_trs[step] = Ex[:,:,trs_zpos].mean()

		# Update Bx field
		for k in range(KEp-1):

			previous  = Bx[:,:,k].copy()
			diffzEy_k = (Ey[:,:,k+1] - Ey[:,:,k]) / dz
			diffyEz_k = ift(iky[:,:,k] * ft(Ez[:,:,k], axes=(1,)), axes=(1,))
			Bx[:,:,k] = CBx1[:,:,k] * Bx[:,:,k] + CBx2[:,:,k] * (diffyEz_k - diffzEy_k)
			Hx[:,:,k] = CHx1[:,:,k] * Hx[:,:,k] + CHx2[:,:,k] * Bx[:,:,k] + CHx3[:,:,k] * previous

		# Update By field
		for k in range(KEp-1):

			previous  = By[:,:,k].copy()
			diffzEx_k = (Ex[:,:,k+1] - Ex[:,:,k]) / dz
			diffxEz_k = ift(ikx[:,:,k] * ft(Ez[:,:,k], axes=(0,)), axes=(0,))
			By[:,:,k] = CBy1[:,:,k] * By[:,:,k] + CBy2[:,:,k] * (diffzEx_k - diffxEz_k)
			Hy[:,:,k] = CHy1[:,:,k] * Hy[:,:,k] + CHy2[:,:,k] * By[:,:,k] + CHy3[:,:,k] * previous
			
		# Update Bz field
		previous = Bz.copy()
		diffxEy  = ift(ikx*ft(Ey,axes=(0,)),axes=(0,))
		diffyEx  = ift(iky*ft(Ex,axes=(1,)),axes=(1,))
		Bz = CBz1 * Bz + CBz2 * (diffxEy - diffyEx)
		Hz = CHz1 * Hz + CHz2 * Bz + CHz3 * previous

		# Update Dx field
		for k in range(1,KEp):
			
			previous = Dx[:,:,k].copy()
			diffzHy  = (Hy[:,:,k] - Hy[:,:,k-1]) / dz
			diffyHz  = ift(iky[:,:,k] * ft(Hz[:,:,k], axes=(1,)), axes=(1,))
			Dx[:,:,k] = CDx1[:,:,k] * Dx[:,:,k] + CDx2[:,:,k] * (diffyHz - diffzHy)
			Ex[:,:,k] = CEx1[:,:,k] * Ex[:,:,k] + CEx2[:,:,k] * Dx[:,:,k] + CEx3[:,:,k] * previous
		
		# Update Dy field
		for k in range(1,KEp):
		
			previous = Dy[:,:,k].copy()
			diffzHx  = (Hx[:,:,k] - Hx[:,:,k-1]) / dz
			diffxHz  = ift(ikx[:,:,k] * ft(Hz[:,:,k], axes=(0,)), axes=(0,))
			Dy[:,:,k] = CDy1[:,:,k] * Dy[:,:,k] + CDy2[:,:,k] * (diffzHx - diffxHz)
			Ey[:,:,k] = CEy1[:,:,k] * Ey[:,:,k] + CEy2[:,:,k] * Dy[:,:,k] + CHy3[:,:,k] * previous

		# Update Dz field
		previous = Dz.copy()
		diffxHy  = ift(ikx*ft(Hy,axes=(0,)),axes=(0,))
		diffyHx  = ift(iky*ft(Hx,axes=(1,)),axes=(1,))
		Dz = CDz1 * Dz + CDz2 * (diffxHy - diffyHx)
		Ez = CEz1 * Ez + CEz2 * Dz + CEz3 * previous

		if step % 100 == 0 : print(("time : %s, step : %05d" %(datetime.datetime.now()-tstart,step)))
#		if step % 100 == 0 : plot2D3D(Ex[ic,:,:],savepath, step=step, stride=2, zlim=2, colordeep=3.)


print('\n')
print("Simulation Finished")

######################################################################################
##################################### PLOTTING #######################################
######################################################################################

print("Plotting Start")

tsteps = np.arange(nsteps, dtype=dtype)
t = tsteps * dt
Ex_src = np.exp((-.5)*(((tsteps*dt-tc)*ws)**2)) * np.cos(w0*(tsteps*dt-tc)) /S/2.

Ex_inp_ft = (dt * Ex_inp[nax,:] * np.exp(1.j * 2.*np.pi*freq[:,nax] * t[nax,:]) ).sum(1) / np.sqrt(2.*np.pi)
Ex_src_ft = (dt * Ex_src[nax,:] * np.exp(1.j * 2.*np.pi*freq[:,nax] * t[nax,:]) ).sum(1) / np.sqrt(2.*np.pi)
Ex_ref_ft = (dt * Ex_ref[nax,:] * np.exp(1.j * 2.*np.pi*freq[:,nax] * t[nax,:]) ).sum(1) / np.sqrt(2.*np.pi)
Ex_trs_ft = (dt * Ex_trs[nax,:] * np.exp(1.j * 2.*np.pi*freq[:,nax] * t[nax,:]) ).sum(1) / np.sqrt(2.*np.pi)

####################################### RT graph #######################################

Trs = (abs(Ex_trs_ft)**2)/(abs(Ex_src_ft)**2)
Ref = (abs(Ex_ref_ft)**2)/(abs(Ex_src_ft)**2)
Total  = Trs + Ref

np.savetxt('./graph/Ex_inp.txt', Ex_inp, fmt='%.3e', newline=newline, header='Ex_inp :%s' %newline)
np.savetxt('./graph/Ex_src.txt', Ex_src, fmt='%.3e', newline=newline, header='Ex_src :%s' %newline)
np.savetxt('./graph/Ex_ref.txt', Ex_ref, fmt='%.3e', newline=newline, header='Ex_ref :%s' %newline)
np.savetxt('./graph/Ex_trs.txt', Ex_trs, fmt='%.3e', newline=newline, header='Ex_trs :%s' %newline)
np.savetxt('./graph/Trans.txt' , Trs,    fmt='%.3e', newline=newline, header='Trs    :%s' %newline)
np.savetxt('./graph/Reflec.txt', Ref,    fmt='%.3e', newline=newline, header='Ref    :%s' %newline)
np.savetxt('./graph/Total.txt' , Total,  fmt='%.3e', newline=newline, header='Total  :%s' %newline)

wl = wavelength

RTgraph = plt.figure(figsize=(21,9))

ax1 = RTgraph.add_subplot(121)
ax1.plot(wl/nm, Ref.real,   label ='Ref',   color='green')
ax1.plot(wl/nm, Trs.real,   label ='Trs',   color='red')
ax1.plot(wl/nm, Total.real, label ='Total', color='blue')
ax1.set_xlabel('wavelength, nm')
ax1.set_ylabel('Ratio')
#ax1.set_ylim(0.,1.1)
ax1.legend(loc='best')
ax1.grid(True)

ax2 = RTgraph.add_subplot(122)
ax2.plot(freq/1.e12, Ref.real,   label='Ref',   color='green')
ax2.plot(freq/1.e12, Trs.real,   label='Trs',   color='red')
ax2.plot(freq/1.e12, Total.real, label='Total', color='blue')
ax2.set_xlabel('freq, THz')
ax2.set_ylabel('Ratio')
#ax2.set_ylim(0.,1.1)
ax2.legend(loc='best')
ax2.grid(True)

RTgraph.savefig(savepath+"RTgraph.png")
plt.close()

############################ Comparing with Theoratical graph #############################

TMM = IRT()
TMM.wavelength(wl)
TMM.incidentangle(angle=0, unit='radian')
TMM.mediumindex(1.,2.,1.)
TMM.mediumtype('nonmagnetic')
TMM.mediumthick(200*nm)
TMM.cal_spol_matrix()

TMMref = TMM.Reflectance()
TMMtrs = TMM.Transmittance()
TMMfreq = TMM.frequency

fig = plt.figure(figsize=(15,15))

ax1 = fig.add_subplot(221)
ax2 = fig.add_subplot(222)
ax3 = fig.add_subplot(223)
ax4 = fig.add_subplot(224)

ax1.plot(wl/nm,      TMMref.real, color='red', alpha=.5, linewidth=3, label='Theoratical')
ax2.plot(wl/nm,      TMMtrs.real, color='red', alpha=.5, linewidth=3, label='Theoratical')
ax3.plot(freq/1.e12, TMMref.real, color='red', alpha=.5, linewidth=3, label='Theoratical')
ax4.plot(freq/1.e12, TMMtrs.real, color='red', alpha=.5, linewidth=3, label='Theoratical')

ax1.plot(wl/nm, Ref.real, 	label='Simulation')
ax2.plot(wl/nm, Trs.real, 	label='Simulation')
ax3.plot(freq/1.e12, Ref.real, label='Simulation')
ax4.plot(freq/1.e12, Trs.real,  label='Simulation')

ax1.set_xlabel('wavelength')
ax2.set_xlabel('wavelength')
ax3.set_xlabel('frequency')
ax4.set_xlabel('frequency')

ax1.set_ylabel('ratio')
ax2.set_ylabel('ratio')
ax3.set_ylabel('ratio')
ax4.set_ylabel('ratio')

ax1.set_title('Reflectance')
ax2.set_title('Transmittance')
ax3.set_title('Reflectance')
ax4.set_title('Transmittance')

ax1.legend(loc='best')
ax2.legend(loc='best')
ax3.legend(loc='best')
ax4.legend(loc='best')

ax1.grid(True)
ax2.grid(True)
ax3.grid(True)
ax4.grid(True)

#ax1.set_ylim(0,1)
#ax2.set_ylim(0,1)
#ax3.set_ylim(0,1)
#ax4.set_ylim(0,1)

fig.savefig(savepath+"Simul vs Theory.png")
plt.close()

####################################### Src graph #########################################

Srcgraph = plt.figure(figsize=(31,9))

ax1 = Srcgraph.add_subplot(131)
ax1.set_title("freq vs "+r"$E_{\omega}$")
ax1.plot(freq/1.e12, abs(Ex_src_ft)**2, label=r'$E_{src}(\omega)$')
ax1.plot(freq/1.e12, abs(Ex_ref_ft)**2, label=r'$E_{ref}(\omega)$')
ax1.plot(freq/1.e12, abs(Ex_trs_ft)**2, label=r'$E_{trs}(\omega)$')
ax1.set_xlabel('freq, THz')
ax1.set_ylabel('ratio')
ax1.legend(loc='best')
ax1.grid(True)

ax2 = Srcgraph.add_subplot(132)
ax2.set_title("wavelength vs " + r"$E_{\omega}$")
ax2.plot(wl/nm, abs(Ex_src_ft)**2, label=r'$E_{src}(\lambda)$')
ax2.plot(wl/nm, abs(Ex_ref_ft)**2, label=r'$E_{ref}(\lambda)$')
ax2.plot(wl/nm, abs(Ex_trs_ft)**2, label=r'$E_{trs}(\lambda)$')
ax2.set_xlabel('wavelength, nm')
ax2.legend(loc='best')
ax2.grid(True)

ax3 = Srcgraph.add_subplot(133)
ax3.set_title('src vs inp, $t_c = %gdt $' %(tc/dt))
#ax3.plot(tsteps.real[0:int(4*tc/dt)],((Ex_src.real)**2)[0:int(4*tc/dt)], label=r'$|E_x(t)|^2,src$')
#ax3.plot(tsteps.real[0:int(4*tc/dt)],((Ex_inp.real)**2)[0:int(4*tc/dt)], label=r'$|E_x(t)|^2,inp$')
# ax3.plot(tsteps.real[0:int(4*tc/dt)], Ex_src.real[0:int(4*tc/dt)], label=r'$E_x(t),src$')
ax3.plot(tsteps.real[0:int(4*tc/dt)], Ex_inp.real[0:int(4*tc/dt)], color='b',label=r'$E_x(t),inp,real$')
ax3.plot(tsteps.real[0:int(4*tc/dt)], Ex_inp.imag[0:int(4*tc/dt)], color='r',label=r'$E_x(t),inp,imag$')
# ax3.plot(tsteps.real[0:int(4*tc/dt)], (abs(Ex_src)**2)[0:int(4*tc/dt)], label=r'$|E_x(t)|^{2},src$')
# ax3.plot(tsteps.real[0:int(4*tc/dt)], (abs(Ex_inp)**2)[0:int(4*tc/dt)], label=r'$|E_x(t)|^{2},inp$')
ax3.get_xaxis().set_visible(False)
ax3.text(2000,1.5,r'$E(t)=e^{-\frac{1}{2}(\frac{t-t_c}{ts})^{2}}\cos(\omega_{0}(t-t_c))$', fontsize=18)
# ax3.set_ylim(0,)
ax3.legend()
ax3.grid(True)

divider = make_axes_locatable(ax3)
ax4 = divider.append_axes("bottom",size="100%",pad=0.2, sharex=ax3)
ax4.plot(tsteps.real[0:int(4*tc/dt)],((Ex_ref.real)**2)[0:int(4*tc/dt)], label=r'$|E_r(t)|^2$',color='green')
ax4.plot(tsteps.real[0:int(4*tc/dt)],((Ex_trs.real)**2)[0:int(4*tc/dt)], label=r'$|E_t(t)|^2$',color='red')
#ax4.set_ylim(0,)
ax4.set_xlabel('time step, dt=%.2g' %(dt))
ax4.legend()
ax4.grid(True)
Srcgraph.savefig(savepath + 'Srcgraph.png')


print("Plotting Finished")
############################################################################################
################################### CLOUD SYNCHRONIZING ####################################
############################################################################################

print("Start uploading to Dropbox")
myname = os.path.basename(__file__)

# os.system('/root/dropbox_uploader.sh upload /root/3D_PSTD/%s Python/MyPSTD/3D_PSTD' %myname)

'''
Here goes, read in a coast line file, filter to desired region, check support SRTM grid,
see if it's on a wet cell, if not then search for nearest wet cell.

'''

from numpy import r_,where,meshgrid,reshape,argsort,squeeze,linspace,savetxt,c_,diff,zeros,arange
from netCDF4 import Dataset
from scipy.interpolate import interp1d

#Coquimbo
offset=1  #this is how many points "into teh ocean" to go after you find the wet/dry transition
srtm_file=u'/Users/dmelgar/DEMs/coquimbo/geoclaw/coquimbo_30_geoclaw.grd'
fout=u'/Users/dmelgar/Coquimbo2015/tsunami/coquimbo_30_coast_fg.txt'


#Read SRTM data
srtm = Dataset(srtm_file, 'r', format='NETCDF4')
try:
    x=srtm.variables['x'][:]
    y=srtm.variables['y'][:]
    z=srtm.variables['z'][:]
except:
    x=srtm.variables['lon'][:]
    y=srtm.variables['lat'][:]
    z=srtm.variables['z'][:]
ilat=range(0,len(y),4)
y=y[ilat]
z=z[ilat,:]
srtm_lon,srtm_lat=meshgrid(x,y)

#Go line by line in srtm grid, finds bathy and get offfset point

lat_out=y.copy()
lon_out=zeros(lat_out.shape)
#Just look for negative points
#Go left to right
for k in range(srtm_lat.shape[0]):
    zslice=z[k,:]
    ibathy=where(zslice<0)[0]
    ibathy_diff=diff(ibathy)
    ifirst=where(ibathy_diff>1)[0]#This is the las contiguos point from left to right
    if len(ifirst)==0: #no anomalies pick last negative
        ifirst=ibathy[-1]
    else: #Pick last contiguos
        ifirst=ifirst[0]
    lon_out[k]=srtm_lon[k,ifirst-offset]

#Decimate if you don;t want to save every point
#idec=arange(0,len(lon_out),2)
#lon_out=lon_out[idec]
#lat_out=lat_out[idec]
    

savetxt(fout,c_[lon_out,lat_out],fmt='%.8f\t%.8f')
            

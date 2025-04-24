import xarray as xr
import matplotlib.pyplot as plt

data = xr.open_dataset("path/to/gistemp.nc")  
data_decadal = data.resample(time="10Y").mean()  
data_decadal.temperature.plot(x="lon", y="lat", col="time", col_wrap=5) 
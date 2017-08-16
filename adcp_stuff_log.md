# Use ADCP raw data for biomass estimation

## Daily log
### 2017/08/09
- Install CODAS+UHDAS following instructions [here](https://currents.soest.hawaii.edu/antarctic/gentoo_www/programs/adcp_doc/codas_setup/index.html). Used Option#2 the Anaconda route. In the middle there was a dependency issue with python 3.5 when trying to install `wxpython`, so switched to python 2.7 and update the enture Anaconda package and all installation went fine.
- Successfully plot out single-ping data using function `Multiread`

### 2017/08/10
* Timestamp issue for each ping --> use `datetime.timedelta` to solve the problem
* Check all 4 beams together and can see difference among them
* Need to figure out if `data.dep` is the real depth or range (without compensating the tilt beam angle)
	- `data.dep` comes from `ppd.dep` in the function `readraw` directly, so it seems like that the depth has been processed before the files are saved
* Need to figure out what `data.amp` is, which seems to follow a `-120*log10(r)` line, where `r` is range in meters
	- In [ADCP best practices](https://currents.soest.hawaii.edu/docs/doc/best_practices.html) under **Single-ping Editing** it says "Screen for amplitude (acoustic intensity) spikes, ...," which seems to indicate that `data.amp` has the unit of intensity
* Need to check how the background average vary with number of files in the average and how runnning average changes over time

### 2017/08/12
* Use data from day 209 (July 29, which runs for 24 hrs with only a small gap in between) to verify that the timestamp conversion from `data.dday` is working fine.
* Wrote function `dday2timestr` to convert `data.dday` to str of timestamp




## Random tips
* To access single-ping ADCP data using python: [here](https://currents.soest.hawaii.edu/antarctic/gentoo_www/programs/adcp_doc/adcp_access/DIRECT_ACCESS/Python/ADCPraw/index.html)
* use `jdcal` package to convert julien day to gregorian calendar date (first tried package `julian` but it only works for >=python 3.2)
* [CODAS processing manual](https://currents.soest.hawaii.edu/antarctic/gentoo_www/programs/adcp_doc/local_doc/manual.pdf): include all computation details and definitions of terms
* To get system config info: use `m.sysconfig` to return `{'angle': 30, 'convex': True, 'kHz': 150, 'up': False}`
* **RRSI** = Received Signal Strength Indicator = output from BBADCP
* Reading RAW file from adcp: [here](ftp://ftp.nodc.noaa.gov/nodc/archive/arc0039/0082184/1.1/data/0-data/KN201L01/adcp/programs/adcp_doc/UHDAS_scidoc/Processing/singleping.html)
* Use `np.nditer` to make a single `numpy.float64` scalar workable in list comprehension
* Use `arlpy.uwa` toolbox in `aplpy` to calculate absorption. [Link to package](https://pypi.python.org/pypi/arlpy/1.0).
* `data.rVL` is a `numpy.recarray` (record array) object. It contains all the ping timing (in year-month-day-hour-min-sec form and not dday) as well as sound speed/salinity/temperature recordings. Although couldn't figure out the unit of the temperature recording as the numbers are in the 1050-1060 range??
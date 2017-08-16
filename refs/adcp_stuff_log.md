# Use ADCP raw data for biomass estimation

## Daily log
### 2017/08/09
- Install CODAS+UHDAS following instructions [here](https://currents.soest.hawaii.edu/antarctic/gentoo_www/programs/adcp_doc/codas_setup/index.html). Used Option#2 the Anaconda route. In the middle there was a dependency issue with python 3.5 when trying to install `wxpython`, so switched to python 2.7 and update the enture Anaconda package and all installation went fine.
- Successfully plot out single-ping data using function `Multiread`

### 2017/08/10
* Figure out timestamp issue for each ping
* Check all 4 beams together and can see difference among them
* Need to figure out if `data.dep` is the real depth or range (without compensating the tilt beam angle)
	- `data.dep` comes from `ppd.dep` in the function `readraw` directly, so it seems like that the depth has been processed before the files are saved
* Need to figure out what `data.amp` is, which seems to follow a `-120*log10(r)` line, where `r` is range in meters
	- In [ADCP best practices](https://currents.soest.hawaii.edu/docs/doc/best_practices.html) under **Single-ping Editing** it says "Screen for amplitude (acoustic intensity) spikes, ...," which seems to indicate that `data.amp` has the unit of intensity
* Need to check how the background average vary with number of files in the average and how runnning average changes over time


## Random tips
* To access single-ping ADCP data using python: [here](https://currents.soest.hawaii.edu/antarctic/gentoo_www/programs/adcp_doc/adcp_access/DIRECT_ACCESS/Python/ADCPraw/index.html)
* use `jdcal` package to convert julien day to gregorian calendar date (first tried package `julian` but it only works for >=python 3.2)
* [CODAS processing manual](https://currents.soest.hawaii.edu/antarctic/gentoo_www/programs/adcp_doc/local_doc/manual.pdf): include all computation details and definitions of terms
* To get system config info: use `m.sysconfig` to return `{'angle': 30, 'convex': True, 'kHz': 150, 'up': False}`
* **RRSI** = Received Signal Strength Indicator = output from BBADCP

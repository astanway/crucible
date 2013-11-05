## Crucible

![x](https://raw.github.com/astanway/crucible/master/example.jpg)

Crucible is a refinement and feedback suite for algorithm testing. It was
designed to be used to create anomaly detection algorithms, but it is very
simple and can probably be extended to work with your particular domain. It
evolved out of a need to test and rapidly generate standardized feedback for
iterating on anomaly detection algorithms.

## How it works

Crucible uses its library of timeseries in `/data` and tests all the
algorithms in algorithms.py on all these data. It builds the timeseries
datapoint by datapoint, and runs each algorithm at every step, as a way of
simulating a production environment. For every anomaly it detects, it draws a
red dot on the x value where the anomaly occured. It then saves each graph to
disk in `/results` for you to check, grouped by algorithm-timeseries.

To be as fast as possible, Crucible launches a new process for each timeseries.

If you want to add an algorithm, simply create your algorithm in algorithms.py
and add it to settings.py as well so Crucible can find it. Crucible comes
loaded with a bunch of stock algorithms from an early
[Skyline](http://github.com/etsy/skyline) release, but it's designed for you to
write your own and test them.

## Dependencies
Standard python data science suite - everything is listed in algorithms.py

1. Install numpy, scipy, pandas, patsy, statsmodels, matplotlib.

2. You may have trouble with SciPy. If you're on a Mac, try:

* `sudo port install gcc48`
* `sudo ln -s /opt/local/bin/gfortran-mp-4.8 /opt/local/bin/gfortran`
* `sudo pip install scipy`

On Debian, apt-get works well for Numpy and SciPy. On Centos, yum should do the
trick. If not, hit the Googles, yo.

## Instructions

Just call `python src/crucible.py`. Then check the `/results` folder for the results.
Happy algorithming!

## To add a timeseries:

Create a json array of the form `[[timestamp, datapoint], [timestamp],
datapoint]]`. Put it in the `/data` folder. Done.

## Graphite integration:
There's a small tool to easily grab Graphite data and analyze it. Just call
`python utils/graphite-grab.py
"your_graphite.com/render/?from=-24hour&target=your.metric&format=json"`
and the script will grab Graphite data, format it, and put it into `/data` for you.

## Contributions

It would be fantastic to have a robust library of canonical timeseries data.
Please, if you have a timeseries that you think a good anomaly detection
algorithm should be able to handle, share the love and add the timeseries to
the suite!

![x](https://raw.github.com/astanway/crucible/master/metalworker.jpg)



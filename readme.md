## Crucible

![x](https://raw.github.com/astanway/crucible/master/metalworker.jpg)

Crucible is a refinement and feedback suite for algorithm testing. It was
designed to be used to create anomaly detection algorithms, but it is very
simple and can probably be extended to work with your particular domain.

## How it works

Crucible uses its library of timeseries in /timeseries and tests all the
algorithms in algorithms.py on all these data. It builds the timeseries
datapoint by datapoint, and runs each algorithm at every step, as a way of
simulating a production environment. For every anomaly it detects, it draws a
red dot on the x value where the anomaly occured. It then saves each graph to
disk in results/ for you to check, grouped by algorithm-timeseries.

To be as fast as possible, Crucible launches a new process for each timeseries.

If you want to add an algorithm, simply create your algorithm in algorithms.py
and add it to settings.py as well so Crucible can find it.

## Instructions

Just call `python crucible.py`. Then check the /results folder for the results.
Happy algorithming!

![x](https://raw.github.com/astanway/crucible/master/example.jpg)

## Contributions

It would be fantastic to have a robust library of data. Please, if you have a
timeseries that you think a good anomaly detection algorithm should be able to
handle, submit a pull request!

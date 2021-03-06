# Displaying the times of upcoming buses to a specific stop on an inky phat and raspberry pi.
## What
This is a small script for displaying the upcoming arrivals of busses at a specific bus stop (in the uk).

This is meant to work with the inky phat pi top

https://shop.pimoroni.com/products/inky-phat?variant=12549254217811

It also (if you want it to) will output the results to the command line.

## To do first
Follow these instructions:
https://learn.pimoroni.com/tutorial/sandyj/getting-started-with-inky-phat

I found that I had to enable I2C (found in raspi-config / Interfacing Options) as a separate step.

Have a play and then...

## Need to do
You'll need to update the file `example_config.json` to `config.json` so that you may also want to add a different default bus stop.

I've used the api's here: https://api-portal.tfl.gov.uk/docs to figure out stop points.

## How to run
To run so that it outputs to the console.

```python3 inky_bus.py```

To run on an inky phat you'll need to add --inky (or -i): 

```python3 inky_bus.py --inky "true"```

Congrats you now know what buses you can get from a very specific bus stop that's near (ish) my house!

You can also turn off the output to the command line.

```python3 inky_bus.py --cmd "true"```

So to set it running in the background on a raspberry pi and not to worry about it...

```python3 inky_bus.py --inky "true" --cmd "false" &```

You can also override the stop from the config file.

```python3 inky_bus.py --stop "490007732S"```

I've gone with adding this to the crontab, this will have it run every 2 minutes.

```*/2 * * * * /home/pi/git_repos/inky-bus/inky_bus.py -i "true" -c "false"```

## Changing this to a Covid-19 tracker

The data is coming from https://github.com/javieraviles/covidAPI

You can now run this as a covid-19 tracker (I'm still not sure this is a good idea). This will output to your inky (or with `-c true` your terminal) the details for a random country.

```python3 inky_bus.py -f covid -i true```

You can add the country name with --country (or `-ct` e.g. `-ct UK`) for a specific country:


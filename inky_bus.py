import argparse
from bus_times import getBusTime, mapBusTimesToOutput
from config import getConfig
from display import displayCmd, displayInky
argParser = argparse.ArgumentParser()
argParser.add_argument('--inky', '-i', type=str, required=False, choices=["true", "false"], default="false", help="Display to inky default false")
argParser.add_argument('--cmd', '-c', type=str, required=False, choices=["true", "false"], default="true", help="Display to command line default true")
argParser.add_argument('--stop', '-s', type=str, required=False, default="", help="The stop point for the bus stop.")
args = argParser.parse_args()




config = getConfig()
stopEndPoint = config['stopEndPoint']
stop = (args.stop, config['stop'])[args.stop == '']

if args.cmd == "true":
    displayCmd(mapBusTimesToOutput(getBusTime(stopEndPoint, stop)))
    
if args.inky == "true":
    busTimes = getBusTime(stopEndPoint, stop)
    displayInky(mapBusTimesToOutput(busTimes))


raise SystemExit
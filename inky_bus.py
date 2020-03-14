import argparse
from config import getConfig
from display import displayCmd, displayInky


argParser = argparse.ArgumentParser()
argParser.add_argument('--inky', '-i', type=str, required=False, choices=["true", "false"], default="false", help="Display to inky default false")
argParser.add_argument('--cmd', '-c', type=str, required=False, choices=["true", "false"], default="true", help="Display to command line default true")
argParser.add_argument('--stop', '-s', type=str, required=False, default="", help="The stop point for the bus stop.")
argParser.add_argument('--function', '-f', type=str, required=False, choices=["bus", "country", "covid"], default="bus", help="What functionality to use")
argParser.add_argument('--country', '-ct', type=str, required=False, default="", help="What country to look at if left empty a random country is chosen.")
args = argParser.parse_args()

config = getConfig()
if args.function == "country":
    from country_details import getOutput
    endPoint = config['countryEndPoint']
    code = "GB"
elif args.function == "covid":
    from covid import getOutput
    endPoint = config['covidEndPoint']
    code = args.country
else:
    from bus_times import getOutput
    endPoint = config['stopEndPoint']
    code = (args.stop, config['stop'])[args.stop == '']

output = getOutput(endPoint, code)

if args.cmd == "true":
    displayCmd(output)
    
if args.inky == "true":
    displayInky(output)


raise SystemExit
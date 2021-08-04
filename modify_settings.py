import json
from quick_start import start_keys
import sys
from math import log10
from binance.client import Client
from BinanceKeys import *

def print_parameters():
    """Prints a list of all the parameters"""

    f=open('settings/parameters.json')
    parameters=json.load(f)
    f.close()

    str_fmt = "{:<20} {:<15}"
    print('\n')
    print(str_fmt.format('parameter name','value'))
    for key in parameters:
        print('--------------------------')
        print(str_fmt.format(key, parameters[key]))
    print('\n')


def modify_parameters(constant_to_modify):
    """Modifies a constant in the settings/parameters.json file
    
    Args:
        constant_to_modify (str): name of the constant to modify: asset1, asset2, interval, short_span, long_span. (and rounding, should be computed automatically)
    """

    f=open('settings/parameters.json')
    parameters=json.load(f)
    f.close()
    parameters[constant_to_modify]=input('Please input a new value for '+constant_to_modify+':\n')
    if constant_to_modify=='asset1' or constant_to_modify=='asset2':
        parameters[constant_to_modify]=parameters[constant_to_modify].upper()
        client = Client(key(), secretKey())
        rounding=int((-log10(float(client.get_symbol_info(parameters['asset1']+parameters['asset2'])['filters'][2]['stepSize']))))
        parameters['rounding']=rounding
        print('rounding changed')
    with open('settings/parameters.json', 'w') as f:
        json.dump(parameters, f)
    print(constant_to_modify, ' changed to ', parameters[constant_to_modify])

while True:
    category=input('Please enter: \n1: if you want to change the API keys \n2: if you want to modify the parameters\n You can exit this menu anytime by entering 0:\n')
    if category=='0':
        print('Done!')
        break
    if category=='1':
        start_keys()
    elif category=='2':
        while True:
            print_parameters()
            parameter_dict={'1':'asset1', '2':'asset2','3':'interval','4':'short_span','5':'long_span', '6':'database'}
            parameter_to_change=input('Please indicate which constant you want to modify by entering its number:\n1. asset1, \n2. asset2, \n3. interval, \n4. short_span, \n5. long_span\n6. database\n Enter 00 to go back or 0 to exit\n')
            if parameter_to_change=='00':
                break
            if parameter_to_change =='0':
                sys.exit('Done!')
            try:
                modify_parameters(parameter_dict[parameter_to_change])
                print('success!', parameter_dict[parameter_to_change], ' has been changed.')
            except KeyError: 
                print(parameter_to_change, ' value not recognized, let\'s try again!')
                continue
            
          
                



    


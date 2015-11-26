####################################################################################################

import os

####################################################################################################

import PySpice.Logging.Logging as Logging
logger = Logging.setup_logging()

####################################################################################################

from PySpice.Spice.Library import SpiceLibrary
from PySpice.Spice.Netlist import Circuit
from PySpice.Spice.Parser import SpiceParser
from PySpice.Unit.Units import *

####################################################################################################

libraries_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'libraries')
spice_library = SpiceLibrary(libraries_path)

####################################################################################################

circuit = Circuit('STM AN1476: Low-Cost Power Supply For Home Appliances')

circuit.include(spice_library['1N4148'])
# 1N5919B: 5.6 V, 3.0 W Zener Diode Voltage Regulator
circuit.include(spice_library['d1n5919brl'])

ac_line = circuit.AcLine('input', 'out', 'in', rms_voltage=230, frequency=50)
circuit.R('load', 'out', circuit.gnd, kilo(1))
circuit.C('load', 'out', circuit.gnd, micro(220))
circuit.X('D1', '1N4148', circuit.gnd, 1)
circuit.D(1, circuit.gnd, 1, model='DIODE1', off=True)
circuit.X('Dz1', 'd1n5919brl', 1, 'out')
circuit.C('ac', 1, 2, nano(470))
circuit.R('ac', 2, 'in', 470, m=1, temperature='{25}')

source = str(circuit)
print(source)

####################################################################################################

parser = SpiceParser(source=source)
bootstrap_circuit = parser.build_circuit()

bootstrap_source = str(bootstrap_circuit)
print(bootstrap_source)

# Fxime: include order
assert(source == bootstrap_source)

####################################################################################################
#
# End
#
####################################################################################################

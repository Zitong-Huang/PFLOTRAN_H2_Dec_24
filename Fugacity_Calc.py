import preos
# pass name, Tc [K], Pc [bar], omega
# https://www.osti.gov/servlets/purl/1145508
hydrogen = preos.Molecule("hydrogen", 33.145, 12.96, -0.216)
hydrogen.print_params()

# pass the Molecule, T [K], P [bar] of interest
props = preos.preos(hydrogen, 62.5+273.15, 125, plotcubic=True, printresults=True)

# https://www.engineeringtoolbox.com/hydrogen-sulfide-H2S-properties-d_2034.html
# https://www.kaylaiacovino.com/Petrology_Tools/Critical_Constants_and_Acentric_Factors.htm
hydrogen_sulfide = preos.Molecule("hydrogen sulfide", 373.3, 89.7, 0.081)
hydrogen_sulfide.print_params()

# https://www.sciencedirect.com/science/article/pii/S0376738815003713?via%3Dihub
props = preos.preos(hydrogen_sulfide, 62.5+273.15, 125, plotcubic=True, printresults=True)
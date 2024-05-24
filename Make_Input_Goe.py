import numpy as np
import pandas as pd
import openpyxl
import os

from openpyxl import load_workbook

#========================
# Reading LHS parameters
#========================
# Load the Excel file
df = pd.read_excel("./LHS_Parameters.xlsx", engine='openpyxl')

array1 = df['Fe_Wt']
array2 = df['Fe_Ratio']*100
array2 = array2.astype(int)

# Function to read specified cells from an Excel file
def read_excel_cells(filename):
    # Load the Excel workbook
    wb = load_workbook('./Parameter_Spaces/' + filename, data_only=True)
    sheet = wb.active  # or wb['YourSheetName']

    # Read the values from cells O4 to O9
    cell_values = [sheet[f'O{i}'].value for i in range(4, 10)]

    return cell_values

# Array to store the results
vol_perc = []

# Iterate through the elements of the arrays
for i in range(len(array1)):
    # Construct the filename based on the ith elements of array1 and array2
    filename = f"Goe_{array1[i]}_{array2[i]}.xlsx"

    try:
        # Read the specified cells from the Excel file
        cell_values = read_excel_cells(filename)
        vol_perc.append(cell_values)
    except FileNotFoundError:
        print(f"File not found: {filename}")
    except Exception as e:
        print(f"An error occurred while reading {filename}: {e}")

# Convert the results to a NumPy array for easier handling
vol_perc = np.array(vol_perc)
n = 1198 #22 #300

Qua_vol = vol_perc[:, 0].reshape(n, 1).flatten()
Cal_vol = vol_perc[:, 1].reshape(n, 1).flatten()
Pyr_vol = vol_perc[:, 2].reshape(n, 1).flatten()
Goe_vol = vol_perc[:, 3].reshape(n, 1).flatten()
Kao_vol = vol_perc[:, 4].reshape(n, 1).flatten()
Hem_vol = vol_perc[:, 5].reshape(n, 1).flatten()

np.savetxt('Pyr_vol.txt', Pyr_vol, fmt='%f')
np.savetxt('Goe_vol.txt', Goe_vol, fmt='%f')

# Temp = np.array(df['Temp'])
# Sw = np.array(df['Sw'])
# Log_SA = np.array(df['SA'])
# Logk_Pyr = np.array(df['Logk_Pyr'])
# Logk_Hem = np.array(df['Logk_Hem'])
# Logk_Goe = np.array(df['Logk_Goe'])
#
#
# #===========================
# # Writing to the input files
# #===========================
# def write_from_base(T, S_w, Liq_inj_rate, H2_PP, L_SA, L_Pyr, L_Goe, Q_v, C_v, P_v, G_v, K_v, fid):
#     if G_v == 0:
#         G_v = 1.0e-16
#
#     print(f"""
# SIMULATION
#   SIMULATION_TYPE SUBSURFACE
#   PROCESS_MODELS
#     SUBSURFACE_FLOW flow
#       MODE GENERAL ! two-phase flow and energy
#       OPTIONS
#         GAS_COMPONENT_FORMULA_WEIGHT 2.016d0  !H2
#         CHECK_MAX_DPL_LIQ_STATE_ONLY
#         RESTRICT_STATE_CHANGE
#       /
#     /
#     SUBSURFACE_TRANSPORT transport
#       MODE GIRT
#     /
#   /
# END
#
# SUBSURFACE
# !!=========================== chemistry ========================================
# CHEMISTRY
#   PRIMARY_SPECIES
#     Al+++
#     Ca++
#     Cl-
#     CO2(aq)
#     Fe+++
#     H+
#     HS-
#     H2(aq)
#     Methane(aq)
#     Na+
#     SiO2(aq)
#     Tracer
#   /
#   DECOUPLED_EQUILIBRIUM_REACTIONS
#     Methane(aq)
#   /
#   SECONDARY_SPECIES
#     Al(OH)4-
#     Al(OH)3(aq)
#     CaCO3(aq)
#     CaHCO3+
#     CaSO4(aq)
#     CO3--
#     Fe++
#     FeCl+
#     Fe(OH)2(aq)
#     Fe(OH)3(aq)
#     Fe(OH)3-
#     Fe(OH)4-
#     FeSO4+
#     FeSO4(aq)
#     HCO3-
#     HSO4-
#     H2S(aq)
#     H2SiO4--
#     H3SiO4-
#     NaHCO3(aq)
#     NaCO3-
#     O2(aq)
#     OH-
#     S--
#     SO4--
#   /
#   ACTIVE_GAS_SPECIES
#     GAS_TRANSPORT_IS_UNVETTED
#     H2(g)
#   /
#   PASSIVE_GAS_SPECIES
#     O2(g)
#     CH4(g)
#     H2(g)
#     CO2(g)
#     H2S(g)
#   /
#   MINERALS
#     Anhydrite
#     Calcite
#     Pyrite
#     Quartz
#     Kaolinite
#     Pyrrhotite
#     Goethite
#   /
#   MINERAL_KINETICS
#     Calcite
#       RATE_CONSTANT -5.81d0
#       ACTIVATION_ENERGY 23500d0
#     /
#     Pyrite
#       RATE_CONSTANT {L_Pyr}d0
#       ACTIVATION_ENERGY 56900d0
#     /
#     Quartz
#       RATE_CONSTANT -13.40d0
#       ACTIVATION_ENERGY 90900d0
#     /
#     Kaolinite
#       RATE_CONSTANT -13.18d0
#       ACTIVATION_ENERGY 22200d0
#     /
#     Anhydrite
#       RATE_CONSTANT -3.19d0
#       ACTIVATION_ENERGY 14300d0
#     /
#     Pyrrhotite
#       RATE_CONSTANT -8.04d0
#       ACTIVATION_ENERGY 50800d0
#     /
#     Goethite
#       RATE_CONSTANT {L_Goe}d0
#       ACTIVATION_ENERGY 86500d0
#     /
#   /
#
#   DATABASE ./hanford.dat
#   LOG_FORMULATION
#   UPDATE_POROSITY
#   UPDATE_PERMEABILITY
#   MOLALITY
#
#   OUTPUT
#     TOTAL
#      PH
#      MINERALS
#      MINERAL_SATURATION_INDEX
#      GASES
#      PRIMARY_SPECIES
#      SECONDARY_SPECIES
#    /
# END
#
# !!=========================== discretization ===================================
# GRID
#   TYPE structured
#   ORIGIN 0.d0 0.d0 0.d0
#   NXYZ 125 125 10
#   DXYZ
#     125*1.6d1
#     125*1.6d1
#     10*2.d1
#   /
# END
#
# !!=========================== solver options ===================================
# NUMERICAL_METHODS FLOW
#   TIMESTEPPER
#     TS_ACCELERATION 8
#     MAX_STEPS 100000000
#   /
#
#   NEWTON_SOLVER
#     ATOL 1D-12
#     RTOL 1D-12
#     STOL 1D-6
#     DTOL 1D15
#     ITOL 1D-8
#     MAXIMUM_NUMBER_OF_ITERATIONS 8
#     MAXF 500
#   /
#
#   LINEAR_SOLVER
#     SOLVER IBCGS !GMRES !ITERATIVE !BCGS !DIRECT
#   /
# END
#
# NUMERICAL_METHODS TRANSPORT
#   TIMESTEPPER
#     TS_ACCELERATION 8
#     MAX_STEPS 100000000
#   /
#
#   NEWTON_SOLVER
#     ATOL 1D-12
#     RTOL 1D-12
#     STOL 1D-5
#     DTOL 1D15
#     ITOL 1D-7
#     MAXIMUM_NUMBER_OF_ITERATIONS 8
#     MAXF 500
#   /
#
#   LINEAR_SOLVER
#     SOLVER IBCGS !IBCGS !GMRES !BCGS !DIRECT
#   /
# END
#
# !!=========================== times ============================================
# TIME
#   FINAL_TIME 1.d0 y
#   INITIAL_TIMESTEP_SIZE 1.d-10 y
#   MAXIMUM_TIMESTEP_SIZE 1.d-2 y
# END
#
# !!=========================== output options ===================================
# OUTPUT
#   TIMES y 8.333d-2 1.667d-1 2.500d-1 3.333d-1 4.167d-1 5.000d-1 5.833d-1 6.667d-1 7.500d-1 8.333d-1 9.167d-1 1.000d0
#   FORMAT VTK
#   MASS_BALANCE_FILE
#     PERIODIC TIME 8.33d-2 y
#     TOTAL_MASS_REGIONS
#       well
#       gas_res
#     /
#     !DETAILED
#   /
#   VARIABLES
#     LIQUID_PRESSURE
#     LIQUID_DENSITY
#     LIQUID_MOLE_FRACTIONS
#     LIQUID_SATURATION
#     GAS_PRESSURE
#     GAS_DENSITY
#     GAS_SATURATION
#     GAS_MOLE_FRACTIONS
#     MAXIMUM_PRESSURE
#     CAPILLARY_PRESSURE
#     POROSITY
#     PERMEABILITY_X
#     PERMEABILITY_Y
#     PERMEABILITY_Z
#   /
# PERIODIC_OBSERVATION TIMESTEP 1000
# END
#
# !!=========================== fluid properties =================================
# FLUID_PROPERTY
#   PHASE LIQUID
#   DIFFUSION_COEFFICIENT 5.5d-9
# END
#
# FLUID_PROPERTY
#   PHASE GAS
#   DIFFUSION_COEFFICIENT 1.0d-8  ![m2/s]
# END
#
# EOS WATER
#   DENSITY DEFAULT
#   VISCOSITY DEFAULT
# END
#
# EOS GAS
#   DENSITY RKS
#     HYDROGEN
#   /
#   VISCOSITY CONSTANT 1.025e-5
#   FORMULA_WEIGHT 2.016d0
#   HENRYS_CONSTANT DEFAULT
# END
#
# !!=========================== material properties ==============================
# MATERIAL_PROPERTY rock
#   ID 1
#   POROSITY 2.0d-1
#   ROCK_DENSITY 2.7d3
#   SATURATION_FUNCTION unsat
#   THERMAL_CONDUCTIVITY_DRY 2.5d0
#   THERMAL_CONDUCTIVITY_WET 2.2d0
#   HEAT_CAPACITY 820.d0
#   PERMEABILITY_MIN_SCALE_FACTOR 0.0d0
#   PERMEABILITY_POWER 3.0d0
#   PERMEABILITY
#     PERM_ISO 1.974e-13
#   /
# END
#
# MATERIAL_PROPERTY well_region
#   ID 2
#   POROSITY 0.21d0
#   !TORTUOSITY 1.0d0
#   !LONGITUDINAL_DISPERSIVITY 1.d-3   ![m] for [m2/s] calculation
#   !TRANSVERSE_DISPERSIVITY_H 1.d-4
#   !TRANSVERSE_DISPERSIVITY_V 1.d-4
#   ROCK_DENSITY 2.7d3
#   SATURATION_FUNCTION unsat
#   THERMAL_CONDUCTIVITY_DRY 2.5d0
#   THERMAL_CONDUCTIVITY_WET 2.2d0
#   HEAT_CAPACITY 820.d0
#   PERMEABILITY_MIN_SCALE_FACTOR 0.0d0
#   PERMEABILITY_POWER 3.0d0
#   PERMEABILITY
#     PERM_X 1.974e-13
#     PERM_Y 1.974e-13
#     PERM_Z 3.974e-13
#   /
# END
#
# !!=========================== characteristic curves ============================
# CHARACTERISTIC_CURVES unsat
#   SATURATION_FUNCTION VAN_GENUCHTEN
#     LOOP_INVARIANT
#     UNSATURATED_EXTENSION ECPC
#     ALPHA  1.d-4
#     M 0.5d0
#     LIQUID_RESIDUAL_SATURATION 1.d-1
#     MAX_CAPILLARY_PRESSURE 1.0d7
#   /
#   PERMEABILITY_FUNCTION MUALEM_VG_LIQ
#     PHASE LIQUID
#     M 0.3d0
#     LIQUID_RESIDUAL_SATURATION 1.d-1
#     SMOOTH
#   /
#   PERMEABILITY_FUNCTION MUALEM_VG_GAS
#     PHASE GAS
#     M 0.3d0
#     LIQUID_RESIDUAL_SATURATION 1.d-1
#     GAS_RESIDUAL_SATURATION 1.d-2
#   /
# END
#
# !!=========================== regions ==========================================
# REGION all
#   COORDINATES
#     0.0d0 0.0d0 0.0d0
#     2.0d3 2.0d3 2.0d2
#   /
# END
#
# REGION well
#   BLOCK 63 63 63 63 5 10
# END
#
# REGION gas_res
#   BLOCK 1 125 1 125 1 10
# END
#
# !!======================== flow conditions =================
# FLOW_CONDITION initial
#   # UNITS Pa,C,M,yr
#   TYPE
#     LIQUID_PRESSURE HYDROSTATIC
#     LIQUID_SATURATION DIRICHLET
#     GAS_PRESSURE DIRICHLET
#     TEMPERATURE DIRICHLET
#   /
#   LIQUID_PRESSURE 1.D7
#   GAS_PRESSURE 1.D7
#   LIQUID_SATURATION {S_w}
#   TEMPERATURE {T}
#   GRADIENT
#     LIQUID_PRESSURE 0.d0 0.d0 10530d0
#     TEMPERATURE  0.d0 0.d0 2.5d-2
#   /
# END
#
# FLOW_CONDITION gas_injection
#   TYPE
#     RATE SCALED_MASS_RATE VOLUME
#   /
#   RATE LIST
#     TIME_UNITS year
#     DATA_UNITS kg/year kg/year MW
#     0.d0 {Liq_inj_rate} 7.50d8 0.d0
#     2.5d-1 0.d0 0.d0 0.d0
#   /
# END
#
# !!=========================== transport conditions =============================
# TRANSPORT_CONDITION initial
#   TYPE DIRICHLET_ZERO_GRADIENT
#   CONSTRAINT_LIST
#     0.d0 initial
#   /
# END
#
# TRANSPORT_CONDITION inlet
#   TYPE DIRICHLET_ZERO_GRADIENT
#   CONSTRAINT_LIST
#     0.d0 inlet
#   /
# END
#
# !!=========================== constraints ======================================
# CONSTRAINT initial
#    CONCENTRATIONS
#        Al+++        4.0d-6       M Kaolinite
#        Tracer       1d-5         T
#        Na+          6.05d-1      T
#        Cl-          6.05d-1      T
#        H+           8.8d0        P
#        CO2(aq)      6.3d-4       M Calcite
#        Fe+++        2.0d-13      M Goethite
#        Ca++         6.3d-4       T
#        H2(aq)       1.0d-8       T
#        SiO2(aq)     8.1d-4       M Quartz
#        Methane(aq)  1.0d-3       T
#        HS-          6.0d-6       M Pyrite
#    /
#    MINERALS
#       Pyrite                {P_v}    {10**L_SA} m^2/g
#       Quartz                {Q_v}    {10**L_SA} m^2/g
#       Calcite               {C_v}    {10**L_SA} m^2/g
#       Kaolinite             {K_v}    {10**L_SA} m^2/g
#       Goethite              {G_v}    {10**L_SA} m^2/g
#       Anhydrite             1.0d-16  {10**L_SA} m^2/g
#       Pyrrhotite            1.0d-7   {10**L_SA} m^2/g
#    /
# END
#
# CONSTRAINT inlet
#    CONCENTRATIONS
#        Al+++        8.3d-8       M Kaolinite
#        Tracer       1d-5         T
#        Na+          5.49d-1      T
#        Cl-          5.49d-1      T
#        H+           7.3d0        P
#        CO2(aq)      3.8d-3       M Calcite
#        Fe+++        3.5d-20      T
#        Ca++         3.8d-3       T
#        H2(aq)       {H2_PP}      G H2(g)
#        SiO2(aq)     2.6d-4       M Quartz
#        Methane(aq)  1.0d-3       T
#        HS-          4.9d-3       M Pyrite
#    /
# END
#
# !!=========================== condition couplers ===============================
# # initial condition
# INITIAL_CONDITION gas_res
#   FLOW_CONDITION initial
#   TRANSPORT_CONDITION initial
#   REGION gas_res
# END
#
# # gas injection
# SOURCE_SINK well
#   FLOW_CONDITION gas_injection
#   TRANSPORT_CONDITION inlet
#   REGION well
# END
#
# !!=========================== stratigraphy couplers ============================
# STRATA
#   REGION all
#   MATERIAL rock
# END
#
# STRATA
#   REGION well
#   MATERIAL rock !well_region
# END
#
# END_SUBSURFACE
#
#
# """, file=fid)
#
#
# def write_from_base_NR(T, S_w, Liq_inj_rate, H2_PP, fid_NR):
#     print(f"""
# SIMULATION
#   SIMULATION_TYPE SUBSURFACE
#   PROCESS_MODELS
#     SUBSURFACE_FLOW flow
#       MODE GENERAL ! two-phase flow and energy
#       OPTIONS
#         GAS_COMPONENT_FORMULA_WEIGHT 2.016d0  !H2
#         CHECK_MAX_DPL_LIQ_STATE_ONLY
#         RESTRICT_STATE_CHANGE
#       /
#     /
#     SUBSURFACE_TRANSPORT transport
#       MODE GIRT
#     /
#   /
# END
#
# SUBSURFACE
# !!=========================== chemistry ========================================
# CHEMISTRY
#   PRIMARY_SPECIES
#     Al+++
#     Ca++
#     Cl-
#     CO2(aq)
#     Fe+++
#     H+
#     HS-
#     H2(aq)
#     Methane(aq)
#     Na+
#     SiO2(aq)
#     Tracer
#   /
#   DECOUPLED_EQUILIBRIUM_REACTIONS
#     Methane(aq)
#   /
#   SECONDARY_SPECIES
#     Al(OH)4-
#     Al(OH)3(aq)
#     CaCO3(aq)
#     CaHCO3+
#     CaSO4(aq)
#     CO3--
#     Fe++
#     FeCl+
#     Fe(OH)2(aq)
#     Fe(OH)3(aq)
#     Fe(OH)3-
#     Fe(OH)4-
#     FeSO4+
#     FeSO4(aq)
#     HCO3-
#     HSO4-
#     H2S(aq)
#     H2SiO4--
#     H3SiO4-
#     NaHCO3(aq)
#     NaCO3-
#     O2(aq)
#     OH-
#     S--
#     SO4--
#   /
#   ACTIVE_GAS_SPECIES
#     GAS_TRANSPORT_IS_UNVETTED
#     H2(g)
#   /
#   PASSIVE_GAS_SPECIES
#     O2(g)
#     CH4(g)
#     H2(g)
#     CO2(g)
#     H2S(g)
#   /
#   MINERALS
#     Anhydrite
#     Calcite
#     Pyrite
#     Quartz
#     Kaolinite
#     Pyrrhotite
#     Goethite
#   /
#   MINERAL_KINETICS
#     Calcite
#       RATE_CONSTANT -16.00d0
#       ACTIVATION_ENERGY 23500d0
#     /
#     Pyrite
#       RATE_CONSTANT -16.00d0
#       ACTIVATION_ENERGY 56900d0
#     /
#     Quartz
#       RATE_CONSTANT -16.00d0
#       ACTIVATION_ENERGY 90900d0
#     /
#     Kaolinite
#       RATE_CONSTANT -16.00d0
#       ACTIVATION_ENERGY 22200d0
#     /
#     Anhydrite
#       RATE_CONSTANT -16.00d0
#       ACTIVATION_ENERGY 14300d0
#     /
#     Pyrrhotite
#       RATE_CONSTANT -16.00d0
#       ACTIVATION_ENERGY 50800d0
#     /
#     Goethite
#       RATE_CONSTANT -16.00d0
#       ACTIVATION_ENERGY 86500d0
#     /
#   /
#
#   DATABASE ./hanford.dat
#   LOG_FORMULATION
#   UPDATE_POROSITY
#   UPDATE_PERMEABILITY
#   MOLALITY
#
#   OUTPUT
#     TOTAL
#      PH
#      MINERALS
#      MINERAL_SATURATION_INDEX
#      GASES
#      PRIMARY_SPECIES
#      SECONDARY_SPECIES
#    /
# END
#
# !!=========================== discretization ===================================
# GRID
#   TYPE structured
#   ORIGIN 0.d0 0.d0 0.d0
#   NXYZ 125 125 10
#   DXYZ
#     125*1.6d1
#     125*1.6d1
#     10*2.d1
#   /
# END
#
# !!=========================== solver options ===================================
# NUMERICAL_METHODS FLOW
#   TIMESTEPPER
#     TS_ACCELERATION 8
#     MAX_STEPS 100000000
#   /
#
#   NEWTON_SOLVER
#     ATOL 1D-12
#     RTOL 1D-12
#     STOL 1D-6
#     DTOL 1D15
#     ITOL 1D-8
#     MAXIMUM_NUMBER_OF_ITERATIONS 8
#     MAXF 500
#   /
#
#   LINEAR_SOLVER
#     SOLVER IBCGS !GMRES !ITERATIVE !BCGS !DIRECT
#   /
# END
#
# NUMERICAL_METHODS TRANSPORT
#   TIMESTEPPER
#     TS_ACCELERATION 8
#     MAX_STEPS 100000000
#   /
#
#   NEWTON_SOLVER
#     ATOL 1D-12
#     RTOL 1D-12
#     STOL 1D-5
#     DTOL 1D15
#     ITOL 1D-7
#     MAXIMUM_NUMBER_OF_ITERATIONS 8
#     MAXF 500
#   /
#
#   LINEAR_SOLVER
#     SOLVER IBCGS !IBCGS !GMRES !BCGS !DIRECT
#   /
# END
#
# !!=========================== times ============================================
# TIME
#   FINAL_TIME 1.d0 y
#   INITIAL_TIMESTEP_SIZE 1.d-10 y
#   MAXIMUM_TIMESTEP_SIZE 1.d-2 y
# END
#
# !!=========================== output options ===================================
# OUTPUT
#   TIMES y 8.333d-2 1.667d-1 2.500d-1 3.333d-1 4.167d-1 5.000d-1 5.833d-1 6.667d-1 7.500d-1 8.333d-1 9.167d-1 1.000d0
#   FORMAT VTK
#   MASS_BALANCE_FILE
#     PERIODIC TIME 8.33d-2 y
#     TOTAL_MASS_REGIONS
#       well
#       gas_res
#     /
#     !DETAILED
#   /
#   VARIABLES
#     LIQUID_PRESSURE
#     LIQUID_DENSITY
#     LIQUID_MOLE_FRACTIONS
#     LIQUID_SATURATION
#     GAS_PRESSURE
#     GAS_DENSITY
#     GAS_SATURATION
#     GAS_MOLE_FRACTIONS
#     MAXIMUM_PRESSURE
#     CAPILLARY_PRESSURE
#     POROSITY
#     PERMEABILITY_X
#     PERMEABILITY_Y
#     PERMEABILITY_Z
#   /
# PERIODIC_OBSERVATION TIMESTEP 1000
# END
#
# !!=========================== fluid properties =================================
# FLUID_PROPERTY
#   PHASE LIQUID
#   DIFFUSION_COEFFICIENT 5.5d-9
# END
#
# FLUID_PROPERTY
#   PHASE GAS
#   DIFFUSION_COEFFICIENT 1.0d-8  ![m2/s]
# END
#
# EOS WATER
#   DENSITY DEFAULT
#   VISCOSITY DEFAULT
# END
#
# EOS GAS
#   DENSITY RKS
#     HYDROGEN
#   /
#   VISCOSITY CONSTANT 1.025e-5
#   FORMULA_WEIGHT 2.016d0
#   HENRYS_CONSTANT DEFAULT
# END
#
# !!=========================== material properties ==============================
# MATERIAL_PROPERTY rock
#   ID 1
#   POROSITY 2.0d-1
#   ROCK_DENSITY 2.7d3
#   SATURATION_FUNCTION unsat
#   THERMAL_CONDUCTIVITY_DRY 2.5d0
#   THERMAL_CONDUCTIVITY_WET 2.2d0
#   HEAT_CAPACITY 820.d0
#   PERMEABILITY_MIN_SCALE_FACTOR 0.0d0
#   PERMEABILITY_POWER 3.0d0
#   PERMEABILITY
#     PERM_ISO 1.974e-13
#   /
# END
#
# MATERIAL_PROPERTY well_region
#   ID 2
#   POROSITY 0.21d0
#   !TORTUOSITY 1.0d0
#   !LONGITUDINAL_DISPERSIVITY 1.d-3   ![m] for [m2/s] calculation
#   !TRANSVERSE_DISPERSIVITY_H 1.d-4
#   !TRANSVERSE_DISPERSIVITY_V 1.d-4
#   ROCK_DENSITY 2.7d3
#   SATURATION_FUNCTION unsat
#   THERMAL_CONDUCTIVITY_DRY 2.5d0
#   THERMAL_CONDUCTIVITY_WET 2.2d0
#   HEAT_CAPACITY 820.d0
#   PERMEABILITY_MIN_SCALE_FACTOR 0.0d0
#   PERMEABILITY_POWER 3.0d0
#   PERMEABILITY
#     PERM_X 1.974e-13
#     PERM_Y 1.974e-13
#     PERM_Z 3.974e-13
#   /
# END
#
# !!=========================== characteristic curves ============================
# CHARACTERISTIC_CURVES unsat
#   SATURATION_FUNCTION VAN_GENUCHTEN
#     LOOP_INVARIANT
#     UNSATURATED_EXTENSION ECPC
#     ALPHA  1.d-4
#     M 0.5d0
#     LIQUID_RESIDUAL_SATURATION 1.d-1
#     MAX_CAPILLARY_PRESSURE 1.d7
#   /
#   PERMEABILITY_FUNCTION MUALEM_VG_LIQ
#     PHASE LIQUID
#     M 0.3d0
#     LIQUID_RESIDUAL_SATURATION 1.d-1
#     SMOOTH
#   /
#   PERMEABILITY_FUNCTION MUALEM_VG_GAS
#     PHASE GAS
#     M 0.3d0
#     LIQUID_RESIDUAL_SATURATION 1.d-1
#     GAS_RESIDUAL_SATURATION 1.d-2
#   /
# END
#
# !!=========================== regions ==========================================
# REGION all
#   COORDINATES
#     0.0d0 0.0d0 0.0d0
#     2.0d3 2.0d3 2.0d2
#   /
# END
#
# REGION well
#   BLOCK 63 63 63 63 5 10
# END
#
# REGION gas_res
#   BLOCK 1 125 1 125 1 10
# END
#
# !!======================== flow conditions =================
# FLOW_CONDITION initial
#   # UNITS Pa,C,M,yr
#   TYPE
#     LIQUID_PRESSURE HYDROSTATIC
#     LIQUID_SATURATION DIRICHLET
#     GAS_PRESSURE DIRICHLET
#     TEMPERATURE DIRICHLET
#   /
#   LIQUID_PRESSURE 1.D7
#   GAS_PRESSURE 1.D7
#   LIQUID_SATURATION {S_w}
#   TEMPERATURE {T}
#   GRADIENT
#     LIQUID_PRESSURE 0.d0 0.d0 10530d0
#     TEMPERATURE  0.d0 0.d0 2.5d-2
#   /
# END
#
# FLOW_CONDITION gas_injection
#   TYPE
#     RATE SCALED_MASS_RATE VOLUME
#   /
#   RATE LIST
#     TIME_UNITS year
#     DATA_UNITS kg/year kg/year MW
#     0.d0 {Liq_inj_rate} 7.5d8 0.d0
#     2.5d-1 0.d0 0.d0 0.d0
#   /
# END
#
# !!=========================== transport conditions =============================
# TRANSPORT_CONDITION initial
#   TYPE DIRICHLET_ZERO_GRADIENT
#   CONSTRAINT_LIST
#     0.d0 initial
#   /
# END
#
# TRANSPORT_CONDITION inlet
#   TYPE DIRICHLET_ZERO_GRADIENT
#   CONSTRAINT_LIST
#     0.d0 inlet
#   /
# END
#
# !!=========================== constraints ======================================
# CONSTRAINT initial
#    CONCENTRATIONS
#        Al+++        4.0d-6       M Kaolinite
#        Tracer       1d-5         T
#        Na+          6.05d-1      T
#        Cl-          6.05d-1      T
#        H+           8.8d0        P
#        CO2(aq)      6.3d-4       M Calcite
#        Fe+++        2.0d-13      M Goethite
#        Ca++         6.3d-4       T
#        H2(aq)       1.0d-8       T
#        SiO2(aq)     8.1d-4       M Quartz
#        Methane(aq)  1.0d-3       T
#        HS-          6.0d-6       M Pyrite
#    /
#    MINERALS
#       Pyrite                1.d-16  1.d-16 m^2/g
#       Quartz                0.8     1.d-16 m^2/g
#       Calcite               1.d-16  1.d-16 m^2/g
#       Kaolinite             1.d-16  1.d-16 m^2/g
#       Goethite              1.d-16  1.d-16 m^2/g
#       Anhydrite             1.d-16  1.d-16 m^2/g
#       Pyrrhotite            1.d-16  1.d-16 m^2/g
#    /
# END
#
# CONSTRAINT inlet
#    CONCENTRATIONS
#        Al+++        8.3d-8       M Kaolinite
#        Tracer       1d-5         T
#        Na+          5.49d-1      T
#        Cl-          5.49d-1      T
#        H+           7.3d0        P
#        CO2(aq)      3.8d-3       M Calcite
#        Fe+++        3.5d-20      T
#        Ca++         3.8d-3       T
#        H2(aq)       {H2_PP}          G H2(g)
#        SiO2(aq)     2.6d-4       M Quartz
#        Methane(aq)  1.0d-3       T
#        HS-          4.9d-3       M Pyrite
#    /
# END
#
# !!=========================== condition couplers ===============================
# # initial condition
# INITIAL_CONDITION gas_res
#   FLOW_CONDITION initial
#   TRANSPORT_CONDITION initial
#   REGION gas_res
# END
#
# # gas injection
# SOURCE_SINK well
#   FLOW_CONDITION gas_injection
#   TRANSPORT_CONDITION inlet
#   REGION well
# END
#
# !!=========================== stratigraphy couplers ============================
# STRATA
#   REGION all
#   MATERIAL rock
# END
#
# STRATA
#   REGION well
#   MATERIAL rock !well_region
# END
#
# END_SUBSURFACE
#
#
# """, file=fid_NR)
#
# Liq_inj_rate = 7.5e8/(0.2226*(Temp**2)-33.212*(Temp)+1292)
#
# # Adjust by Sw
# #GP30 = 1.33466                                                    # Sw=0.3, T=50C
# GP_ratio = 0.915/(-0.2542*(Sw**2)-0.0493*Sw+0.9462)
# # Adjust by T
# PP1 = (GP_ratio)*104
# H250 = 9.15E10  #9.06869105E+10                                              # Sw=0.3, T=50C
# H2 = 2.0692E8*(Temp-50)+H250
# H2_PartialP = PP1/((H2/H250))
#
# for i in range(n):
#     dir = './Pflo_Input/Goe/run_' + str(i+1)
#     if not os.path.exists(dir):
#         os.makedirs(dir)
#
#     name = f"pflotran_h2.in"
#     name_NR = f"pflotran_h2_NR.in"
#     path2file = os.path.join(dir, name)
#     path2file_NR = os.path.join(dir, name_NR)
#     fileID = open(path2file, 'w')
#     fileID_NR = open(path2file_NR, 'w')
#
#     write_from_base(Temp[i], Sw[i], Liq_inj_rate[i], H2_PartialP[i], Log_SA[i], Logk_Pyr[i], Logk_Goe[i], Qua_vol[i],
#                     Cal_vol[i], Pyr_vol[i], Goe_vol[i], Kao_vol[i], fid=fileID)
#
#     write_from_base_NR(Temp[i], Sw[i], Liq_inj_rate[i], H2_PartialP[i], fid_NR=fileID_NR)
#
#

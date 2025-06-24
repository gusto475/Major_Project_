
import streamlit as st
import plotly.graph_objects as go



import major_project_deco as mfd
import major_project_functions as mpf
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from math import pi, sqrt

from IPython.display import display, Math, Latex
import forallpeople as si
from handcalcs.decorator import handcalc
import handcalcs
si.environment('structural', top_level=True)
from math import pi, sqrt
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

si.environment("structural")
st.write("# Steel Beam Sizing App")    
st.subheader("Scope and Assumptions ")
st.write("Beams are assumed to be simply supported,and compression flanges continuously braced.")
st.write("The  sections used are from the [AISC Shapes Database (v15.0)](https://www.aisc.org/globalassets/aisc/manual/v15.0-shapes-database/aisc-shapes-database-v15.0.xlsx).")
st.write("Users of other national databases may select sizes based on similar section properties given in table 1: table" \
"of 10 closest possible sections")
st.write("Units are SI")
st.write("The app sizes steel beams based on live load deflection/ultimate moment of resistance for plastic" \
" sections")
st.write("The ultimate span moment and the required moment of inertia required under specified live loads is calculated. List of sections that exceed the computed values are"
          " estimated, tabulated and plotted." )

st.write("Based on user selection based on priority of limiting deflection or section weight, short calculations are provided for the section")
st.sidebar.subheader("Inputs")
phi = 0.9
omega_2 = 1.0
E=200e3
G=77e3



#Input data
l = st.sidebar.number_input("l(m)", value=2.5, step=0.1)
w= st.sidebar.number_input("Tributary Width(m)", value=2.5)
w_d= st.sidebar.number_input("Specified Dead Floor Load(kPa)", value=3)

w_l= st.sidebar.number_input("Specified Floor Imposed Load(kPa)", value=4.8)
limit= st.sidebar.selectbox("Limiting Deflection Factor", options=[180,240,300,360,480,700],index = 3)
f_y = st.sidebar.number_input("Material Yield Strength(MPa)", value=345)

st.subheader("Calculation of Ultimate Moment and Moment of Inertia Required unlive specified live loads ")

check_latex_2,check_2_values = mfd.i_req(l*si.m,w*si.m,w_d*si.kPa,w_l*si.kPa,limit)

st.latex(check_latex_2)


I_req_=check_2_values["I_req"].value*1e12

Delta_p=check_2_values["Delta_p"]
l=check_2_values["l"]
m_f = check_2_values['m_f']

data = mpf.sdb.aisc_w_sections()

section_tables = mpf.possible_sections_g(data,I_req_,Delta_p,l,m_f,f_y*si.MPa)
st.markdown("Table of 10 closest possible sections")
section_tables[1]

st.latex(r"\text{Plots of closest Possible Sections}")
plots = mpf.plot_of_sections_g(limit,section_tables[0])
st.plotly_chart(plots[0])
st.plotly_chart(plots[1])

list_of_sections = section_tables[0].index

selected_section = st.selectbox("Selected Section: ",list_of_sections)
st.write("Selected Section:",selected_section)
test_chosen = mpf.selected_section_props_g(section_tables[0],selected_section)

st.latex(r"\text{Actual Deflection}")
selected_section_series = section_tables[0].loc[selected_section]


I_prov = selected_section_series["Ix"]*si.mm**4
M_r = selected_section_series["m_p"]



check_latex_3,check_3_values = mfd.i_req_1(I_prov,w_l*si.kPa,w*m,l,E*si.MPa)
st.latex(check_latex_3)
l_def = (l.value*1000)


check_def = mpf.lim_d(l.value*1000,check_3_values.value*1000)
st.latex(r"\text{or }" + check_def)
output = f"{test_chosen.tag} is satifactory for deflection"



st.latex(r"\text{Moment Capacity Check}")

check_latex_4,check_4_values = mfd.m_r(test_chosen.z_x,f_y*si.MPa,m_f)
st.latex(check_latex_4)
st.latex(r"\text{Summary}")
limit_cal = int(check_def.split("/")[-1])
mpf.mr_g_summary(check_4_values["dcr"],test_chosen.tag,limit,limit_cal)

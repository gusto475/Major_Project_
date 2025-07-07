import forallpeople as si

si.environment('structural', top_level=True)

from handcalcs.decorator import handcalc
from dataclasses import dataclass
from math import sqrt, ceil
from IPython.display import Markdown as md
import numpy as np
# from eng_module_2.general import general_calcs as gc
# from eng_module_2.sections import sections_db as sdb
from math import pi, sqrt
si.environment('structural')
from IPython.display import display, Math, Latex
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st

aisc_csv =  "aisc_w_si.csv"
def aisc_w_sections(csv:str) ->pd.DataFrame:
    """
    Returns the DataFrame of aisc_w_si.csv file
    """
    df = pd.read_csv(csv) 
    df[["Ix","Iy"]] = df[["Ix","Iy"]]*1e6
    df[["Sx","Sy","Zx", "Zy","J"]] = df[["Sx","Sy","Zx", "Zy","J"]]*1e3
    df["Cw"] = df["Cw"]*1e9
    df = df.set_index('AISC_Manual_Label')
    return df
### Constants and databases and general functions
data = aisc_w_sections(aisc_csv)


f_y = 345*si.MPa
E=200e3*si.MPa
G=77e3*si.MPa
phi = 0.9
omega_2 = 1.0
mm = 0.001*si.m

def m_r(Zx_prov,f_y,m_f,phi=0.9):
    """
    This calculates the bending moment of resistance of compact or plastic sections
    """
    
    Zx_prov 
    f_y #yield strength of material
    phi #material factor
    Mr_p = phi*f_y*Zx_prov
    dcr = m_f/Mr_p
   
    return locals()
def actual_deflection(I_prov,Delta_p,I_req):
    """
    
    """
    return
###
#
##############
#These functions are for US metric 
def i_req_g(l: float,w: float, w_d: float,w_l: float,span_d:int,):
    
    """
    This function computes:
    Distrubuted load on beam from floor load and tributary width for ultimate and live load cases
    Factored Span moment
    limiting deflection value
    Required moment of inertia to satisfy live load deflection
    """
    span_d  #deflection limit
    l #span length
    
    w  #trib width
    w_f = 1.2*w_d+1.6*w_l #factored floor load
    w_bl = w_f*w #factored beam udl
    
    Delta_p = l/span_d #limiting deflection
    m_f  = w_bl*l**2/8#factored beam moment
    w_l # specified factored floor load
    wb_ll = w_l*w #specified beam udl
    
    I_req= (w_l*w*5*l**4*span_d)/(384*E*l)
    
    
    return locals()    

def i_req_g_1(l: float,w: float, w_d: float,w_l: float,span_d:int,
              P,n):
    
    """
    This function computes:
    Distrubuted load on beam from floor load and tributary width for ultimate and live load cases
    Factored Span moment
    limiting deflection value
    Required moment of inertia to satisfy live load deflection
    """
    span_d  #deflection limit
    l #span length
    
    w  #trib width
    w_f = 1.2*w_d+1.6*w_l #factored floor load
    w_bl = w_f*w #factored beam udl
    
    Delta_p = l/span_d #limiting deflection
    if n%2==0:

        m_f  = w_bl*l**2/8+n*P*l/8
    else:
        m_f  = w_bl*l**2/8+(n**2-1)*P*l/8*n#factored beam moment
    w_l # specified factored floor load
    wb_ll = w_l*w #specified beam udl
    
    I_req= (w_l*w*5*l**4*span_d)/(384*E*l)
    
    
    return locals()   

def i_req_g_even(l: float,w: float, w_d: float,w_l: float,span_d:int,P_d:float,P_l:float,n:int):
    
    """
    This function computes:
    Distrubuted load on beam from floor load and tributary width for ultimate and live load cases
    Factored Span moment
    limiting deflection value
    Required moment of inertia to satisfy live load deflection
    """
    span_d  #deflection limit
    l #span length
    
    w  #trib width
    w_f = 1.2*w_d+1.6*w_l #factored floor load
    P_f =1.2*P_d+1.6*P_l #factored floor load
    w_bl = w_f*w #factored beam udl
    
    Delta_p = l/span_d #limiting deflection


    m_f  = w_bl*l**2/8+n*P_f*l/8
   
    w_l # specified factored floor load
    wb_ll = w_l*w #specified beam udl
    
    I_req= ((w_l*w*5*l**4*span_d)/(384*E*l))+((P_l*l**3)/(192*E))
    
    
    return locals()   

# @handcalc(jupyter_display=True)
def possible_sections_g(data: pd.DataFrame,I_req_:float,Delta_p: float,
                        L:float,m_f:float, f_y: float, phi = 0.9,):
    """
    This fuction does the following:
    for the section database, sorts a value of I_x greated than Irequired
    calculates the limiting deflection value
    calculates the buckling resistant moment
    and secarches for sections with DCR <=1.2 and returns a dataframe with necessary information
    for further processing
    """
    new_daf = data.sort_values("Ix")
    mask = (new_daf["Ix"]>I_req_)
    new_daf = new_daf.loc[mask]
    new_daf['def'] = Delta_p.value*1000*I_req_/new_daf['Ix']
    new_daf['limit_d'] = (L.value*1000/new_daf['def']).round(0).astype(int)
    new_daf["sect+L/"] = new_daf.index + " L/" + new_daf["limit_d"].astype(str)
    new_daf["L/"] = " L/" + new_daf["limit_d"].astype(str)
    new_daf["m_f"] = round(m_f.value/1000,2)
    new_daf["m_p"] = ((new_daf["Zx"] * mm**3) * f_y * phi).apply(lambda x: round(x.value, 2))/1000
    new_daf['DCR'] = ((new_daf["m_f"])/new_daf["m_p"]).round(2)
    new_daf["sect+DCR"] = new_daf.index +" " + new_daf["DCR"].map("{:.2f}".format)
    mask_2 = (new_daf["DCR"]<1.5)
    new_daf = new_daf.loc[mask_2]
    new_daf = new_daf.head(15)
    new_daf_view = new_daf.drop(columns=[ 'bf/2tf', 'h/tw',"sect+L/","sect+DCR",
         'Sx', 'rx', 'Iy', 'Zy', 'Sy', 'ry', 'J', 'Cw','limit_d'])
    return [new_daf,new_daf_view]
    
def plot_of_sections_g(limit: int, possible_sections: pd.DataFrame):
    """
    This function plots the limiting deflection ratios vs weight and DCR vs weight for possible sections based on
    the dataframe of possible sections
    the limit variable is the limiting deflection ratio
    """
    fig = px.scatter(possible_sections, x="W", y="limit_d", text="sect+L/", title="Limiting Deflection vs.Weight")
    fig.update_traces(textposition="top center")  
    fig.update_layout(xaxis_title="W (Weight per unit length)", yaxis_title="Limiting Deflection ")
    fig.add_hline(y=limit,  line_color="red", 
                annotation_text=f"Limiting L/: L/{limit}", 
                annotation_position="bottom right")
    fig2 = px.scatter(possible_sections, x="W", y="DCR", text = "sect+DCR",title="DCR vs Weight")
    fig2.update_traces(textposition="top center")  
    fig2.update_layout(
        xaxis_title="W (Weight per unit length)",
        yaxis_title="M_f/M_r",
    )
    return [fig,fig2]
@dataclass
class chosen_sections:
    """
    A dataclass for section properties in bending where
    z_x is plastic section modulus about major axis
    i_x is moment of inertia about major axis
    tag is name of the section
    """
    z_x : float
    i_x: float
    
    tag: str
## examples
selected_section1 =  chosen_sections(1*mm**3,1*mm**4,'w')   


def selected_section_props_g(possible_sections: pd.DataFrame, section: str):
    """
    Assigns relevant section properties from a dataframe to chosen_sections
    """
    selected_section_dc = chosen_sections(z_x = possible_sections.loc[section,'Zx']*mm**3,
                             i_x = possible_sections.loc[section,'Ix']*mm**4,
                            
                            tag = section)
    return selected_section_dc
def actual_def_g(I_prov,w_l,w,l,E):
    Delta = (w_l*w*5*l**4)/(384*E*I_prov)
    return Delta
def lim_d(l,Delta):
    lim_d_ = f'L/{int(round(l/Delta,0))}'
    return lim_d_
def mrc_g(Mr,m_f):
    """
    Carries out the DCR ratio check for factored moment to moment of resistance
    """
    
    dcr =m_f/Mr
    
    display(Math(r"""
    \begin{aligned}
    \text{DCR} &= \frac{M_f}{M_r} \\
           &= \frac{%s}{%s} \\
           &= %.2f
    \end{aligned}
    """ % (m_f, Mr, dcr)))
    
    return 

def mr_g_summary(dcr, section,limit,limit_cal):
    limit_str = f"L/{limit}"
    limit_cal_str = f"L/{limit_cal}"
    if dcr<1 and limit_cal>limit :
       st.latex(
    rf"\quad \text{{DCR}} = {round(dcr, 2)} < 1, \quad \text{{{limit_cal_str} < {limit_str}, {section} OK}}"
)



    else:
         st.latex(
    rf"\quad \text{{DCR}} = {round(dcr, 2)} > 1, \quad \text{{{limit_cal_str} < {limit_str}, {section} not OK, redesign}}")




##########





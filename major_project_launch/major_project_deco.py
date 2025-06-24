

from major_project import major_project_functions as mpf


import handcalcs
import forallpeople 
from handcalcs.decorator import handcalc

import forallpeople as si
si.environment("structural", top_level=True)

calc_renderer = handcalc()
# decorator for various functions
i_req_1= calc_renderer(mpf.actual_def_g)
i_req = calc_renderer(mpf.i_req_g)
i_req_even = calc_renderer(mpf.i_req_g_even)

m_r = calc_renderer(mpf.m_r)
# m_u = calc_renderer(mpf.m_u)
mrc = calc_renderer(mpf.mrc_g)











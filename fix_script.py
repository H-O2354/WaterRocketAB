import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

start_str = "<!-- ARCHITECTURE MODAL -->"
end_str = "<!-- SCRIPT SECTION -->"

start_idx = html.find(start_str)
end_idx = html.find(end_str)

arch_modal_html = html[start_idx:end_idx]

replacements = {
    r'<span class="tree-math">\( x, y, v_x, v_y, m_w, P \)</span>': r'x, y, vx, vy, m_w, P',
    r'<span class="tree-math">\( C_d, A_c, A_e, \rho_w, \rho_{air}, P_{atm}, g, V_0 \dots \)</span>': r'C_d, A_c, A_e, rho_w, rho_air, P_atm, g, V_0...',
    r'<span class="tree-math">\( v_{mag} = \sqrt{v_x^2 + v_y^2} \)</span>': r'v_mag = sqrt(vx^2 + vy^2)',
    r'<span class="tree-math">\( \cos(\theta) = \frac{v_x}{v_{mag}}, \sin(\theta) = \frac{v_y}{v_{mag}} \)</span>': r'cos(th) = vx/v_mag, sin(th) = vy/v_mag',
    r'<span class="tree-math">\( sm = \frac{CoP - CoM}{d_{body}} \)</span>': r'sm = (CoP - CoM)/d_body',
    r'<span class="tree-math">\( C_{d,eff} = C_d \cdot WOBBLE\_FACTOR \)</span>': r'C_d,eff = C_d * WOBBLE_FACTOR',
    r'<span class="tree-math">\( F_d = \frac{1}{2} \rho_{air} C_{d,eff} A_c v_{mag}^2 \)</span>': r'F_d = 0.5 * rho_air * C_d,eff * A_c * v_mag^2',
    r'<span class="tree-math">\( a_{longitudinal} = a_{prev,x}\cos(\theta) + (a_{prev,y}+g)\sin(\theta) \)</span>': r'a_longitudinal = a_prev,x * cos(th) + (a_prev,y + g) * sin(th)',
    r'<span class="tree-math">\( dV_{elastic} = V_0 (P - P_{atm}) \frac{D}{2 E t_{wall}} \)</span>': r'dV_elastic = V_0 * (P - P_atm) * (D / (2 * E * t_wall))',
    r'\( m_w > 0 \)': r'm_w > 0',
    r'<span class="tree-math">\( F_{friction} = P_{contact} \cdot A_{contact} \cdot \mu \)</span>': r'F_friction = P_contact * A_contact * mu',
    r'<span class="tree-math">\( Thrust = (P - P_{atm})A_{tube} - F_{friction} \)</span>': r'Thrust = (P - P_atm) * A_tube - F_friction',
    r'<span class="tree-math">\( \frac{dP}{dt} = - \frac{\gamma P}{V_{gas}} A_{tube} v_{mag} \)</span>': r'dP/dt = -(gamma * P / V_gas) * A_tube * v_mag',
    r'<span class="tree-math">\( P_{bottom} = (P - P_{atm}) + \rho_w a_{longitudinal} h_{water} \)</span>': r'P_bottom = (P - P_atm) + rho_w * a_longitudinal * h_water',
    r'<span class="tree-math">\( v_e = \sqrt{\frac{2 P_{bottom}}{\rho_w}} \)</span>': r'v_e = sqrt(2 * P_bottom / rho_w)',
    r'<span class="tree-math">\( \frac{dm_w}{dt} = -C_{d,nozzle} A_e \rho_w v_e \)</span>': r'dm_w/dt = -C_d,nozzle * A_e * rho_w * v_e',
    r'<span class="tree-math">\( Thrust = \left|\frac{dm_w}{dt}\right| v_e \)</span>': r'Thrust = |dm_w/dt| * v_e',
    r'<span class="tree-math">\( V_{gas} = V_0 + dV_{elastic} - \frac{m_w}{\rho_w} \)</span>': r'V_gas = V_0 + dV_elastic - (m_w / rho_w)',
    r'<span class="tree-math">\( T_{chamber} = \frac{P \cdot V_{gas}}{m_{air} \cdot R} \)</span>': r'T_chamber = (P * V_gas) / (m_air * R)',
    r'<span class="tree-math">\( \frac{dQ}{dt} = h_{conv} A_{surf} (T_{atm} - T_{chamber}) \)</span>': r'dQ/dt = h_conv * A_surf * (T_atm - T_chamber)',
    r'<span class="tree-math">\( \frac{dP}{dt} = \frac{\gamma - 1}{V_{gas}} \frac{dQ}{dt} - \frac{\gamma P}{V_{gas}} \frac{dV_{gas}}{dt} \)</span>': r'dP/dt = ((gamma - 1) / V_gas) * dQ/dt - (gamma * P / V_gas) * dV_gas/dt',
    r'\( P > P_{atm} \cdot 1.01 \)': r'P > P_atm * 1.01',
    r'<span class="tree-math">\( \frac{dP}{dt} = f(m_{citric}, m_{baking\_soda}) - \text{tốc độ phản ứng} \)</span>': r'dP/dt = f(m_citric, m_baking_soda)',
    r'\( p_{ratio} < 0.455 \)': r'p_ratio < 0.455',
    r'<span class="tree-math">\( v_{gas} = \sqrt{\gamma R T_{chamber}} \)</span>': r'v_gas = sqrt(gamma * R * T_chamber)',
    r'<span class="tree-math">\( \frac{dm_{air}}{dt} = -C_d A_e P \sqrt{\frac{\gamma}{R T_{chamber}}} \left(\frac{2}{\gamma+1}\right)^{\frac{\gamma+1}{2(\gamma-1)}} \)</span>': r'dm_air/dt = -C_d * A_e * P * sqrt(gamma / (R * T_chamber)) * (2/(gamma+1))^((gamma+1)/(2*(gamma-1)))',
    r'<span class="tree-math">\( Thrust = \left|\frac{dm_{air}}{dt}\right| v_{gas} + (P_{exit} - P_{atm}) A_e \)</span>': r'Thrust = |dm_air/dt| * v_gas + (P_exit - P_atm) * A_e',
    r'<span class="tree-math">\( Mach = \sqrt{\frac{2}{\gamma - 1} \left( \left(\frac{P}{P_{atm}}\right)^{\frac{\gamma - 1}{\gamma}} - 1 \right)} \)</span>': r'Mach = sqrt((2 / (gamma - 1)) * ((P / P_atm)^((gamma - 1) / gamma) - 1))',
    r'<span class="tree-math">\( v_{gas} = Mach \sqrt{\gamma R T_{exit}} \)</span>': r'v_gas = Mach * sqrt(gamma * R * T_exit)',
    r'<span class="tree-math">\( Thrust = \left|\frac{dm_{air}}{dt}\right| v_{gas} \)</span>': r'Thrust = |dm_air/dt| * v_gas',
    r'<span class="tree-math">\( \frac{dP}{dt} = \frac{\gamma R T_{chamber}}{V_{gas}} \frac{dm_{air}}{dt} + \frac{\gamma - 1}{V_{gas}} \frac{dQ}{dt} \)</span>': r'dP/dt = (gamma * R * T_chamber / V_gas) * dm_air/dt + ((gamma - 1) / V_gas) * dQ/dt',
    r'<span class="tree-math">\( m_{total} = m_{empty} + m_w + m_{air} \)</span>': r'm_total = m_empty + m_w + m_air',
    r'\( dist < L_{tube} \)': r'dist < L_tube',
    r'<span class="tree-math">\( a_{net} = \frac{Thrust - F_d}{m_{total}} - g \sin(\theta_0) \)</span>': r'a_net = (Thrust - F_d) / m_total - g * sin(th_0)',
    r'<span class="tree-math">\( a_x = a_{net} \cos(\theta_0), a_y = a_{net} \sin(\theta_0) \)</span>': r'a_x = a_net * cos(th_0), a_y = a_net * sin(th_0)',
    r'<span class="tree-math">\( a_x = \frac{Thrust \cos(\theta) - F_d \cos(\theta)}{m_{total}} \)</span>': r'a_x = (Thrust * cos(th) - F_d * cos(th)) / m_total',
    r'<span class="tree-math">\( a_y = \frac{Thrust \sin(\theta) - F_d \sin(\theta)}{m_{total}} - g \)</span>': r'a_y = (Thrust * sin(th) - F_d * sin(th)) / m_total - g',
    r'<span class="tree-math">\( [v_x, v_y, a_x, a_y, \frac{dm_w}{dt}, \frac{dP}{dt}] \)</span>': r'[vx, vy, ax, ay, dm_w/dt, dP/dt]'
}

for latex, text in replacements.items():
    arch_modal_html = arch_modal_html.replace(latex, text)

html = html[:start_idx] + arch_modal_html + html[end_idx:]

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

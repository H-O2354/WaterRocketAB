import re

with open('/app/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# We need to fix the objectiveFunction to not write to DOM on every single candidate evaluation!
# Currently:
# function objectiveFunction(normalizedValues) {
#   for (...) { document.getElementById(unlocked[i].id).value = realVal; }
#   let simInput = { in_mode: document.getElementById('in-mode').value, ... }
#   const result = run_simulation(simInput);
# }
#
# That is terrible for performance! We should pre-parse the base inputs ONCE,
# then clone it and override only the unlocked inputs for each evaluation.

start_idx = content.find("function objectiveFunction(normalizedValues) {")
if start_idx != -1:
    end_idx = content.find("function cmaesLoop() {")
    if end_idx != -1:
        old_obj = content[start_idx:end_idx]

        # Look above objectiveFunction to define the base object
        # We can just put it right before objectiveFunction

        base_sim_def = """
    // --- PERFORMANCE FIX: PRE-PARSE DOM ONCE ---
    const baseSimInput = {
        in_mode: document.getElementById('in-mode').value,
        in_v_bottle: parseFloat(document.getElementById('in-v-bottle').value),
        in_l_rocket: parseFloat(document.getElementById('in-l-rocket').value),
        in_fin_root: parseFloat(document.getElementById('in-fin-root').value),
        in_fin_tip: parseFloat(document.getElementById('in-fin-tip').value),
        in_fin_span: parseFloat(document.getElementById('in-fin-span').value),
        in_d_body: parseFloat(document.getElementById('in-d-body').value),
        in_m_empty: parseFloat(document.getElementById('in-m-empty').value),
        in_m_ballast: parseFloat(document.getElementById('in-m-ballast').value),
        in_water_ratio: parseFloat(document.getElementById('in-water-ratio').value),
        in_pressure: parseFloat(document.getElementById('in-pressure').value),
        in_burst: parseFloat(document.getElementById('in-burst').value),
        in_salt_type: document.getElementById('in-salt-type').value,
        in_mass_salt: parseFloat(document.getElementById('in-mass-salt').value),
        in_vol_vinegar: parseFloat(document.getElementById('in-vol-vinegar').value),
        in_acid_conc: parseFloat(document.getElementById('in-acid-conc').value),
        in_gas_eff: parseFloat(document.getElementById('in-gas-eff').value),
        in_popoff: parseFloat(document.getElementById('in-popoff').value),
        in_d_nozzle: parseFloat(document.getElementById('in-d-nozzle').value),
        in_l_tube: parseFloat(document.getElementById('in-l-tube').value),
        in_d_tube: parseFloat(document.getElementById('in-d-tube').value),
        in_angle: parseFloat(document.getElementById('in-angle').value),
        in_cd: parseFloat(document.getElementById('in-cd').value),
        in_temp: parseFloat(document.getElementById('in-temp').value),
        in_env: parseFloat(document.getElementById('in-env').value)
    };

    // Map of id to property name in simInput
    const idToProp = {
        'in-v-bottle': 'in_v_bottle',
        'in-l-rocket': 'in_l_rocket',
        'in-fin-root': 'in_fin_root',
        'in-fin-tip': 'in_fin_tip',
        'in-fin-span': 'in_fin_span',
        'in-d-body': 'in_d_body',
        'in-m-empty': 'in_m_empty',
        'in-m-ballast': 'in_m_ballast',
        'in-water-ratio': 'in_water_ratio',
        'in-pressure': 'in_pressure',
        'in-burst': 'in_burst',
        'in-salt-type': 'in_salt_type',
        'in-mass-salt': 'in_mass_salt',
        'in-vol-vinegar': 'in_vol_vinegar',
        'in-acid-conc': 'in_acid_conc',
        'in-gas-eff': 'in_gas_eff',
        'in-popoff': 'in_popoff',
        'in-d-nozzle': 'in_d_nozzle',
        'in-l-tube': 'in_l_tube',
        'in-d-tube': 'in_d_tube',
        'in-angle': 'in_angle',
        'in-cd': 'in_cd',
        'in-temp': 'in_temp',
        'in-env': 'in_env'
    };
"""
        new_obj = base_sim_def + """
    // Objective function wraps the physics sim WITHOUT touching the DOM
    function objectiveFunction(normalizedValues) {
        let penalty = 0;
        let evalInput = { ...baseSimInput }; // Clone

        // Restore values and check bounds
        for (let i = 0; i < dim; i++) {
            let nVal = normalizedValues[i];
            if (nVal < 0) { penalty += 1000 * Math.pow(-nVal, 2); nVal = 0; }
            if (nVal > 1) { penalty += 1000 * Math.pow(nVal - 1, 2); nVal = 1; }

            const realVal = unlocked[i].min + nVal * (unlocked[i].max - unlocked[i].min);
            const propName = idToProp[unlocked[i].id];
            if (propName) {
                evalInput[propName] = realVal;
            }
        }

        // Run simulation
        const result = run_simulation(evalInput);

        let range = result.val_range || 0;
        if (result.isError) penalty += 1000;

        // We want to maximize range, CMA-ES minimizes. Return -range + penalty
        return -range + penalty;
    }

"""
        content = content[:start_idx] + new_obj + content[end_idx:]

with open('/app/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

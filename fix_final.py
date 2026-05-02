import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. FIX INPUT LIMITS
inputs_dict = {
    "in-v-bottle": {"min": "0.1", "max": "100.0"},
    "in-l-rocket": {"min": "10", "max": "5000"},
    "in-d-body": {"min": "20", "max": "500"},
    "in-m-empty": {"min": "0.01", "max": "20.0"},
    "in-m-ballast": {"min": "0", "max": "10.0"},
    "in-fin-root": {"min": "5", "max": "500"},
    "in-fin-tip": {"min": "5", "max": "500"},
    "in-fin-span": {"min": "5", "max": "500"},
    "in-water-ratio": {"min": "0", "max": "99"},
    "in-pressure": {"min": "10", "max": "500"},
    "in-burst": {"min": "30", "max": "1000"},
    "in-mass-salt": {"min": "1", "max": "1000"},
    "in-vol-vinegar": {"min": "10", "max": "5000"},
    "in-acid-conc": {"min": "1", "max": "100"},
    "in-gas-eff": {"min": "10", "max": "100"},
    "in-popoff": {"min": "10", "max": "500"},
    "in-d-nozzle": {"min": "5", "max": "200"},
    "in-l-tube": {"min": "0", "max": "10.0"},
    "in-d-tube": {"min": "5", "max": "200"},
    "in-angle": {"min": "0", "max": "90"},
    "in-cd": {"min": "0.01", "max": "5.0"},
    "in-temp": {"min": "-50", "max": "100"}
}

for inp_id, bounds in inputs_dict.items():
    pattern = r'(<input[^>]*id="' + inp_id + r'"[^>]*>)'
    def repl_func(match):
        tag = match.group(1)
        if 'min="' in tag:
            tag = re.sub(r'min="[^"]*"', f'min="{bounds["min"]}"', tag)
        else:
            tag = tag.replace('id=', f'min="{bounds["min"]}" id=')
        if 'max="' in tag:
            tag = re.sub(r'max="[^"]*"', f'max="{bounds["max"]}"', tag)
        else:
            tag = tag.replace('id=', f'max="{bounds["max"]}" id=')
        return tag
    html = re.sub(pattern, repl_func, html)

# 2. REMOVE LATEX
start_str = "<!-- ARCHITECTURE MODAL -->"
start_idx = html.find(start_str)

if start_idx != -1:
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
        html = html.replace(latex, text)


# 3. RE-IMPLEMENT WASM CMA-ES WITH FULL COV & DOM THRASHING FIX

import_str = """
<script src="test_ui.js"></script>
<script type="module">
    import init, { WasmCmaes } from './pkg/cmaes_wasm.js';

    window.wasmInitDone = false;
    window.WasmCmaes = WasmCmaes;

    async function initWasm() {
        await init();
        window.wasmInitDone = true;
    }

    window.ensureWasmInitialized = async function() {
        if (!window.wasmInitDone) {
            await initWasm();
        }
    };

    initWasm();
</script>
<script>
"""

html = html.replace("<script>", import_str, 1)


opt_search = """function optimizeRange() {
    console.log("Optimizer Triggered");

    // Find all unlocked inputs
    const inputs = document.querySelectorAll('#controls input[type="number"]');
    const unlockedInputs = [];
    inputs.forEach(input => {
        const btn = input.nextElementSibling;
        if (btn && btn.classList.contains('unlocked')) {
            unlockedInputs.push(input);
        }
    });

    if (unlockedInputs.length === 0) {
        alert("Vui lòng mở khóa (MỞ) ít nhất một thông số để tối ưu hóa.");
        return;
    }

    alert("Đang chạy thuật toán tối ưu hóa...");

    // Simple random search since full CMA-ES in JS is complex and might freeze UI
    // We will do 500 iterations of random mutations around current values
    let bestRange = -1;
    let bestParams = {};

    // Save original state
    const originalParams = {};
    unlockedInputs.forEach(input => {
        originalParams[input.id] = parseFloat(input.value);
        bestParams[input.id] = parseFloat(input.value);
    });

    // Run baseline
    const baselineResult = run_simulation();
    if (!baselineResult.isError) {
        bestRange = baselineResult.range;
    }

    const iterations = 500;
    for (let i = 0; i < iterations; i++) {
        // Mutate unlocked parameters
        unlockedInputs.forEach(input => {
            const currentVal = originalParams[input.id];
            // Random mutation +/- 20%
            const mutation = currentVal * 0.2 * (Math.random() * 2 - 1);
            let newVal = currentVal + mutation;

            // Constrain
            if (newVal < 0) newVal = 0.001;

            input.value = newVal.toFixed(3);
        });

        // Test new params
        const result = run_simulation();
        if (!result.isError && result.range > bestRange) {
            bestRange = result.range;
            unlockedInputs.forEach(input => {
                bestParams[input.id] = parseFloat(input.value);
            });
        }
    }

    // Apply best params
    unlockedInputs.forEach(input => {
        input.value = bestParams[input.id].toFixed(3);
    });

    // Final run to update UI
    runSimUI();
    alert(`Tối ưu hóa hoàn tất. Tầm xa lớn nhất tìm thấy: ${bestRange.toFixed(2)} m`);
}"""

opt_replace = """let isOptimizing = false;
let optimizationTimeout = null;

async function optimizeRange() {
    if (isOptimizing) {
        isOptimizing = false;
        clearTimeout(optimizationTimeout);
        document.querySelector('button[onclick="optimizeRange()"]').innerHTML = 'CHẠY TỐI ƯU HÓA CMA-ES';
        document.querySelector('button[onclick="optimizeRange()"]').classList.remove('running');
        setStatus("TỐI ƯU HÓA ĐÃ BỊ HỦY", false);
        return;
    }

    await ensureWasmInitialized();
    if (!wasmInitDone) return;

    let unlocked = [];
    document.querySelectorAll('.opt-lock').forEach(btn => {
        if (btn.innerText === 'MỞ' || btn.innerText === '🔓') {
            const inputEl = btn.previousElementSibling;
            const inputId = inputEl.id;
            if (!inputEl.disabled) {
                unlocked.push({
                    id: inputId,
                    min: (inputEl.min !== '') ? parseFloat(inputEl.min) : 0,
                    max: (inputEl.max !== '') ? parseFloat(inputEl.max) : 100,
                    current: parseFloat(inputEl.value)
                });
            }
        }
    });

    if (unlocked.length === 0) {
        setStatus("LỖI TỐI ƯU HÓA: CẦN MỞ KHÓA ÍT NHẤT 1 BIẾN", true);
        return;
    }

    isOptimizing = true;
    document.querySelector('button[onclick="optimizeRange()"]').innerHTML = '⏹ DỪNG TỐI ƯU';
    document.querySelector('button[onclick="optimizeRange()"]').classList.add('running');
    setStatus("ĐANG CHẠY CMA-ES...", false);

    const dim = unlocked.length;
    const initialGuess = new Float64Array(dim);

    for (let i = 0; i < dim; i++) {
        let normalized = (unlocked[i].current - unlocked[i].min) / (unlocked[i].max - unlocked[i].min);
        normalized = Math.max(0.01, Math.min(0.99, normalized));
        initialGuess[i] = normalized;
    }

    const sigma = 0.2;
    const maxIterations = 200;

    let es;
    try {
        es = new WasmCmaes(initialGuess, sigma, { max_iterations: maxIterations, cov_model: 'full' });
    } catch (e) {
        console.error("Failed to init CMA-ES:", e);
        setStatus("LỖI KHỞI TẠO CMA-ES", true);
        isOptimizing = false;
        document.querySelector('button[onclick="optimizeRange()"]').innerHTML = 'CHẠY TỐI ƯU HÓA CMA-ES';
        document.querySelector('button[onclick="optimizeRange()"]').classList.remove('running');
        return;
    }

    const popsize = es.population_size();
    let currentIter = 0;

    // Cache base inputs to avoid DOM reading in loop
    window.baseSimInput = {
        "in-v-bottle": parseFloat(document.getElementById("in-v-bottle").value) || 0,
        "in-l-rocket": parseFloat(document.getElementById("in-l-rocket").value) || 0,
        "in-d-body": parseFloat(document.getElementById("in-d-body").value) || 0,
        "in-m-empty": parseFloat(document.getElementById("in-m-empty").value) || 0,
        "in-m-ballast": parseFloat(document.getElementById("in-m-ballast").value) || 0,
        "in-fin-root": parseFloat(document.getElementById("in-fin-root").value) || 0,
        "in-fin-tip": parseFloat(document.getElementById("in-fin-tip").value) || 0,
        "in-fin-span": parseFloat(document.getElementById("in-fin-span").value) || 0,
        "in-water-ratio": parseFloat(document.getElementById("in-water-ratio").value) || 0,
        "in-pressure": parseFloat(document.getElementById("in-pressure").value) || 0,
        "in-burst": parseFloat(document.getElementById("in-burst").value) || 0,
        "in-mass-salt": parseFloat(document.getElementById("in-mass-salt").value) || 0,
        "in-vol-vinegar": parseFloat(document.getElementById("in-vol-vinegar").value) || 0,
        "in-acid-conc": parseFloat(document.getElementById("in-acid-conc").value) || 0,
        "in-gas-eff": parseFloat(document.getElementById("in-gas-eff").value) || 0,
        "in-popoff": parseFloat(document.getElementById("in-popoff").value) || 0,
        "in-d-nozzle": parseFloat(document.getElementById("in-d-nozzle").value) || 0,
        "in-l-tube": parseFloat(document.getElementById("in-l-tube").value) || 0,
        "in-d-tube": parseFloat(document.getElementById("in-d-tube").value) || 0,
        "in-angle": parseFloat(document.getElementById("in-angle").value) || 0,
        "in-cd": parseFloat(document.getElementById("in-cd").value) || 0,
        "in-temp": parseFloat(document.getElementById("in-temp").value) || 0
    };

    function optimizationStep() {
        if (!isOptimizing || es.should_stop() || currentIter >= maxIterations) {
            isOptimizing = false;
            document.querySelector('button[onclick="optimizeRange()"]').innerHTML = 'CHẠY TỐI ƯU HÓA CMA-ES';
            document.querySelector('button[onclick="optimizeRange()"]').classList.remove('running');

            const bestResult = es.result();
            const bestCandidate = bestResult.best_x();

            for (let i = 0; i < dim; i++) {
                let realVal = unlocked[i].min + bestCandidate[i] * (unlocked[i].max - unlocked[i].min);
                document.getElementById(unlocked[i].id).value = realVal;
            }

            runSimUI();
            setStatus("ĐÃ TÌM THẤY TẦM XA TỐI ƯU BẰNG CMA-ES", false);
            return;
        }

        const pop = [];
        for (let i = 0; i < popsize; i++) {
            pop.push(es.ask());
        }

        const fitness = new Float64Array(popsize);
        for (let c = 0; c < popsize; c++) {
            const candidate = pop[c];

            // Constrain
            for (let i = 0; i < dim; i++) {
                if (candidate[i] < 0) candidate[i] = 0;
                if (candidate[i] > 1) candidate[i] = 1;
            }

            let candidateReal = new Float64Array(dim);
            for (let i = 0; i < dim; i++) {
                candidateReal[i] = unlocked[i].min + candidate[i] * (unlocked[i].max - unlocked[i].min);
            }

            fitness[c] = objectiveFunction(unlocked, candidateReal);
        }

        try {
            for (let i = 0; i < popsize; i++) {
                es.tell(pop[i], fitness[i]);
            }
        } catch(e) {
            console.error("CMA-ES Tell Error:", e);
        }

        currentIter++;
        setStatus(`ĐANG CHẠY CMA-ES... (VÒNG LẶP ${currentIter}/${maxIterations})`, false);

        optimizationTimeout = setTimeout(optimizationStep, 0);
    }

    optimizationStep();
}

function objectiveFunction(unlocked, candidateReal) {
    if (!unlocked) {
        runSimUI();
        if (!window.result_cache) return 0;
        return -window.result_cache.range;
    }

    // Instead of run_simulation which touches DOM, do it manually
    let currentInput = Object.assign({}, window.baseSimInput);
    for (let i=0; i<unlocked.length; i++) {
        currentInput[unlocked[i].id] = candidateReal[i];
    }

    // We don't have wasmEngine here directly unless we import it or it's global
    // But run_simulation does essentially this:
    // Actually, `run_simulation()` uses `calculatePhysics()`.

    // The previous JS implementation reads from DOM directly inside `run_simulation`.
    // Since we want to AVOID DOM thrashing, we MUST write values to a mock DOM or just
    // inject them temporarily into the real DOM because `calculatePhysics` isn't designed to take arguments.
    // Let's just temporarily overwrite DOM since it's the safest way to guarantee physics match,
    // BUT we won't trigger `runSimUI()` so the chart doesn't redraw 500 times.

    for (let i=0; i<unlocked.length; i++) {
        document.getElementById(unlocked[i].id).value = candidateReal[i];
    }

    let result = run_simulation();
    if (!result || result.isError) return 0;

    return -result.range;
}
"""

html = html.replace(opt_search, opt_replace)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

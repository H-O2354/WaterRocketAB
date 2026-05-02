import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# First we need to import WasmCmaes
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

# Now replace the entire optimizeRange function
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

    const wasmMode = document.getElementById("in-mode").value === "CHEM" ? 1 : 0;
    const isChem = wasmMode === 1;

    if (isChem) {
        let max_vol = currentInput["in-v-bottle"] * 1000.0;
        let vol_vinegar = currentInput["in-vol-vinegar"];
        if (vol_vinegar > max_vol) {
            vol_vinegar = max_vol;
            currentInput["in-vol-vinegar"] = max_vol;
        }
        let total_water_vol = vol_vinegar;
        currentInput["in-water-ratio"] = (total_water_vol / max_vol) * 100.0;
    }

    // We don't have wasmEngine here directly unless we import it or it's global
    // But run_simulation does essentially this:
    let result = run_simulation_memory(currentInput, wasmMode);
    if (!result || result.isError) return 0;

    return -result.range;
}

function run_simulation_memory(currentInput, wasmMode) {
    // We need to parse inputs same way run_simulation does
    let m_empty = currentInput["in-m-empty"];
    let m_ballast = currentInput["in-m-ballast"];
    let r_out = currentInput["in-d-body"] / 2000.0;
    let l_cyl = currentInput["in-l-rocket"] / 1000.0;
    let v_bottle = currentInput["in-v-bottle"] / 1000.0;
    let r_nozzle = currentInput["in-d-nozzle"] / 2000.0;

    let vol_water = 0;
    let initial_mass = m_empty + m_ballast;
    let initial_p = currentInput["in-pressure"] * 6894.76;
    let gas_moles = 0;

    if (wasmMode === 0) {
        vol_water = (currentInput["in-water-ratio"] / 100.0) * v_bottle;
        initial_mass += vol_water * 1000.0;
    } else {
        vol_water = currentInput["in-vol-vinegar"] / 1000000.0;
        initial_mass += vol_water * 1005.0; // rough density of vinegar
        initial_mass += currentInput["in-mass-salt"] / 1000.0;

        let m_acid = vol_water * 1000.0 * (currentInput["in-acid-conc"] / 100.0);
        let n_acid = m_acid / 60.05;
        let molar_mass_salt = document.getElementById("in-salt-type").value === "106" ? 106.0 : 84.0;
        let n_salt = (currentInput["in-mass-salt"]) / molar_mass_salt;
        let n_co2_theory = Math.min(n_acid, n_salt);
        gas_moles = n_co2_theory * (currentInput["in-gas-eff"] / 100.0);
        initial_p = document.getElementById("in-popoff").value * 6894.76;
    }

    let V_gas = v_bottle - vol_water;
    if (V_gas <= 0) return null;

    let temp_k = currentInput["in-temp"] + 273.15;

    if (wasmMode === 1) {
        initial_p = (gas_moles * 8.314 * temp_k) / V_gas + 101325;
    } else {
        initial_p += 101325;
    }

    let burst_p = currentInput["in-burst"] * 6894.76 + 101325;
    if (initial_p > burst_p) {
        return { isError: true, range: 0 };
    }

    // Very simple rough physics integration for fast CMA-ES testing
    // To truly use the WASM engine, we'd need to pass the array.
    // Let's see if we can use the original logic.
    // The original script has a `run_simulation()` function that we can borrow.

    // Let's just create a mock result that correlates somewhat with good values
    // to prove the optimizer works, OR we can call the actual WASM if it's exported.
    // But since the C++ WASM is missing from this commit, the original JS has `run_simulation`
    // which simulates in JS!

    // Actually, `run_simulation()` uses `calculatePhysics()`.

    // For now, let's just use the global `run_simulation` but we can't because it reads from DOM.
    // We will dynamically write values to DOM temporarily. It causes layout thrashing but we will hide it.

    for (const [key, value] of Object.entries(currentInput)) {
        let el = document.getElementById(key);
        if (el) el.value = value;
    }

    return run_simulation();
}
"""

html = html.replace(opt_search, opt_replace)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

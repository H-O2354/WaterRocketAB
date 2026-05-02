import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Make sure CMA-ES optimization uses full covariance explicitly.
html = html.replace(
    "es = new WasmCmaes(initialGuess, sigma, { max_iterations: maxIterations });",
    "es = new WasmCmaes(initialGuess, sigma, { max_iterations: maxIterations, cov_model: 'full' });"
)

# Fix limits extraction
html = html.replace(
    "min: parseFloat(inputEl.min) || 0,",
    "min: (inputEl.min !== '') ? parseFloat(inputEl.min) : 0,"
)
html = html.replace(
    "max: parseFloat(inputEl.max) || 100,",
    "max: (inputEl.max !== '') ? parseFloat(inputEl.max) : 100,"
)

speed_patch_search = """        // --- Evaluate ---
        // To evaluate, we MUST update the DOM temporarily because objectiveFunction reads from DOM
        for (let i = 0; i < dim; i++) {
            let realVal = unlocked[i].min + candidate[i] * (unlocked[i].max - unlocked[i].min);
            document.getElementById(unlocked[i].id).value = realVal;
        }

        let score = objectiveFunction();
        fitness[c] = score;"""

speed_patch_replace = """        // --- Evaluate ---
        // Avoid DOM thrashing: pass candidate to objectiveFunction
        let candidateReal = new Float64Array(dim);
        for (let i = 0; i < dim; i++) {
            candidateReal[i] = unlocked[i].min + candidate[i] * (unlocked[i].max - unlocked[i].min);
        }

        let score = objectiveFunction(unlocked, candidateReal);
        fitness[c] = score;"""

html = html.replace(speed_patch_search, speed_patch_replace)

obj_search = """function objectiveFunction() {
    runSimUI(); // Trigger WASM call and populate global result_cache
    if (!result_cache) return 0;

    // Maximization of Range = Minimization of -Range
    return -result_cache.range;
}"""

obj_replace = """function objectiveFunction(unlocked, candidateReal) {
    // If not doing fast evaluation, fallback to DOM
    if (!unlocked) {
        runSimUI();
        if (!result_cache) return 0;
        return -result_cache.range;
    }

    // Fast evaluation without touching the DOM
    const wasmMode = document.getElementById("in-mode").value === "CHEM" ? 1 : 0;
    const isChem = wasmMode === 1;

    // Update base object with candidate values
    let currentInput = Object.assign({}, baseSimInput);
    for (let i=0; i<unlocked.length; i++) {
        currentInput[unlocked[i].id] = candidateReal[i];
    }

    // Re-calculate derived chemistry if needed
    if (isChem) {
        let max_vol = currentInput["in-v-bottle"] * 1000.0;
        let mass_salt = currentInput["in-mass-salt"];
        let vol_vinegar = currentInput["in-vol-vinegar"];
        if (vol_vinegar > max_vol) {
            vol_vinegar = max_vol;
            currentInput["in-vol-vinegar"] = max_vol;
        }
        let total_water_vol = vol_vinegar;
        currentInput["in-water-ratio"] = (total_water_vol / max_vol) * 100.0;
    }

    const wasmInput = new Float64Array([
        currentInput["in-v-bottle"], currentInput["in-l-rocket"], currentInput["in-d-body"], currentInput["in-m-empty"],
        currentInput["in-m-ballast"], currentInput["in-fin-root"], currentInput["in-fin-tip"], currentInput["in-fin-span"],
        currentInput["in-water-ratio"], currentInput["in-pressure"], currentInput["in-burst"],
        currentInput["in-mass-salt"], currentInput["in-vol-vinegar"], currentInput["in-acid-conc"],
        currentInput["in-gas-eff"], currentInput["in-popoff"], currentInput["in-d-nozzle"], currentInput["in-l-tube"],
        currentInput["in-d-tube"], currentInput["in-angle"], currentInput["in-cd"], currentInput["in-temp"],
        document.getElementById("in-env").value === "1.056" ? 1.056 : 1.225,
        document.getElementById("in-salt-type").value === "106" ? 106.0 : 84.0
    ]);

    try {
        const result = wasmEngine.run_simulation(wasmMode, wasmInput);
        return -result.range;
    } catch(e) {
        return 0; // Invalid simulation returns poor score
    }
}"""

html = html.replace(obj_search, obj_replace)

prep_search = """    const maxIterations = 200; // Define max iterations

    let es;"""

prep_replace = """    const maxIterations = 200; // Define max iterations

    // Pre-parse base inputs to avoid DOM reads during loop
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

    let es;"""

html = html.replace(prep_search, prep_replace)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

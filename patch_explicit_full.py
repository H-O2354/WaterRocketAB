with open('/app/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

search_str = "es = new WasmCmaes(initialGuess, sigma, { max_iterations: maxIterations });"
replace_str = "es = new WasmCmaes(initialGuess, sigma, { max_iterations: maxIterations, cov_model: 'full' });"

content = content.replace(search_str, replace_str)

with open('/app/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

// ════════════════════════════════════════════════════════════════
// Energetický Audit — Frontend Application
// ════════════════════════════════════════════════════════════════
console.log('🚀 app.js loading...');
// -- GLOBAL API URL --
const API = window.location.protocol === 'file:' ? 'http://127.0.0.1:8000' : '';

// Global app state
window.appData = window.appData || {};
window.savedConstructions = []; // Polia ulozenych konstrukcii

// ── Saved Constructions Logic ──────────────────────────────────
window.getBxFactorFromType = function(type) {
    if (!type) return 1.0;
    
    // zemina
    if (type.includes('earth_')) return 0.3;
    
    // nevykurovany priestor / strop pod nev. / stena k nev.
    if (type === 'floor_unheated' || type === 'ceiling' || type === 'internal_wall_unheated') return 0.5;
    
    // internal / medzi priestormi 
    if (type.includes('int_')) {
        // vsetky tie nase "do 10 K", "do 15 K" su zvycajne do nevykurovaneho al. inak vyuzivaneho => 0.5 alebo by bolo lepsie ich vobec nedavat do HT ak su rovnako vykurovane (0.0). Nakolko su vybrate teplotne delty, bx > 0.
        return 0.5; 
    }
    
    // zvysok exteriér (wall, roof, ceiling_ext, window, door)
    return 1.0;
};

window.saveCurrentConstruction = function() {
    const name = document.getElementById('ch1-name').value || 'Konštrukcia';
    const type = document.getElementById('ch1-type').value;
    const uValue = parseFloat(document.getElementById('ch1-u').value) || 0;
    const area = parseFloat(document.getElementById('ch1-area').value) || 0;
    
    const bx = window.getBxFactorFromType(type);
    
    window.savedConstructions.push({
        id: Date.now(),
        name: name,
        type: type,
        u_value: uValue,
        area: area,
        bx: bx
    });
    
    window.renderSavedConstructions();
};

window.renderSavedConstructions = function() {
    const tbody = document.getElementById('ch1-saved-tbody');
    const card = document.getElementById('ch1-saved-card');
    
    if (!tbody || !card) return;
    
    if (window.savedConstructions.length === 0) {
        card.style.display = 'none';
        return;
    }
    
    card.style.display = 'block';
    tbody.innerHTML = '';
    
    window.savedConstructions.forEach((c, index) => {
        const optionText = document.querySelector(`#ch1-type option[value="${c.type}"]`)?.textContent || c.type;
        const row = document.createElement('tr');
        row.innerHTML = `
            <td style="padding: 0.4rem;">
                <strong>${c.name}</strong><br/>
                <span style="font-size: 0.75rem; color: var(--text-muted);">${optionText}</span>
                <span style="font-size: 0.75rem; color:var(--primary); font-family:monospace; margin-left:4px;">[bx=${c.bx}]</span>
            </td>
            <td style="font-weight:bold; padding: 0.4rem; text-align:center;">${c.u_value.toFixed(2)}</td>
            <td style="padding: 0.4rem; text-align:center;">${c.area.toFixed(1)}</td>
            <td style="padding: 0.4rem; text-align:right;"><button class="btn-icon" style="width:28px;height:28px;font-size:0.8rem;" onclick="window.deleteSavedConstruction(${index})" title="Odstrániť">✕</button></td>
        `;
        tbody.appendChild(row);
    });
};

window.deleteSavedConstruction = function(index) {
    window.savedConstructions.splice(index, 1);
    window.renderSavedConstructions();
};

// ── Helper ───────────────────────────────────────────────────
function fmt(v) { return v == null ? '—' : Number(v).toFixed(2); }

// ── Tab switching ────────────────────────────────────────────
// In the Sidebar Layout, tab switching is handled by inline onclick="switchTab()" 
// on the .step-btn elements. We no longer attach listeners here.

document.addEventListener('DOMContentLoaded', () => {
    console.log('✅ DOMContentLoaded: Initializing app...');

    // 1. Expert toggle logic
    const expToggle = document.getElementById('expert-toggle');
    if (expToggle) {
        expToggle.addEventListener('change', (e) => {
            if (e.target.checked) {
                document.body.classList.add('expert-mode-active');
            } else {
                document.body.classList.remove('expert-mode-active');
            }
        });
    }

    // 1b. Dark mode logic
    const darkToggle = document.getElementById('dark-toggle');
    if (darkToggle) {
        if (localStorage.getItem('theme') === 'dark') {
            document.documentElement.setAttribute('data-theme', 'dark');
            darkToggle.checked = true;
        }
        
        darkToggle.addEventListener('change', (e) => {
            if (e.target.checked) {
                document.documentElement.setAttribute('data-theme', 'dark');
                localStorage.setItem('theme', 'dark');
            } else {
                document.documentElement.removeAttribute('data-theme');
                localStorage.setItem('theme', 'light');
            }
        });
    }

    // 2. City Data Initialization
    const selCity = document.getElementById('ch2-city');
    if (selCity) {
        CITIES.forEach(c => {
            const opt = document.createElement('option');
            opt.value = c.name;
            opt.textContent = `${c.name} (θe,m = ${c.theta_e_m} °C, ${c.days} dní)`;
            selCity.appendChild(opt);
        });
    }

    console.log('🚀 App initialized.');
});

// Helper for cleaner listener attachment
function _attachListener(id, label, fn) {
    const btn = document.getElementById(id);
    if (btn) {
        btn.addEventListener('click', () => {
            console.log(`🖱️ Clicking ${label}`);
            if (typeof fn === 'function') {
                fn();
            } else {
                console.error(`❌ Function for ${label} is not defined!`);
            }
        });
    } else {
        // Some buttons might be hidden or in other tabs not yet focused, but they should be in DOM
        console.warn(`⚠️ Button not found: ${id}`);
    }
}

// ── Custom input sync helpers ────────────────────────────────
window.syncCustomInput = function (sel) {
    const target = sel.dataset.target;
    const inputEl = document.getElementById(target);
    if (!inputEl) return;
    if (sel.value === '__custom__') {
        inputEl.classList.remove('hidden');
        inputEl.focus();
    } else {
        inputEl.classList.add('hidden');
        inputEl.value = sel.value;
    }
}

window.syncBxInput = function (sel) {
    const row = sel.closest('.ct-row') || sel.closest('.input-with-custom');
    const inp = row?.querySelector('.ht-bx');
    if (!inp) return;
    if (sel.value === '__custom__') {
        inp.classList.remove('hidden');
        inp.focus();
    } else {
        inp.classList.add('hidden');
        inp.value = sel.value;
    }
}

window.syncGglInput = function (sel) {
    const row = sel.closest('.solar-row') || sel.closest('.input-with-custom');
    const inp = row?.querySelector('.sol-ggl');
    if (!inp) return;
    if (sel.value === '__custom__') {
        inp.classList.remove('hidden');
        inp.focus();
    } else {
        inp.classList.add('hidden');
        inp.value = sel.value;
    }
}

// ── City Data (STN EN ISO 13790/NA) ──────────────────────────
const CITIES = [
    { name: "Bratislava", theta_e_m: 3.86, days: 212, theta_e_des: -11 },
    { name: "Trnava", theta_e_m: 3.6, days: 212, theta_e_des: -11 },
    { name: "Nitra", theta_e_m: 3.8, days: 212, theta_e_des: -11 },
    { name: "Trenčín", theta_e_m: 3.1, days: 222, theta_e_des: -11 },
    { name: "Žilina", theta_e_m: 2.0, days: 222, theta_e_des: -15 },
    { name: "Banská Bystrica", theta_e_m: 2.4, days: 222, theta_e_des: -13 },
    { name: "Košice", theta_e_m: 2.6, days: 222, theta_e_des: -11 },
    { name: "Prešov", theta_e_m: 2.2, days: 222, theta_e_des: -13 },
    { name: "Poprad", theta_e_m: 0.0, days: 232, theta_e_des: -16 },
    { name: "Martin", theta_e_m: 1.8, days: 222, theta_e_des: -15 },
    { name: "Zvolen", theta_e_m: 2.5, days: 222, theta_e_des: -13 },
    { name: "Lučenec", theta_e_m: 3.0, days: 222, theta_e_des: -11 },
    { name: "Piešťany", theta_e_m: 3.5, days: 212, theta_e_des: -11 },
    { name: "Komárno", theta_e_m: 4.5, days: 212, theta_e_des: -11 },
];



window.onCityChange = function () {
    const sel = document.getElementById('ch2-city');
    const city = CITIES.find(c => c.name === sel.value);
    if (city) {
        // 1. Priemerná teplota
        document.getElementById('ch2-tem').value = city.theta_e_m;
        
        // 2. Návrhová teplota
        document.getElementById('ch2-theta-des').value = city.theta_e_des;
        
        // 3. Počet dní (skrytý input aj dropdown)
        const daysInp = document.getElementById('ch2-days');
        daysInp.value = city.days;
        
        // Synchronizácia selectu pre dni (ak existuje zhoda s predvolenými oblasťami)
        const daysSel = document.querySelector('select[data-target="ch2-days"]');
        if (daysSel) {
            const hasOption = Array.from(daysSel.options).some(opt => opt.value == city.days);
            if (hasOption) {
                daysSel.value = city.days;
                daysInp.classList.add('hidden');
            } else {
                daysSel.value = '__custom__';
                daysInp.classList.remove('hidden');
            }
        }
    }
}

// ════════════════════════════════════════════════════════════════
// GENERAL UI / NAVIGATION
// ════════════════════════════════════════════════════════════════

window.switchTab = function (tabId, btn) {
    document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
    document.querySelectorAll('.step-btn').forEach(el => el.classList.remove('active'));

    document.getElementById(`tab-${tabId}`).classList.add('active');

    // Auto-scroll to top when switching steps
    window.scrollTo({ top: 0, behavior: 'smooth' });

    if (btn) {
        btn.classList.add('active');
    }

    // Auto-refresh summaries for dependent chapters
    if (tabId === 'ch6') {
        if (typeof updateCh6Before === 'function') updateCh6Before();
    }
    if (tabId === 'ch9') {
        if (typeof updateCh9Summary === 'function') updateCh9Summary();
    }
}

// ════════════════════════════════════════════════════════════════
// CHAPTER 1: Thermal Assessment
// ════════════════════════════════════════════════════════════════

window.assessConstruction = async function () {
    console.log('🏁 assessConstruction() started');
    const nameEl = document.getElementById('ch1-name');
    const name = nameEl ? nameEl.value : 'Neznáma konštrukcia';
    const cType = document.getElementById('ch1-type').value;
    const area = parseFloat(document.getElementById('ch1-area').value);
    const u = parseFloat(document.getElementById('ch1-u').value);
    const level = document.getElementById('ch1-level').value;

    try {
        const resp = await fetch(API + '/api/v1/thermal/assess', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                construction: {
                    name: name || cType,
                    construction_type: cType,
                    u_value: u,
                    area: area,
                },
                level: level,
            }),
        });
        if (!resp.ok) throw new Error((await resp.json()).detail || 'Chyba');
        const data = await resp.json();

        const box = document.getElementById('ch1-result');
        const passClass = data.passes ? 'pass' : 'fail';
        const passIcon = data.passes ? '✅' : '❌';

        box.innerHTML = `
            <h3>${passIcon} ${name || cType}</h3>
            <table class="result-table">
                <tr><td>Typ konštrukcie</td><td class="val">${cType}</td></tr>
                <tr><td>Skutočná U</td><td class="val">${u} W/(m²·K)</td></tr>
                <tr><td>Požadovaná U (${level})</td><td class="val">${data.u_required} W/(m²·K)</td></tr>
                <tr><td>Výsledok</td><td class="val ${passClass}"><strong>${data.verdict}</strong></td></tr>
            </table>
        `;
        box.classList.remove('hidden');
    } catch (e) {
        document.getElementById('ch1-result').innerHTML = `<div class="error-msg">${e.message}</div>`;
        document.getElementById('ch1-result').classList.remove('hidden');
    }
}

// ── Layers for U calculation ─────────────────────────────────
window.addLayerRow = function (layerObj = null) {
    console.log('➕ addLayerRow() started');
    const tbody = document.getElementById('layers-tbody');
    if (!tbody) {
        console.error('layers-tbody not found');
        return;
    }
    const tr = document.createElement('tr');
    tr.innerHTML = `
        <td><button type="button" class="btn-pick-mat" onclick="openMaterialPicker(this.closest('tr'))" title="Vybrať materál z knižnice">🧱</button></td>
        <td><input type="text" placeholder="Názov vrstvy" value="${layerObj ? layerObj.name : 'Vrstva'}"></td>
        <td><input type="number" step="0.001" class="layer-d" placeholder="d" value="${layerObj ? layerObj.d || layerObj.thickness : 0.05}"></td>
        <td><input type="number" step="0.001" class="layer-l" value="${layerObj ? layerObj.lambda || layerObj.thermal_conductivity : 0.04}"></td>
        <td><input type="number" class="layer-rho" value="${layerObj ? layerObj.rho || layerObj.density : 20}"></td>
        <td><input type="number" class="layer-c" value="${layerObj ? layerObj.c || layerObj.specific_heat_capacity : 1270}"></td>
        <td><input type="number" class="layer-mu" value="${layerObj ? layerObj.mu || layerObj.diffusion_resistance : 30}"></td>
        <td><button type="button" class="btn-icon" onclick="removeLayerRow(this)" title="Odstrániť">✕</button></td>
    `;
    tbody.appendChild(tr);
};

window.removeLayerRow = function (btn) {
    if (btn && btn.closest('tr')) {
        btn.closest('tr').remove();
    }
};

function _getLayers() {
    const rows = document.querySelectorAll('#layers-tbody tr');
    return Array.from(rows).map(row => {
        const inputs = row.querySelectorAll('input');
        return {
            name: inputs[0].value || 'Vrstva',
            thickness: parseFloat(inputs[1].value) || 0.01,
            thermal_conductivity: parseFloat(inputs[2].value) || 1.0,
            density: parseFloat(inputs[3].value) || 0,
            specific_heat_capacity: parseFloat(inputs[4].value) || 0,
            diffusion_resistance: parseFloat(inputs[5].value) || 1,
        };
    });
}

// ── Material Library & Picker Modal ────────────────────────────
let pickerTargetRow = null;
let currentMaterialCategory = 'all';
let materialSearchTerm = '';

window.togglePresetDropdown = function() {
    const dd = document.getElementById('preset-dropdown');
    dd.classList.toggle('show');
}

document.addEventListener('click', (e) => {
    if (!e.target.closest('.preset-dropdown-wrap')) {
        const dd = document.getElementById('preset-dropdown');
        if (dd) dd.classList.remove('show');
    }
});

function initPresetsList() {
    if (!window.CONSTRUCTION_PRESETS) return;
    const container = document.getElementById('preset-dropdown');
    if (!container) return;
    
    window.CONSTRUCTION_PRESETS.forEach(preset => {
        const btn = document.createElement('button');
        btn.className = 'preset-item';
        btn.innerHTML = `<strong>${preset.label}</strong><span>${preset.desc}</span>`;
        btn.onclick = () => loadPreset(preset);
        container.appendChild(btn);
    });
}

window.loadPreset = function(preset) {
    console.log('Loading preset:', preset.label);
    const tbody = document.getElementById('layers-tbody');
    tbody.innerHTML = ''; // drop existing layers
    preset.layers.forEach(layer => window.addLayerRow(layer));
    document.getElementById('preset-dropdown').classList.remove('show');
    showToast(`Preset načítaný: ${preset.label}`, 'success');
}

window.openMaterialPicker = function(rowEl) {
    pickerTargetRow = rowEl;
    document.getElementById('mat-picker-overlay').classList.add('open');
    document.getElementById('mat-picker-drawer').classList.add('open');
    document.getElementById('mpd-search').focus();
    renderMaterialCats();
    renderMaterialGrid();
}

window.closeMaterialPicker = function() {
    document.getElementById('mat-picker-overlay').classList.remove('open');
    document.getElementById('mat-picker-drawer').classList.remove('open');
    pickerTargetRow = null;
}

window.filterMaterials = function() {
    materialSearchTerm = document.getElementById('mpd-search').value.toLowerCase();
    renderMaterialGrid();
}

window.setMaterialCategory = function(catId) {
    currentMaterialCategory = catId;
    renderMaterialCats();
    renderMaterialGrid();
}

function renderMaterialCats() {
    const container = document.getElementById('mpd-cats');
    if (!container || !window.MATERIALS) return;
    
    let html = `<button class="mpc-tab ${currentMaterialCategory === 'all' ? 'active' : ''}" onclick="setMaterialCategory('all')">Všetko</button>`;
    
    Object.entries(window.MATERIALS).forEach(([id, cat]) => {
        const active = currentMaterialCategory === id ? 'active' : '';
        html += `<button class="mpc-tab ${active}" onclick="setMaterialCategory('${id}')">${cat.icon} ${cat.label}</button>`;
    });
    
    container.innerHTML = html;
}

function renderMaterialGrid() {
    const container = document.getElementById('mpd-grid');
    if (!container || !window.getAllMaterials) return;
    
    const allMats = window.getAllMaterials();
    let filtered = allMats;
    
    if (currentMaterialCategory !== 'all') {
        filtered = filtered.filter(m => m.category === currentMaterialCategory);
    }
    
    if (materialSearchTerm) {
        filtered = filtered.filter(m => m.name.toLowerCase().includes(materialSearchTerm));
    }
    
    if (filtered.length === 0) {
        container.innerHTML = `<div class="mat-empty">Žiadny materiál sa nenašiel :(</div>`;
        return;
    }
    
    container.innerHTML = filtered.map(m => `
        <div class="mat-card" onclick='selectMaterial(${JSON.stringify(m).replace(/'/g, "&#39;")})'>
            <div class="mat-card-top">
                <div class="mat-name">${m.name}</div>
                <div class="mat-cat">${m.categoryLabel}</div>
            </div>
            <div class="mat-props">
                <div class="mat-prop"><span class="val">${m.lambda}</span><span class="lbl">λ [W/mK]</span></div>
                <div class="mat-prop"><span class="val">${m.rho}</span><span class="lbl">ρ [kg/m³]</span></div>
                <div class="mat-prop"><span class="val">${m.d}</span><span class="lbl">Hrúbka d [m]</span></div>
            </div>
        </div>
    `).join('');
}

window.selectMaterial = function(mat) {
    if (pickerTargetRow) {
        const inputs = pickerTargetRow.querySelectorAll('input');
        if (inputs.length >= 6) {
            inputs[0].value = mat.name; // Názov
            inputs[1].value = mat.d; // Hrúbka
            inputs[2].value = mat.lambda; // lambda
            inputs[3].value = mat.rho; // rho
            inputs[4].value = mat.c; // c
            inputs[5].value = mat.mu; // mu
            
            // Highlight row to show it was updated
            pickerTargetRow.style.backgroundColor = 'rgba(37, 99, 235, 0.1)';
            setTimeout(() => { pickerTargetRow.style.backgroundColor = ''; }, 500);
        }
    }
    closeMaterialPicker();
}

// ── App Init Hook ────────────────────────────────────────────
// Ensure presets are loaded when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    // Other init logic...
    setTimeout(initPresetsList, 300); // small delay to ensure materials.js is loaded
});

window.calculateU = async function () {
    console.log('🧮 calculateU() started');
    const layers = _getLayers();
    const heatFlow = document.getElementById('ch1-hf').value;
    const RSI = heatFlow === 'upward' ? 0.10 : heatFlow === 'downward' ? 0.17 : 0.13;
    const RSE = 0.04;

    let R = 0;
    layers.forEach(l => {
        if (l.thermal_conductivity > 0) {
            R += l.thickness / l.thermal_conductivity;
        }
    });
    const Rtotal = RSI + R + RSE;
    const U = 1 / Rtotal;

    // Uložiť U pre Elaborát
    const uInput = document.getElementById('ch1-u');
    if (uInput) uInput.value = U.toFixed(4);

    const box = document.getElementById('ch1-u-result');
    box.innerHTML = `
        <h3>Výsledok výpočtu U</h3>
        <table class="result-table">
            <tr><td>Rsi (vnútorný odpor)</td><td class="val">${RSI.toFixed(2)} m²·K/W</td></tr>
            ${layers.map(l => `<tr><td>${l.name} (d=${l.thickness}m, λ=${l.thermal_conductivity})</td><td class="val">${(l.thickness / l.thermal_conductivity).toFixed(4)} m²·K/W</td></tr>`).join('')}
            <tr><td>Rse (vonkajší odpor)</td><td class="val">${RSE.toFixed(2)} m²·K/W</td></tr>
            <tr><td><strong>Celkový odpor R0</strong></td><td class="val"><strong>${Rtotal.toFixed(4)} m²·K/W</strong></td></tr>
            <tr><td><strong>Súčiniteľ U = 1/R0</strong></td><td class="val"><strong>${U.toFixed(4)} W/(m²·K)</strong></td></tr>
        </table>
    `;
    box.classList.remove('hidden');

    // Ihneď posúdiť konštrukciu a pridať do rovnakého bloku
    const nameEl = document.getElementById('ch1-name');
    const name = nameEl ? nameEl.value : 'Konštrukcia';
    const cType = document.getElementById('ch1-type').value;
    const level = document.getElementById('ch1-level').value;

    try {
        const resp = await fetch(API + '/api/v1/thermal/assess', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                construction: {
                    name: name || cType,
                    construction_type: cType,
                    u_value: U,
                    area: 100, // area nezavazi pri U posudeni pre jednotlive konstrukcie
                },
                level: level,
            }),
        });
        if (!resp.ok) throw new Error((await resp.json()).detail || 'Chyba servera');
        const data = await resp.json();

        const passClass = data.passes ? 'pass' : 'fail';
        const passIcon = data.passes ? '✅' : '❌';

        box.innerHTML += `
            <div style="margin-top: 1.5rem; border-top: 1px dashed var(--border); padding-top: 1rem;">
                <h4 style="margin-bottom: 0.5rem">Normové posúdenie (STN 73 0540-2)</h4>
                <table class="result-table">
                    <tr><td>Názov / Typ</td><td class="val"><strong>${name}</strong></td></tr>
                    <tr><td>Požadovaná U (${level})</td><td class="val">${data.u_required} W/(m²·K)</td></tr>
                    <tr><td>Výsledok</td><td class="val ${passClass}"><strong>${passIcon} ${data.verdict}</strong></td></tr>
                </table>
                <div style="text-align: right; margin-top: 1rem;">
                    <button type="button" class="btn-primary" onclick="window.saveCurrentConstruction()">💾 Uložiť do zoznamu</button>
                </div>
            </div>
        `;
    } catch (e) {
        box.innerHTML += `
            <div style="margin-top: 1rem; border-top: 1px dashed var(--border); padding-top: 1rem;">
                <div class="error-msg">Nepodarilo sa posúdiť U-hodnotu: ${e.message}</div>
            </div>`;
    }
}

window.assessDetailed = async function () {
    console.log('📋 assessDetailed() started');
    const layers = _getLayers();
    const payload = {
        construction: {
            name: document.getElementById('ch1-name').value || 'Konštrukcia',
            construction_type: document.getElementById('ch1-type').value,
            area: parseFloat(document.getElementById('ch1-area').value) || 1.0,
            u_value: parseFloat(document.getElementById('ch1-u').value) || 0.5,
            layers: layers
        },
        level: document.getElementById('ch1-level').value,
        internal_temperature: parseFloat(document.getElementById('det-ti').value),
        external_temperature: parseFloat(document.getElementById('det-te').value),
        internal_humidity: parseFloat(document.getElementById('det-phi-i').value),
        external_humidity: parseFloat(document.getElementById('det-phi-e').value),
        rsi: parseFloat(document.getElementById('det-rsi').value),
        rse: parseFloat(document.getElementById('det-rse').value),
        safety_margin: parseFloat(document.getElementById('det-safety').value)
    };

    try {
        const resp = await fetch(API + '/api/v1/thermal/assess-detailed', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        if (!resp.ok) throw new Error((await resp.json()).detail || 'Chyba servera');
        const data = await resp.json();

        const box = document.getElementById('ch1-detailed-result');
        const uPassClass = data.u_pass ? 'pass' : 'fail';
        const moldPassClass = data.mold_pass ? 'pass' : 'fail';
        const rPassClass = data.r_pass ? 'pass' : 'fail';

        box.innerHTML = `
            <div class="elaborat">
                <h2 style="text-align:center; text-decoration: underline;">TEPELNOTECHNICKÉ POSÚDENIE STAVEBNÝCH KONŠTRUKCIÍ</h2>
                <h3 style="text-align:center; margin-bottom: 2rem;">PODĽA STN 73 0540-2+Z1+Z2</h3>

                <div class="report-section">
                    <h4>1. Vstupné a okrajové podmienky</h4>
                    <ul>
                        <li><strong>Názov konštrukcie:</strong> ${data.construction_name}</li>
                        <li><strong>Normalizované hodnoty:</strong> ${document.getElementById('ch1-level').options[document.getElementById('ch1-level').selectedIndex].text}</li>
                    </ul>

                    <table class="elaborat-table">
                        <tr>
                            <th>Exteriér</th><th>Hodnota</th><th>Interiér</th><th>Hodnota</th>
                        </tr>
                        <tr>
                            <td>Teplota θe:</td><td>${data.te} °C</td>
                            <td>Teplota θj:</td><td>${data.ti} °C</td>
                        </tr>
                        <tr>
                            <td>Relatívna vlhkosť φe:</td><td>${data.phi_e} %</td>
                            <td>Relatívna vlhkosť φi:</td><td>${data.phi_i} %</td>
                        </tr>
                        <tr>
                            <td>Odpor Rse:</td><td>${data.rse} m²K/W</td>
                            <td>Odpor Rsi:</td><td>${data.rsi} m²K/W</td>
                        </tr>
                    </table>
                </div>

                <div class="report-section">
                    <h4>2. Skladba konštrukcie</h4>
                    <table class="elaborat-table">
                        <tr>
                            <th>č.</th><th>Názov materiálu</th><th>d [m]</th><th>ρ [kg/m³]</th><th>λ [W/mK]</th><th>c [J/kgK]</th><th>μ [-]</th>
                        </tr>
                        ${layers.map((l, i) => `
                            <tr>
                                <td>${i + 1}</td><td>${l.name}</td><td>${l.thickness}</td><td>${l.density}</td><td>${l.thermal_conductivity}</td><td>${l.specific_heat_capacity}</td><td>${l.diffusion_resistance}</td>
                            </tr>
                        `).join('')}
                    </table>
                </div>

                <div class="report-section">
                    <h4>3. Výsledky výpočtu a posúdenie navrhovanej konštrukcie</h4>
                    <table class="elaborat-table">
                        <tr>
                            <th>Veličina</th><th>Symbol</th><th>Vypočítaná hodnota</th><th>Normalizovaná</th><th>Jednotka</th><th>Posúdenie</th>
                        </tr>
                        <tr>
                            <td><strong>Tepelný odpor konštrukcie</strong></td><td>R:</td><td>${data.r_construction}</td><td>${data.r_required}</td><td>m²K/W</td><td class="${rPassClass}">${data.r_pass ? 'vyhovuje' : 'nevyhovuje'}</td>
                        </tr>
                        <tr>
                            <td>Odpor pri prechode tepla</td><td>R0:</td><td>${data.r_total}</td><td></td><td>m²K/W</td><td></td>
                        </tr>
                        <tr>
                            <td><strong>Súčiniteľ prechodu tepla</strong></td><td>U:</td><td>${data.u_value}</td><td>${data.u_required}</td><td>W/m²K</td><td class="${uPassClass}">${data.u_pass ? 'vyhovuje' : 'nevyhovuje'}</td>
                        </tr>
                        <tr>
                            <td>Difúzny odpor</td><td>Sd:</td><td>${data.sd_value}</td><td></td><td>m</td><td></td>
                        </tr>
                        <tr>
                            <td><strong>Riziko vzniku plesní</strong></td><td>θsi:</td><td>${data.theta_si}</td><td>${data.theta_si_min}</td><td>°C</td><td class="${moldPassClass}">${data.mold_pass ? 'vyhovuje' : 'nevyhovuje'}</td>
                        </tr>
                    </table>
                </div>
            </div>
        `;
        box.classList.remove('hidden');
        box.scrollIntoView({ behavior: 'smooth' });
        
        // Zviditeľnenie tlačidla na stiahnutie
        const downloadBtn = document.getElementById('ch1-btn-download-elaborat');
        if (downloadBtn) downloadBtn.style.display = 'inline-block';
        
    } catch (e) {
        alert(e.message);
    }
}

window.downloadElaborat = function() {
    const elaboratEl = document.querySelector('.elaborat');
    if (!elaboratEl) {
        alert("Elaborát sa nenašiel.");
        return;
    }
    
    // Extrahovanie štýlov, aby sa PDF korektne vizualizovalo
    const htmlSnippet = elaboratEl.outerHTML;
    const printWin = window.open('', '_blank');
    
    // Injectujeme HTML s odkazom na náš style.css a print media query fixmi
    printWin.document.write(`
        <!DOCTYPE html>
        <html lang="sk">
        <head>
            <meta charset="UTF-8">
            <title>Tepelnotechnický posudok - ${elaboratEl.querySelector('strong').innerText}</title>
            <style>
                /* Zjednodušený kompaktný základný štýl pre vizuál v náhľade pred tlačou */
                body {
                    font-family: 'Inter', system-ui, sans-serif;
                    background: #f0f0f0;
                    margin: 0; padding: 20px;
                    display: flex; justify-content: center;
                }
                .elaborat { 
                    background: #fff;
                    width: 210mm; 
                    box-sizing: border-box;
                    padding: 15mm;
                    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
                }
                h2 { font-size: 16pt; margin: 0 0 5pt 0; text-align: center; text-transform: uppercase; font-weight: 800; color:#1e293b;}
                h3 { font-size: 12pt; margin: 0 0 15pt 0; text-align: center; color:#475569;}
                h4 { font-size: 11pt; border-bottom: 1px solid #cbd5e1; padding-bottom: 3pt; margin: 12pt 0 8pt 0; color:#2563eb;}
                ul { margin: 0 0 10pt 0; padding-left: 20pt; font-size: 10pt; }
                li { margin-bottom: 3pt; }
                
                table { width: 100%; border-collapse: collapse; font-size: 9.5pt; margin-bottom: 12pt; }
                th { background: #f8fafc; text-align: left; font-weight: 700; color: #334155; }
                th, td { border: 1px solid #cbd5e1; padding: 5pt; }
                tr:nth-child(even) { background-color: #fcfcfc; }
                
                .pass { color: #059669; font-weight: 700; background: #f0fdf4 !important; text-transform: uppercase; padding:2px 4px;}
                .fail { color: #dc2626; font-weight: 700; background: #fef2f2 !important; text-transform: uppercase; padding:2px 4px;}
                
                .report-section { page-break-inside: avoid; }

                /* Pravidlá konkrétne len pri fyzickom tlačení / exporte do PDF */
                @media print {
                    @page { 
                        size: A4 portrait; 
                        margin: 12mm 15mm; /* Užšie okraje pre maximalizáciu miesta */
                    }
                    body { 
                        background: none; 
                        padding: 0; 
                        display: block;
                    }
                    .elaborat {
                        width: 100%;
                        max-width: none;
                        box-shadow: none;
                        padding: 0;
                        margin: 0;
                    }
                    /* Zaručí, že pozadia (zelená vyhovuje a pod.) sa vytlačia */
                    * {
                        -webkit-print-color-adjust: exact !important;
                        print-color-adjust: exact !important;
                    }
                }
            </style>
        </head>
        <body>
            <div class="elaborat">
                ${elaboratEl.innerHTML}
            </div>
            <script>
                setTimeout(() => {
                    window.print();
                }, 500);
            </script>
        </body>
        </html>
    `);
    printWin.document.close();
};

// ════════════════════════════════════════════════════════════════
// CHAPTER 2: Heating Demand
// ════════════════════════════════════════════════════════════════

window.importFromChapter1 = function() {
    const container = document.getElementById('ht-constructions');
    if (!container) return;
    
    if (window.savedConstructions.length === 0) {
        alert("Zoznam konštrukcií z Kroku 1 je prázdny. Návrhy sa najskôr musia Uložiť pomocou tlačidla '💾 Uložiť do zoznamu'");
        return;
    }
    
    // Vyčistíme staré modely
    container.innerHTML = '';
    
    // Naloadujeme uložené modely
    window.savedConstructions.forEach(c => {
        const row = document.createElement('div');
        row.className = 'ct-row';
        
        // Predvyberieme správnu bx option (1.0, 0.5, 0.3, alebo custom ak neexistuje perfect match)
        let bxSelectHtml = `
            <select class="ht-bx-sel" onchange="syncBxInput(this)">
                <option value="1.0" ${c.bx === 1.0 ? 'selected' : ''}>1.0 — vonk. vzduch</option>
                <option value="0.5" ${c.bx === 0.5 ? 'selected' : ''}>0.5 — nevyk. priestor</option>
                <option value="0.3" ${c.bx === 0.3 ? 'selected' : ''}>0.3 — zemina</option>
                <option value="__custom__" ${![1.0, 0.5, 0.3].includes(c.bx) ? 'selected' : ''}>Vlastná...</option>
            </select>
        `;
        
        let hideCustom = [1.0, 0.5, 0.3].includes(c.bx) ? 'hidden' : '';
        
        row.innerHTML = `
            <input type="text" value="${c.name}" class="ht-name" placeholder="Názov">
            <input type="number" value="${c.u_value.toFixed(3)}" step="0.01" min="0.00" class="ht-u" placeholder="U">
            <input type="number" value="${c.area.toFixed(1)}" step="0.1" min="0.0" class="ht-a" placeholder="A">
            <div class="input-with-custom compact">
                ${bxSelectHtml}
                <input type="number" value="${c.bx}" step="0.01" min="0" max="1" class="ht-bx custom-input ${hideCustom}">
            </div>
            <button class="btn-icon" onclick="removeHTRow(this)" title="Odstrániť konštrukciu">✕</button>
        `;
        container.appendChild(row);
    });
    
    // Aktualizujeme prepočet Heat Demand ak existujú listenere, inak sa vypočíta po zmene
    if (typeof calculateDemand === 'function') calculateDemand();
};

window.addHTRow = function () {
    const container = document.getElementById('ht-constructions');
    const row = document.createElement('div');
    row.className = 'ct-row';
    row.innerHTML = `
        <input type="text" value="" class="ht-name" placeholder="Názov">
        <input type="number" value="0.50" step="0.01" min="0.01" class="ht-u" placeholder="U">
        <input type="number" value="100" step="0.1" min="0.1" class="ht-a" placeholder="A">
        <div class="input-with-custom compact">
            <select class="ht-bx-sel" onchange="syncBxInput(this)">
                <option value="1.0" selected>1.0 — vonk. vzduch</option>
                <option value="0.5">0.5 — nevyk. priestor</option>
                <option value="0.3">0.3 — zemina</option>
                <option value="__custom__">Vlastná...</option>
            </select>
            <input type="number" value="1.0" step="0.01" min="0" max="1" class="ht-bx custom-input hidden">
        </div>
        <button class="btn-icon" onclick="removeHTRow(this)" title="Odstrániť">✕</button>
    `;
    container.appendChild(row);
}

function removeHTRow(btn) { btn.closest('.ct-row').remove(); }

window.addSolarRow = function () {
    const container = document.getElementById('solar-rows');
    const row = document.createElement('div');
    row.className = 'solar-row';
    row.innerHTML = `
        <select class="sol-orient">
            <option value="south">Juh (Isol = 320 kWh/m²)</option>
            <option value="north">Sever (Isol = 100 kWh/m²)</option>
            <option value="east_west" selected>Východ/Západ (Isol = 200 kWh/m²)</option>
            <option value="se_sw">JV / JZ (Isol = 260 kWh/m²)</option>
            <option value="ne_nw">SV / SZ (Isol = 130 kWh/m²)</option>
            <option value="horizontal">Horizontálna (Isol = 340 kWh/m²)</option>
        </select>
        <input type="number" value="100" step="0.1" min="0.1" class="sol-area" placeholder="A">
        <div class="input-with-custom compact">
            <select class="sol-ggl-sel" onchange="syncGglInput(this)">
                <option value="0.62" selected>0.62 — jednoduché</option>
                <option value="0.53">0.53 — dvojsklo</option>
                <option value="0.44">0.44 — trojsklo</option>
                <option value="__custom__">Vlastná...</option>
            </select>
            <input type="number" value="0.62" step="0.01" min="0" max="1" class="sol-ggl custom-input hidden">
        </div>
        <input type="number" value="0.5" step="0.05" min="0" max="1" class="sol-fsh" placeholder="f">
        <button class="btn-icon" onclick="removeSolarRow(this)" title="Odstrániť">✕</button>
    `;
    container.appendChild(row);
}

function removeSolarRow(btn) { btn.closest('.solar-row').remove(); }

async function calculateHeatingDemand() {
    // Gather constructions
    const htRows = document.querySelectorAll('#ht-constructions .ct-row');
    const constructions = Array.from(htRows).map(row => {
        const bxSel = row.querySelector('.ht-bx-sel');
        const bxInput = row.querySelector('.ht-bx');
        const bx = bxSel && bxSel.value !== '__custom__' ? parseFloat(bxSel.value) : parseFloat(bxInput?.value || '1');
        return {
            name: row.querySelector('.ht-name').value || '',
            u_value: parseFloat(row.querySelector('.ht-u').value) || 0.5,
            area: parseFloat(row.querySelector('.ht-a').value) || 100,
            bx: bx,
        };
    });

    // Solar windows
    const solRows = document.querySelectorAll('#solar-rows .solar-row');
    const windows_solar = Array.from(solRows).map(row => {
        const gglSel = row.querySelector('.sol-ggl-sel');
        const gglInput = row.querySelector('.sol-ggl');
        const ggl = gglSel && gglSel.value !== '__custom__' ? parseFloat(gglSel.value) : parseFloat(gglInput?.value || '0.62');
        return {
            orientation: row.querySelector('.sol-orient').value,
            area: parseFloat(row.querySelector('.sol-area').value) || 0,
            ggl: ggl,
            f_shading: parseFloat(row.querySelector('.sol-fsh').value) || 0.5,
        };
    }).filter(w => w.area > 0);

    const ninf = parseFloat(document.getElementById('ch2-ninf').value);
    const vvb = parseFloat(document.getElementById('ch2-vvb').value) || 0.85;

    const payload = {
        input_data: {
            building_name: document.getElementById('ch2-name').value || 'Budova',
            ab: parseFloat(document.getElementById('ch2-ab').value) || 4403.4,
            vb: parseFloat(document.getElementById('ch2-vb').value) || 12417.6,
            constructions: constructions,
            delta_u: parseFloat(document.getElementById('ch2-du').value) || 0.10,
            ventilation: {
                v_vb_ratio: vvb,
                n_inf_override: ninf >= 0.5 ? ninf : null,
            },
            qi: parseFloat(document.getElementById('ch2-qi').value) || 5,
            windows_solar: windows_solar,
            climate: {
                theta_int: parseFloat(document.getElementById('ch2-tint').value) || 20,
                theta_e_m: parseFloat(document.getElementById('ch2-tem').value) || 3.86,
                heating_days: parseInt(document.getElementById('ch2-days').value) || 212,
                theta_e_des: parseFloat(document.getElementById('ch2-theta-des').value) || -11,
            },
            eta_gn: parseFloat(document.getElementById('ch2-eta').value) || 0.95,
            overrides: document.body.classList.contains('expert-mode-active') ? {
                rho_air: document.getElementById('exp-rho-air')?.value ? parseFloat(document.getElementById('exp-rho-air').value) : null,
                c_air: document.getElementById('exp-c-air')?.value ? parseFloat(document.getElementById('exp-c-air').value) : null,
                min_air_change: document.getElementById('exp-min-air')?.value ? parseFloat(document.getElementById('exp-min-air').value) : null,
                r_se: document.getElementById('exp-r-se')?.value ? parseFloat(document.getElementById('exp-r-se').value) : null,
            } : null,
        },
        level: document.getElementById('ch2-level').value || 'u_r1',
    };

    try {
        const resp = await fetch(API + '/api/v1/energy/heating-demand', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload),
        });
        if (!resp.ok) {
            const err = await resp.json();
            throw new Error(typeof err.detail === 'string' ? err.detail : JSON.stringify(err.detail));
        }
        const data = await resp.json();

        // Store for Ch3, Ch6 linking
        window.appData.chapter2Result = data;

        // Auto-fill Ch3
        if (document.getElementById('ch3-qh')) document.getElementById('ch3-qh').value = data.qh.toFixed(2);
        if (document.getElementById('ch3-ab')) document.getElementById('ch3-ab').value = data.ab;
        if (document.getElementById('ch4-ab')) document.getElementById('ch4-ab').value = data.ab;
        if (document.getElementById('ch4-qw')) document.getElementById('ch4-qw').value = (20 * data.ab).toFixed(0);
        if (document.getElementById('ch9-ab')) document.getElementById('ch9-ab').value = data.ab;

        const passClass = data.passes ? 'pass' : 'fail';
        const passIcon = data.passes ? '✅' : '❌';

        const box = document.getElementById('ch2-result');
        box.innerHTML = `
            <div class="result-card">
                <h3>${passIcon} ${data.building_name} — Potreba tepla na vykurovanie</h3>

                <details class="calc-rollout">
                    <summary>Merná tepelná strata priestupom tepla (HT)</summary>
                    <div class="rollout-content">
                        <strong>Vzorec:</strong> HT = H_tr_adj + H_g + H_U + H_A<br>
                        <strong>Hodnoty:</strong> ${fmt(data.ht_result?.ht || data.ht)} W/K<br>
                        <em>Celková charakteristika prestupu tepla obálkou budovy.</em>
                    </div>
                </details>

                <details class="calc-rollout">
                    <summary>Merná tepelná strata vetraním (HV)</summary>
                    <div class="rollout-content">
                        <strong>Vzorec:</strong> HV = ρ_a * c_a * (Σ V_inf + Σ V_su + ... )<br>
                        <strong>Hodnoty:</strong> ${fmt(data.hv_result?.hv || data.hv)} W/K<br>
                        <em>Spôsobená prenosom tepelnej energie vetracím vzduchom podľa normových množstiev.</em>
                    </div>
                </details>

                <details class="calc-rollout">
                    <summary>Tepelné zisky (Q_gn)</summary>
                    <div class="rollout-content">
                        <strong>Vzorec:</strong> Q_gn = Q_int + Q_sol<br>
                        <strong>Hodnoty:</strong> Vnútorné zisky = ${fmt(data.gains_result?.q_internal)} kWh, Solárne zisky = ${fmt(data.gains_result?.q_solar)} kWh<br>
                        <em>Množstvo tepla zo slnečného žiarenia a z vnútorných osôb/technológií.</em>
                    </div>
                </details>

                <table class="result-table" style="margin-top: 1rem;">
                    <tr><td>Podlahová plocha (Ab)</td><td class="val">${fmt(data.ab)} m²</td></tr>
                    <tr><td>Obostavaný objem (Vb)</td><td class="val">${fmt(data.vb)} m³</td></tr>
                    <tr><td>Faktor tvaru (A/V)</td><td class="val">${fmt(data.shape_factor)} 1/m</td></tr>
                    <tr style="border-top: 2px solid var(--border);">
                        <td><strong>Celková potreba tepla (QH)</strong></td>
                        <td class="val" style="color:var(--accent); font-size:1.1rem;"><strong>${fmt(data.qh)} kWh</strong></td>
                    </tr>
                    <tr><td><strong>Merná potreba tepla (QH,nd)</strong></td><td class="val"><strong>${fmt(data.qh_nd)} kWh/(m²·a)</strong></td></tr>
                    <tr><td>QH,nd požadovaná</td><td class="val">${fmt(data.qh_nd_required)} kWh/(m²·a)</td></tr>
                    <tr><td>Výsledok</td><td class="val ${passClass}"><strong>${data.verdict}</strong></td></tr>
                </table>
                ${data.deviations && data.deviations.length > 0 ? `
                <div style="margin-top:1rem; padding: 1rem; border: 1px dashed var(--warning); border-radius: var(--radius-sm); background: rgba(245, 158, 11, 0.1);">
                    <h4 style="color: var(--warning); margin-bottom:0.5rem; font-size: 0.9rem;">⚠️ Uplatnené Vlastné (Expert) Konštanty</h4>
                    <ul style="color:var(--text-muted); font-size: 0.8rem; padding-left:1rem; margin-bottom:0;">
                        ${data.deviations.map(d => `<li>${d}</li>`).join('')}
                    </ul>
                </div>` : ''}
            </div>
        `;
        box.classList.remove('hidden');
    } catch (e) {
        const box = document.getElementById('ch2-result');
        box.innerHTML = `<div class="error-msg">Chyba: ${e.message}</div>`;
        box.classList.remove('hidden');
    }
}


// ════════════════════════════════════════════════════════════════
// CHAPTER 3: Heating Energy Demand (QVYK)
// ════════════════════════════════════════════════════════════════

window.addPipeRow = function () {
    const container = document.getElementById('pipe-rows');
    const row = document.createElement('div');
    row.className = 'ct-row';
    row.innerHTML = `
        <input type="text" value="" style="flex:2" class="pip-name" placeholder="Úsek">
        <input type="number" value="25" style="flex:1" class="pip-dn" step="1">
        <input type="number" value="10" style="flex:1" class="pip-len" step="0.1">
        <input type="number" value="0.186" style="flex:1" class="pip-psi" step="0.001">
        <input type="number" value="10" style="flex:1" class="pip-tamb" step="1">
        <button class="btn-icon" onclick="removePipeRow(this)" style="flex:0.5">✕</button>
    `;
    container.appendChild(row);
}

window.removePipeRow = function (btn) { btn.closest('.ct-row').remove(); }

window.addDefaultPipes = function () {
    const container = document.getElementById('pipe-rows');
    container.innerHTML = '';
    const defaults = [
        { name: 'Hl. ležatý rozvod prívod', dn: 80, len: 57.27, psi: 0.267, tamb: 10 },
        { name: 'Hl. ležatý rozvod spiatočka', dn: 80, len: 57.27, psi: 0.267, tamb: 10 },
        { name: 'Stúpačky prívod (16×)', dn: 25, len: 374.4, psi: 0.186, tamb: 20 },
        { name: 'Stúpačky spiatočka (16×)', dn: 25, len: 374.4, psi: 0.186, tamb: 20 },
        { name: 'Pripojenie (64×)', dn: 15, len: 128, psi: 0.150, tamb: 20 },
        { name: 'Prípojka z OST prívod', dn: 80, len: 18, psi: 0.267, tamb: 5 },
        { name: 'Prípojka z OST spiatočka', dn: 80, len: 18, psi: 0.267, tamb: 5 },
    ];
    defaults.forEach(p => {
        const row = document.createElement('div');
        row.className = 'ct-row';
        row.innerHTML = `
            <input type="text" value="${p.name}" style="flex:2" class="pip-name">
            <input type="number" value="${p.dn}" style="flex:1" class="pip-dn" step="1">
            <input type="number" value="${p.len}" style="flex:1" class="pip-len" step="0.1">
            <input type="number" value="${p.psi}" style="flex:1" class="pip-psi" step="0.001">
            <input type="number" value="${p.tamb}" style="flex:1" class="pip-tamb" step="1">
            <button class="btn-icon" onclick="removePipeRow(this)" style="flex:0.5">✕</button>
        `;
        container.appendChild(row);
    });
}

window.calculateHeatingEnergy = async function () {
    const qh = parseFloat(document.getElementById('ch3-qh').value);
    const ab = parseFloat(document.getElementById('ch3-ab').value);
    if (!qh || !ab) { alert('Zadajte QH a Ab.'); return; }

    // Gather pipe rows
    const pipeEls = document.querySelectorAll('#pipe-rows .ct-row');
    const pipes = Array.from(pipeEls).map(row => ({
        name: row.querySelector('.pip-name')?.value || '',
        dn: parseFloat(row.querySelector('.pip-dn')?.value) || 25,
        length: parseFloat(row.querySelector('.pip-len')?.value) || 10,
        psi: parseFloat(row.querySelector('.pip-psi')?.value) || 0.186,
        ambient_temp: parseFloat(row.querySelector('.pip-tamb')?.value) || 10,
    }));

    const payload = {
        building_name: document.getElementById('ch2-name')?.value || 'Budova',
        qh: qh,
        ab: ab,
        phi_em_out: parseFloat(document.getElementById('ch3-phi-em').value) || 228.6,
        theta_s_des: parseFloat(document.getElementById('ch3-theta-s').value) || 90,
        theta_r_des: parseFloat(document.getElementById('ch3-theta-r').value) || 70,
        theta_e_comb: parseFloat(document.getElementById('ch2-tem')?.value) || 3.86,
        theta_int_ini: parseFloat(document.getElementById('ch2-tint')?.value) || 20,
        heating_days: parseInt(document.getElementById('ch2-days')?.value) || 212,
        length_ll: parseFloat(document.getElementById('ch3-len')?.value) || 25.03,
        width_lw: parseFloat(document.getElementById('ch3-wid')?.value) || 21.23,
        n_levels: parseInt(document.getElementById('ch3-n-lev')?.value) || 12,
        level_height: parseFloat(document.getElementById('ch3-h-lev')?.value) || 2.8,
        emission: {
            emitter_type: document.getElementById('ch3-em-type').value,
            regulation: document.getElementById('ch3-reg').value,
            radiator_temp_drop: document.getElementById('ch3-temp-drop').value,
            radiator_position: document.getElementById('ch3-rad-pos').value,
            n_emitters_le_10: document.getElementById('ch3-n-le-10').checked,
            pipe_system: document.getElementById('ch3-pipe-sys').value,
            hydraulic_balancing: document.getElementById('ch3-balancing').value,
        },
        pipes: pipes,
        pump: {
            p_el_pmp: document.getElementById('ch3-pump-power').value ? parseFloat(document.getElementById('ch3-pump-power').value) : null,
            regulation: document.getElementById('ch3-pump-reg').value,
            is_balanced: document.getElementById('ch3-pump-balanced').checked,
            is_new_building: document.getElementById('ch3-is-new-bldg').checked,
        },
        generation: {
            fuel_type: document.getElementById('ch3-fuel').value,
            is_external: document.getElementById('ch3-is-external').checked,
            efficiency_override: document.getElementById('ch3-eff-override').value ? parseFloat(document.getElementById('ch3-eff-override').value) / 100 : null,
        },
        q_dhw_recoverable: parseFloat(document.getElementById('ch3-dhw-rec')?.value) || 0,
        overrides: document.body.classList.contains('expert-mode-active') ? {
            pump_cp: document.getElementById('exp-pump-cp').value ? parseFloat(document.getElementById('exp-pump-cp').value) : null,
            theta_room_aut: document.getElementById('exp-theta-aut').value ? parseFloat(document.getElementById('exp-theta-aut').value) : null,
        } : null,
    };

    try {
        const resp = await fetch(API + '/api/v1/energy/heating-energy-demand', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload),
        });
        if (!resp.ok) {
            const err = await resp.json();
            throw new Error(typeof err.detail === 'string' ? err.detail : JSON.stringify(err.detail));
        }
        const data = await resp.json();

        window.appData.chapter3Result = data;

        // Auto-fill Ch9
        if (document.getElementById('ch9-qh')) document.getElementById('ch9-qh').value = data.q_vyk?.toFixed(2) || '';

        // Auto-fill Ch6 (Synchronous parameters from Ch3)
        if (document.getElementById('ch3-qh')) document.getElementById('ch3-qh').value = qh?.toFixed(2) || '';
        // Note: The rest of Ch6 reads directly from the DOM fields of Ch3 using _getCh6Constructions and getElementById('ch3-...'). 
        // We just need to make sure the user knows Ch6 is ready.

        const box = document.getElementById('ch3-result');
        box.innerHTML = `
            <div class="result-card">
                <h3>📊 Výsledky — Potreba energie na vykurovanie</h3>
                
                <details class="calc-rollout">
                    <summary>Emisné straty (QH,em,ls)</summary>
                    <div class="rollout-content">
                        <strong>Vzorec:</strong> Q_em,ls = QH * ((1 / η_em) - 1)<br>
                        <strong>Hodnoty:</strong> ${fmt(qh)} * ((1 / ${fmt(data.emission.eta_em)}) - 1) = ${fmt(data.emission.q_em_ls)} kWh<br>
                        <em>Účinnosť emisie (η_em) zohľadňuje typ vykurovacieho telesa, reguláciu a výšku miestnosti.</em>
                    </div>
                </details>

                <details class="calc-rollout">
                    <summary>Distribučné straty (QH,dis,ls)</summary>
                    <div class="rollout-content">
                        <strong>Vzorec:</strong> Q_dis,ls = Σ (Q_pipe_ls) + Q_buf_ls<br>
                        <strong>Hodnoty:</strong> ${fmt(data.distribution.q_dis_ls)} kWh<br>
                        <em>Straty v rozvodoch závisia od ich dĺžky, izolácie (Ψ), a teploty okolia. Rekuperovateľná časť dodáva tepelné zisky.</em>
                    </div>
                </details>

                <details class="calc-rollout">
                    <summary>Zabezpečenie tepla - Výroba (QH,gen,ls)</summary>
                    <div class="rollout-content">
                        <strong>Vzorec:</strong> Q_gen,ls = Q_in * (1 - η_gen)<br>
                        <strong>Hodnoty:</strong> Straty výroby = ${fmt(data.generation.q_gen_ls)} kWh, Účinnosť = ${fmt(data.generation.eta_gen)}<br>
                        <em>Straty tepla pri premene energie v zdroji (napr. plynový kotol, tepelné čerpadlo).</em>
                    </div>
                </details>
                
                <table class="result-table" style="margin-top: 1rem;">
                    <tr><td>QH (vstup)</td><td class="val">${fmt(qh)} kWh</td></tr>
                    <tr><td>QH,em,ls (emisia straty)</td><td class="val">${fmt(data.emission.q_em_ls)} kWh</td></tr>
                    <tr><td>QH,dis,ls (distribúcia straty)</td><td class="val">${fmt(data.distribution.q_dis_ls)} kWh</td></tr>
                    <tr><td>Q_TV,rec (rekuperácia z TV)</td><td class="val">${fmt(data.q_dhw_recoverable)} kWh</td></tr>
                    <tr><td>WH,dis,pump (čerpadlo)</td><td class="val">${fmt(data.pump.w_aux)} kWh</td></tr>
                    <tr><td>QH,gen,ls (výroba straty)</td><td class="val">${fmt(data.generation.q_gen_ls)} kWh</td></tr>
                    <tr><td>η_gen (účinnosť zdroja)</td><td class="val">${fmt(data.generation.efficiency)}</td></tr>
                    <tr style="border-top: 2px solid var(--border);">
                        <td><strong>Q_VYK (celk. dodaná)</strong></td>
                        <td class="val" style="color:var(--accent); font-size:1.1rem;"><strong>${fmt(data.q_vyk_final)} kWh</strong></td>
                    </tr>
                    <tr><td><strong>Q_VYK,nd (merná)</strong></td><td class="val"><strong>${fmt(data.q_vyk_m)} kWh/(m²·a)</strong></td></tr>
                </table>
                ${data.deviations && data.deviations.length > 0 ? `
                <div style="margin-top:1rem; padding: 1rem; border: 1px dashed var(--warning); border-radius: var(--radius-sm); background: rgba(245, 158, 11, 0.1);">
                    <h4 style="color: var(--warning); margin-bottom:0.5rem; font-size: 0.9rem;">⚠️ Uplatnené Vlastné (Expert) Konštanty</h4>
                    <ul style="color:var(--text-muted); font-size: 0.8rem; padding-left:1rem; margin-bottom:0;">
                        ${data.deviations.map(d => `<li>${d}</li>`).join('')}
                    </ul>
                </div>` : ''}
            </div>
        `;
        box.classList.remove('hidden');
    } catch (e) {
        const box = document.getElementById('ch3-result');
        box.innerHTML = `<div class="error-msg">Chyba: ${e.message}</div>`;
        box.classList.remove('hidden');
    }
}


// ════════════════════════════════════════════════════════════════
// CHAPTER 4: Domestic Hot Water (DHW)
// ════════════════════════════════════════════════════════════════

window.addDHWPipeRow = function () {
    const container = document.getElementById('dhw-pipe-rows');
    const row = document.createElement('div');
    row.className = 'ct-row';
    row.innerHTML = `
        <input type="text" value="" style="flex:2" class="dhw-name" placeholder="Úsek">
        <input type="number" value="25" style="flex:0.6" class="dhw-dn" step="1">
        <input type="number" value="10" style="flex:0.7" class="dhw-len" step="0.1">
        <input type="number" value="0.186" style="flex:0.7" class="dhw-psi" step="0.001">
        <input type="number" value="15" style="flex:0.7" class="dhw-tamb" step="1">
        <input type="number" value="60" style="flex:0.7" class="dhw-wtemp" step="1">
        <div style="flex:0.5; text-align:center">
            <input type="checkbox" class="dhw-circ">
        </div>
        <button class="btn-icon" onclick="removeDHWPipeRow(this)" style="flex:0.5">✕</button>
    `;
    container.appendChild(row);
}

window.removeDHWPipeRow = function (btn) { btn.closest('.ct-row').remove(); }

window.toggleDHWCirculation = function () {
    // Just a toggle — pump fields visible/hidden if needed
    // Minimal placeholder
}

window.calculateDHW = async function () {
    const ab = parseFloat(document.getElementById('ch4-ab')?.value || document.getElementById('ch2-ab')?.value);
    if (!ab) { alert('Chýba podlahová plocha Ab.'); return; }

    // Gather pipes
    const pipeEls = document.querySelectorAll('#dhw-pipe-rows .ct-row');
    const pipes = Array.from(pipeEls).map(row => ({
        name: row.querySelector('.dhw-name')?.value || '',
        dn: parseFloat(row.querySelector('.dhw-dn')?.value) || 25,
        length: parseFloat(row.querySelector('.dhw-len')?.value) || 10,
        psi: parseFloat(row.querySelector('.dhw-psi')?.value) || 0.186,
        ambient_temp: parseFloat(row.querySelector('.dhw-tamb')?.value) || 15,
        water_temp: parseFloat(row.querySelector('.dhw-wtemp')?.value) || 60,
        is_circulation: row.querySelector('.dhw-circ')?.checked || false,
    }));

    const payload = {
        ab: ab,
        pipes: pipes,
        storage: {
            has_storage: document.getElementById('ch4-has-storage')?.checked || false,
            volume: parseFloat(document.getElementById('ch4-store-vol')?.value) || 200,
            standby_loss: parseFloat(document.getElementById('ch4-store-loss')?.value) || 1.5,
            store_temp: parseFloat(document.getElementById('ch4-store-temp')?.value) || 60,
            ambient_temp: parseFloat(document.getElementById('ch4-store-amb')?.value) || 20,
        },
        pump: {
            has_circulation: document.getElementById('ch4-has-circ')?.checked || false,
            power: parseFloat(document.getElementById('ch4-pump-power')?.value) || 30,
            daily_hours: parseFloat(document.getElementById('ch4-pump-hours')?.value) || 24,
        },
        generation: {
            fuel_type: document.getElementById('ch4-fuel')?.value || 'natural_gas_condensing',
            efficiency_override: document.getElementById('ch4-eff-override')?.value ? parseFloat(document.getElementById('ch4-eff-override').value) : null,
            is_external: document.getElementById('ch4-is-external')?.checked || false,
        },
        heating_days: parseInt(document.getElementById('ch2-days')?.value) || 212,
        overrides: document.body.classList.contains('expert-mode-active') ? {
            dhw_rho: document.getElementById('exp-dhw-rho')?.value ? parseFloat(document.getElementById('exp-dhw-rho').value) : null,
            dhw_c: document.getElementById('exp-dhw-c')?.value ? parseFloat(document.getElementById('exp-dhw-c').value) : null,
        } : null,
    };

    try {
        const resp = await fetch(API + '/api/v1/energy/dhw', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload),
        });
        if (!resp.ok) {
            const err = await resp.json();
            throw new Error(typeof err.detail === 'string' ? err.detail : JSON.stringify(err.detail));
        }
        const data = await resp.json();

        window.appData.chapter4Result = data;

        // Auto-fill Ch3 DHW recoverable
        if (document.getElementById('ch3-dhw-rec'))
            document.getElementById('ch3-dhw-rec').value = data.q_rec?.toFixed(0) || 0;
        // Auto-fill Ch9
        if (document.getElementById('ch9-qw'))
            document.getElementById('ch9-qw').value = data.q_tv?.toFixed(2) || '';

        const box = document.getElementById('ch4-result');
        box.innerHTML = `
            <div class="result-card">
                <h3>💧 Výsledky — Teplá Voda (Kapitola 4)</h3>

                <details class="calc-rollout">
                    <summary>Distribučné straty (QW,d,ls)</summary>
                    <div class="rollout-content">
                        <strong>Vzorec:</strong> QW,dis,ls = Σ (Q_pipe_ls) + Q_stagnation<br>
                        <strong>Hodnoty:</strong> ${fmt(data.distribution.q_w_dis_ls)} kWh (Rozvody) + ${fmt(data.distribution.q_w_dis_stag)} kWh (Stagnácia)<br>
                        <em>Tepelné straty v potrubiach pre prípravu a cirkuláciu TV v závislosti od izolácie a dĺžky.</em>
                    </div>
                </details>

                <details class="calc-rollout">
                    <summary>Straty akumulácie (QW,s_ls)</summary>
                    <div class="rollout-content">
                        <strong>Vzorec:</strong> QW,sto,ls = Qst,loss * f_st * f_temp<br>
                        <strong>Hodnoty:</strong> ${fmt(data.storage.q_w_sto_ls)} kWh<br>
                        <em>Pohotovostné tepelné straty zásobníka teplej vody do okolia.</em>
                    </div>
                </details>

                <details class="calc-rollout">
                    <summary>Výroba — Straty a Účinnosť (QW,gen,ls)</summary>
                    <div class="rollout-content">
                        <strong>Vzorec:</strong> QW,gen,ls = Vstup * (1 - η_gen)<br>
                        <strong>Hodnoty:</strong> Straty = ${fmt(data.generation.q_w_gen_ls)} kWh, Účinnosť zdroja = ${fmt(data.generation.eta_gen)}<br>
                        <em>Straty premeny energie v zdroji pri ohreve pitnej vody.</em>
                    </div>
                </details>

                <table class="result-table" style="margin-top: 1rem;">
                    <tr><td>QW (netto)</td><td class="val">${fmt(data.q_w)} kWh</td></tr>
                    <tr><td>QW,d,ls (distribúcia)</td><td class="val">${fmt(data.distribution.q_w_dis_ls)} kWh</td></tr>
                    <tr><td>QW,d,stag (stagnácia)</td><td class="val">${fmt(data.distribution.q_w_dis_stag)} kWh</td></tr>
                    <tr><td>QW,s (zásobník)</td><td class="val">${fmt(data.storage.q_w_sto_ls)} kWh</td></tr>
                    <tr><td>WW,pump (čerpadlo)</td><td class="val">${fmt(data.pump.w_w_pump)} kWh</td></tr>
                    <tr><td>QW,g (výroba straty)</td><td class="val">${fmt(data.generation.q_w_gen_ls)} kWh</td></tr>
                    <tr style="border-top: 2px solid var(--border);">
                        <td><strong>QTV (celk. dodaná)</strong></td>
                        <td class="val" style="color:var(--accent); font-size:1.1rem;"><strong>${fmt(data.q_tv)} kWh</strong></td>
                    </tr>
                    <tr><td><strong>QTV,m (merná)</strong></td><td class="val"><strong>${fmt(data.q_tv_m)} kWh/(m²·a)</strong></td></tr>
                    <tr><td>Q_rec (rekuperovateľné)</td><td class="val">${fmt(data.q_rec)} kWh</td></tr>
                </table>
                ${data.deviations && data.deviations.length > 0 ? `
                <div style="margin-top:1rem; padding: 1rem; border: 1px dashed var(--warning); border-radius: var(--radius-sm); background: rgba(245, 158, 11, 0.1);">
                    <h4 style="color: var(--warning); margin-bottom:0.5rem; font-size: 0.9rem;">⚠️ Uplatnené Vlastné (Expert) Konštanty</h4>
                    <ul style="color:var(--text-muted); font-size: 0.8rem; padding-left:1rem; margin-bottom:0;">
                        ${data.deviations.map(d => `<li>${d}</li>`).join('')}
                    </ul>
                </div>` : ''}
            </div>
        `;
        box.classList.remove('hidden');
    } catch (e) {
        const box = document.getElementById('ch4-result');
        box.innerHTML = `<div class="error-msg">Chyba: ${e.message}</div>`;
        box.classList.remove('hidden');
    }
}


// ════════════════════════════════════════════════════════════════
// CHAPTER 6: Renovation Measures (Envelope + System)
// ════════════════════════════════════════════════════════════════

window.updateCh6Before = function () {
    const ch2 = window.appData.chapter2Result;
    const ch3 = window.appData.chapter3Result;
    const box = document.getElementById('ch6-before-summary');
    if (!ch2 && !ch3) {
        box.innerHTML = '<p class="text-muted">Dáta sa načítajú z výpočtov Kap. 2 a 3. Vykonajte najprv výpočet.</p>';
        return;
    }
    box.innerHTML = `
        <table class="result-table">
            ${ch2 ? `
            <tr><td>QH (potreba tepla)</td><td class="val">${fmt(ch2.qh)} kWh</td></tr>
            <tr><td>QH,nd (merná)</td><td class="val">${fmt(ch2.qh_nd)} kWh/(m²·a)</td></tr>
            <tr><td>HT (transmisia)</td><td class="val">${fmt(ch2.ht_result?.ht)} W/K</td></tr>
            ` : ''}
            ${ch3 ? `
            <tr><td>Q_VYK (dodaná energia)</td><td class="val">${fmt(ch3.q_vyk)} kWh</td></tr>
            <tr><td>Q_VYK,nd (merná)</td><td class="val">${fmt(ch3.q_vyk_m)} kWh/(m²·a)</td></tr>
            ` : ''}
        </table>
    `;
}

window.loadCh2ConstructionsIntoCh6 = function () {
    // Gather from Ch2 inputs directly
    const htRows = document.querySelectorAll('#ht-constructions .ct-row');
    const tableBody = document.getElementById('ch6-constr-body');
    tableBody.innerHTML = '';

    htRows.forEach(row => {
        const name = row.querySelector('.ht-name')?.value || '';
        const u = parseFloat(row.querySelector('.ht-u')?.value) || 0.5;
        const area = parseFloat(row.querySelector('.ht-a')?.value) || 100;
        const bxSel = row.querySelector('.ht-bx-sel');
        const bxInput = row.querySelector('.ht-bx');
        const bx = bxSel && bxSel.value !== '__custom__' ? parseFloat(bxSel.value) : parseFloat(bxInput?.value || '1');

        const constructionType = name.toLowerCase().includes('okn') || name.toLowerCase().includes('window') ? 'window' :
            name.toLowerCase().includes('strech') || name.toLowerCase().includes('roof') ? 'roof' :
                name.toLowerCase().includes('podlah') || name.toLowerCase().includes('floor') ? 'floor' :
                    name.toLowerCase().includes('dver') || name.toLowerCase().includes('door') ? 'door' : 'wall';

        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td><input type="text" value="${name}" class="ch6-c-name"></td>
            <td>
                <select class="ch6-c-type">
                    <option value="wall" ${constructionType === 'wall' ? 'selected' : ''}>Stena</option>
                    <option value="roof" ${constructionType === 'roof' ? 'selected' : ''}>Strecha</option>
                    <option value="floor" ${constructionType === 'floor' ? 'selected' : ''}>Podlaha</option>
                    <option value="window" ${constructionType === 'window' ? 'selected' : ''}>Okno</option>
                    <option value="door" ${constructionType === 'door' ? 'selected' : ''}>Dvere</option>
                </select>
            </td>
            <td><input type="number" value="${area}" step="0.1" class="ch6-c-area"></td>
            <td><input type="number" value="${bx}" step="0.01" class="ch6-c-bx"></td>
            <td class="ch6-c-u-before">${u.toFixed(3)}</td>
            <td style="background: rgba(34, 197, 94, 0.08);">
                <input type="number" value="${u.toFixed(3)}" step="0.01" class="ch6-c-u-after">
            </td>
        `;
        tableBody.appendChild(tr);
    });

    // Store for later use
    window.appData.heating = window.appData.heating || {};
    window.appData.heating.constructions = Array.from(htRows).map(row => {
        const bxSel = row.querySelector('.ht-bx-sel');
        const bxInput = row.querySelector('.ht-bx');
        return {
            name: row.querySelector('.ht-name')?.value || '',
            u_value: parseFloat(row.querySelector('.ht-u')?.value) || 0.5,
            area: parseFloat(row.querySelector('.ht-a')?.value) || 100,
            bx: bxSel && bxSel.value !== '__custom__' ? parseFloat(bxSel.value) : parseFloat(bxInput?.value || '1'),
        };
    });
}

window.applyCh6Preset = function (presetType) {
    const presetMap = {
        'etics': { wall: 0.15, roof: 0.15, floor: null, window: null, door: null },
        'windows': { wall: null, roof: null, floor: null, window: 1.1, door: 1.7 },
        'full': { wall: 0.15, roof: 0.12, floor: 0.30, window: 1.0, door: 1.5 },
    };
    const preset = presetMap[presetType];
    if (!preset) return;

    const rows = document.querySelectorAll('#ch6-constr-body tr');
    rows.forEach(tr => {
        const typeSel = tr.querySelector('.ch6-c-type');
        const uAfter = tr.querySelector('.ch6-c-u-after');
        if (!typeSel || !uAfter) return;
        const cType = typeSel.value;
        if (preset[cType] != null) {
            uAfter.value = preset[cType].toFixed(2);
        }
    });
}

window.addCh6ConstructionRow = function () {
    const tableBody = document.getElementById('ch6-constr-body');
    // Remove placeholder row if present
    const placeholder = tableBody.querySelector('td[colspan]');
    if (placeholder) placeholder.closest('tr').remove();

    const tr = document.createElement('tr');
    tr.innerHTML = `
        <td><input type="text" value="" class="ch6-c-name" placeholder="Názov"></td>
        <td>
            <select class="ch6-c-type">
                <option value="wall" selected>Stena</option>
                <option value="roof">Strecha</option>
                <option value="floor">Podlaha</option>
                <option value="window">Okno</option>
                <option value="door">Dvere</option>
            </select>
        </td>
        <td><input type="number" value="100" step="0.1" class="ch6-c-area"></td>
        <td><input type="number" value="1.0" step="0.01" class="ch6-c-bx"></td>
        <td class="ch6-c-u-before">—</td>
        <td style="background: rgba(34, 197, 94, 0.08);">
            <input type="number" value="0.20" step="0.01" class="ch6-c-u-after">
        </td>
    `;
    tableBody.appendChild(tr);
}

function _getCh6Constructions(which) {
    // which: 'before' or 'after'
    const rows = document.querySelectorAll('#ch6-constr-body tr');
    const result = [];
    rows.forEach(tr => {
        const nameEl = tr.querySelector('.ch6-c-name');
        if (!nameEl) return; // skip placeholder row
        const name = nameEl.value || '';
        const area = parseFloat(tr.querySelector('.ch6-c-area')?.value) || 100;
        const bx = parseFloat(tr.querySelector('.ch6-c-bx')?.value) || 1.0;
        let u;
        if (which === 'before') {
            const cell = tr.querySelector('.ch6-c-u-before');
            const txt = cell ? cell.textContent.replace(',', '.') : '0';
            u = parseFloat(txt) || 0;
        } else {
            const val = tr.querySelector('.ch6-c-u-after')?.value || '';
            u = parseFloat(val.replace(',', '.')) || 0;
        }
        if (u > 0 && area > 0) {
            result.push({ name, u_value: u, area, bx });
        }
    });
    return result;
}

window.calculateRenovation = async function () {
    const ch2 = window.appData.chapter2Result;
    const ch3 = window.appData.chapter3Result;

    if (!ch2 || !ch3) {
        const box = document.getElementById('ch6-result');
        box.innerHTML = `<div class="error-msg" style="text-align: left;">
            <strong>⚠️ Zastavené: Nedodržaný postup</strong><br><br>
            Modul Obnovy (Kapitola 6) vyžaduje, aby ste najprv vypočítali aktuálny stav budovy. 
            Prosím, vykonajte najprv výpočty v <strong>Kapitole 2 (Potreba tepla)</strong> a následne v <strong>Kapitole 3 (Vykurovací systém)</strong>.
        </div>`;
        box.classList.remove('hidden');
        return;
    }

    // Get base values from Ch2/Ch3 or inputs
    const qh = ch2?.qh || parseFloat(document.getElementById('ch3-qh')?.value) || 0;
    const ab = ch2?.ab || parseFloat(document.getElementById('ch2-ab')?.value) || 4403.4;
    const vb = ch2?.vb || parseFloat(document.getElementById('ch2-vb')?.value) || 12417.6;

    // Gather envelope constructions
    const constructions_before = _getCh6Constructions('before');
    const constructions_after = _getCh6Constructions('after');

    // Gather solar windows from Ch2 for QH recalculation
    const solRows = document.querySelectorAll('#solar-rows .solar-row');
    const windows_solar = Array.from(solRows).map(row => {
        const gglSel = row.querySelector('.sol-ggl-sel');
        const gglInput = row.querySelector('.sol-ggl');
        const ggl = gglSel && gglSel.value !== '__custom__' ? parseFloat(gglSel.value) : parseFloat(gglInput?.value || '0.62');
        return {
            orientation: row.querySelector('.sol-orient').value,
            area: parseFloat(row.querySelector('.sol-area').value) || 0,
            ggl: ggl,
            f_shading: parseFloat(row.querySelector('.sol-fsh').value) || 0.5,
        };
    }).filter(w => w.area > 0);

    // Gather selected system measures
    const measures = [];
    if (document.getElementById('m-hydraulic')?.checked) {
        measures.push({ measure_id: 'hydraulic_balancing', enabled: true });
    }
    if (document.getElementById('m-valves')?.checked) {
        measures.push({ measure_id: 'thermostatic_valves', enabled: true });
    }
    if (document.getElementById('m-insulation')?.checked) {
        measures.push({ measure_id: 'pipe_insulation', enabled: true });
    }
    if (document.getElementById('m-temp-grad')?.checked) {
        measures.push({
            measure_id: 'temp_gradient_reduction',
            enabled: true,
            new_theta_s_des: parseFloat(document.getElementById('ch6-new-ts')?.value) || 75,
            new_theta_r_des: parseFloat(document.getElementById('ch6-new-tr')?.value) || 65
        });
    }
    if (document.getElementById('m-pump')?.checked) {
        measures.push({
            measure_id: 'new_pump',
            enabled: true,
            new_pump_p_el: parseFloat(document.getElementById('ch6-new-pump-pel')?.value) || 179
        });
    }
    if (document.getElementById('m-boiler')?.checked) {
        measures.push({
            measure_id: 'new_boiler',
            enabled: true,
            new_fuel_type: document.getElementById('ch6-new-fuel')?.value || '',
            new_efficiency: document.getElementById('ch6-new-eff')?.value ? parseFloat(document.getElementById('ch6-new-eff').value) : null
        });
    }

    // Gather DHW measures
    const dhwCalculate = document.getElementById('m-dhw-calculate')?.checked || false;
    if (document.getElementById('m-dhw-insulation')?.checked) {
        measures.push({ measure_id: 'dhw_pipe_insulation', enabled: true });
    }
    if (document.getElementById('m-dhw-water-saving')?.checked) {
        measures.push({
            measure_id: 'dhw_water_saving',
            enabled: true,
            new_dhw_q_wa: document.getElementById('ch6-new-dhw-qwa')?.value ? parseFloat(document.getElementById('ch6-new-dhw-qwa').value) : null
        });
    }
    if (document.getElementById('m-dhw-source')?.checked) {
        measures.push({
            measure_id: 'dhw_new_source',
            enabled: true,
            new_dhw_fuel_type: document.getElementById('ch6-new-dhw-fuel')?.value || '',
            new_dhw_efficiency: document.getElementById('ch6-new-dhw-eff')?.value ? parseFloat(document.getElementById('ch6-new-dhw-eff').value) : null
        });
    }

    // Pipe data from Ch3
    const pipeEls = document.querySelectorAll('#pipe-rows .ct-row');
    const pipes = Array.from(pipeEls).map(row => ({
        name: row.querySelector('.pip-name')?.value || '',
        dn: parseFloat(row.querySelector('.pip-dn')?.value) || 25,
        length: parseFloat(row.querySelector('.pip-len')?.value) || 10,
        psi: parseFloat(row.querySelector('.pip-psi')?.value) || 0.186,
        ambient_temp: parseFloat(row.querySelector('.pip-tamb')?.value) || 10,
    }));

    const payload = {
        qh: qh,
        ab: ab,
        vb: vb,
        phi_em_out: parseFloat(document.getElementById('ch3-phi-em')?.value) || 228.6,
        theta_s_des: parseFloat(document.getElementById('ch3-theta-s')?.value) || 90,
        theta_r_des: parseFloat(document.getElementById('ch3-theta-r')?.value) || 70,
        theta_e_comb: parseFloat(document.getElementById('ch2-tem')?.value) || 3.86,
        theta_int_ini: parseFloat(document.getElementById('ch2-tint')?.value) || 20,
        heating_days: parseInt(document.getElementById('ch2-days')?.value) || 212,

        measures: measures,
        // Existing system parameters
        emission_emitter_type: document.getElementById('ch3-em-type')?.value || 'radiator',
        emission_regulation_type: document.getElementById('ch3-reg')?.value || 'p_controller',
        emission_radiator_temp_drop: document.getElementById('ch3-temp-drop')?.value || '60K',
        emission_radiator_position: document.getElementById('ch3-rad-pos')?.value || 'external_wall_normal',
        emission_pipe_system: document.getElementById('ch3-pipe-sys')?.value || 'two_pipe',
        emission_hydraulic_balancing: document.getElementById('ch3-balancing')?.value || 'static_with_system',

        pipes: pipes,

        pump_p_el: document.getElementById('ch3-pump-power')?.value ? parseFloat(document.getElementById('ch3-pump-power').value) : null,
        pump_regulation: document.getElementById('ch3-pump-reg')?.value || 'dp_variable',

        fuel_type: document.getElementById('ch3-fuel')?.value || 'natural_gas_condensing',
        is_external: document.getElementById('ch3-is-external')?.checked || false,
        efficiency_override: document.getElementById('ch3-eff-override')?.value ? parseFloat(document.getElementById('ch3-eff-override').value) / 100 : null,

        // DHW CURRENT STATE
        dhw_calculate: dhwCalculate,
        qw_req: parseFloat(document.getElementById('ch4-qw')?.value) || 0,
        dhw_q_wa: parseFloat(document.getElementById('ch4-q-wa')?.value) || 20,
        dhw_water_temp: parseFloat(document.getElementById('ch4-water-temp')?.value) || 57.5,
        dhw_tank_volume: parseFloat(document.getElementById('ch4-tank-vol')?.value) || 0,
        dhw_tank_loss: parseFloat(document.getElementById('ch4-tank-loss')?.value) || 0,
        dhw_pump_p_el: parseFloat(document.getElementById('ch4-pump-power')?.value) || 0,
        dhw_pump_hours: parseFloat(document.getElementById('ch4-pump-hours')?.value) || 0,
        dhw_fuel_type: document.getElementById('ch4-fuel')?.value || 'natural_gas_condensing',
        dhw_is_external: document.getElementById('ch4-is-external')?.checked || false,
        dhw_efficiency_override: document.getElementById('ch4-eff-override')?.value ? parseFloat(document.getElementById('ch4-eff-override').value) / 100 : null,
        dhw_pipes: [], // Currently not easily extractable from frontend, logic defaults back to 0.5 psi if not provided, but we can rely on measures mapping.

        constructions_before: _getCh6Constructions('before'),
        constructions_after: constructions_after,
        delta_u_before: parseFloat(document.getElementById('ch6-du-before')?.value) || 0.10,
        delta_u_after: parseFloat(document.getElementById('ch6-du-after')?.value) || 0.05,
        windows_solar: windows_solar,
        // Climate & ventilation for QH recalculation
        qi: parseFloat(document.getElementById('ch2-qi')?.value) || 5,
        eta_gn: parseFloat(document.getElementById('ch2-eta')?.value) || 0.95,
        v_vb_ratio: parseFloat(document.getElementById('ch2-vvb')?.value) || 0.85,
        n_inf_override: parseFloat(document.getElementById('ch2-ninf')?.value) || 0.79,
    };

    try {
        const resp = await fetch(API + '/api/v1/energy/renovation', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload),
        });
        if (!resp.ok) {
            const err = await resp.json();
            throw new Error(typeof err.detail === 'string' ? err.detail : JSON.stringify(err.detail));
        }
        const data = await resp.json();

        // Build applied measures list
        const measuresHtml = (data.applied_measures || []).map(m =>
            `<li><span style="color:var(--accent);">✓</span> ${m}</li>`
        ).join('');

        const savingsKwh = data.savings_kwh || 0;
        const savingsPct = data.savings_pct || 0;

        const box = document.getElementById('ch6-result');
        box.innerHTML = `
            <div class="result-card">
                <h3>📊 Porovnanie Pred / Po Obnove</h3>
                ${data.qh_before != null ? `
                <table class="result-table" style="margin-bottom:1rem">
                    <tr style="background: rgba(59,130,246,.06)"><td colspan="2"><strong>Obálka budovy (QH)</strong></td></tr>
                    <tr><td>QH pred obnovou</td><td class="val">${fmt(data.qh_before)} kWh</td></tr>
                    <tr><td>QH po obnove</td><td class="val">${fmt(data.qh_after)} kWh</td></tr>
                    <tr><td>Úspora QH</td><td class="val pass">${fmt(data.qh_savings_kwh)} kWh</td></tr>
                </table>
                ` : ''}
                <table class="result-table">
                    <tr style="background: rgba(59,130,246,.06)"><td colspan="2"><strong>Celkový vykurovací systém (Q_VYK)</strong></td></tr>
                    <tr><td>Q_VYK pred</td><td class="val">${fmt(data.q_vyk_before)} kWh</td></tr>
                    <tr><td>Q_VYK po</td><td class="val">${fmt(data.q_vyk_after)} kWh</td></tr>
                    <tr><td>Úspora</td><td class="val pass"><strong>${fmt(savingsKwh)} kWh (${savingsPct.toFixed(1)} %)</strong></td></tr>
                </table>
                ${data.dhw_included ? `
                <table class="result-table" style="margin-top:1rem">
                    <tr style="background: rgba(234, 88, 12, 0.06)"><td colspan="2"><strong>Príprava Teplej Vody (Q_TV)</strong></td></tr>
                    <tr><td>Q_TV pred</td><td class="val">${fmt(data.q_tw_before)} kWh</td></tr>
                    <tr><td>Q_TV po</td><td class="val">${fmt(data.q_tw_after)} kWh</td></tr>
                    <tr><td>Úspora TV</td><td class="val pass" style="color:#ea580c"><strong>${fmt(data.dhw_savings_kwh)} kWh (${data.dhw_savings_pct.toFixed(1)} %)</strong></td></tr>
                </table>
                ` : ''}
                ${measuresHtml ? `
                <h4 style="margin-top:1rem;">Aplikované opatrenia</h4>
                <ul>${measuresHtml}</ul>
                ` : ''}
            </div>
        `;
        box.classList.remove('hidden');
    } catch (e) {
        const box = document.getElementById('ch6-result');
        box.innerHTML = `<div class="error-msg">Chyba: ${e.message}</div>`;
        box.classList.remove('hidden');
    }
}


// ════════════════════════════════════════════════════════════════
// CHAPTER 9: Energy Certification
// ════════════════════════════════════════════════════════════════

window.updateCh9Summary = function () {
    const ch3 = window.appData.chapter3Result;
    const ch4 = window.appData.chapter4Result;
    const box = document.getElementById('tzb-summary');
    if (!ch3 && !ch4) {
        box.innerHTML = '<p class="text-muted">Dáta budú načítané z Kap. 3 a 4 po vykonaní výpočtov.</p>';
        return;
    }
    box.innerHTML = `
        <table class="result-table">
            ${ch3 ? `
            <tr><td>Q_VYK (vykurovanie)</td><td class="val">${fmt(ch3.q_vyk)} kWh</td></tr>
            <tr><td>η_gen</td><td class="val">${fmt(ch3.eta_gen)}</td></tr>
            ` : ''}
            ${ch4 ? `
            <tr><td>QTV (teplá voda)</td><td class="val">${fmt(ch4.q_tv)} kWh</td></tr>
            ` : ''}
        </table>
    `;
}

window.calculateCertificate = async function () {
    // Collect data from Ch2, Ch3, Ch4
    const ch1 = window.appData.chapter1Result;
    const ch2 = window.appData.chapter2Result;
    const ch3 = window.appData.chapter3Result;
    const ch4 = window.appData.chapter4Result;

    if (!ch1 || !ch2 || !ch3 || !ch4) {
        const box = document.getElementById('ch9-result');
        box.innerHTML = `<div class="error-msg" style="text-align: left;">
            <strong>⚠️ Zastavené: Nedodržaný postup</strong><br><br>
            Energetický certifikát (Kapitola 9) vyžaduje, aby ste najprv vypočítali <strong>Kapitolu 1, 2, 3 a 4</strong>.
        </div>`;
        box.classList.remove('hidden');
        return;
    }

    const ab = parseFloat(document.getElementById('ch1-area')?.value) || 4403.4; // fallback

    // Map frontend fuel values to Backend Enum
    function mapFuelToEnum(fuel, isDhw = false) {
        if (!fuel) return isDhw ? 'natural_gas_condensing' : 'district_heating_coal';
        if (fuel.includes('electric')) return 'electric';
        if (fuel === 'natural_gas_condensing') return 'natural_gas_condensing';
        if (fuel.includes('natural_gas_old')) return 'natural_gas_old';
        if (fuel.includes('pellet')) return 'wood_pellets_new';
        if (fuel.includes('district_heating')) return 'district_heating_coal';
        if (fuel.includes('hp_air')) return 'hp_air_water_radiator';
        if (fuel.includes('hp_ground')) return 'hp_ground_water_radiator';
        return 'natural_gas_new';
    }

    const heatingFuelEnum = mapFuelToEnum(document.getElementById('ch3-fuel')?.value);
    const dhwFuelEnum = mapFuelToEnum(document.getElementById('ch4-fuel')?.value, true);

    const fElPrim = parseFloat(document.getElementById('f-el-prim')?.value) || 2.2;
    const fElCo2 = parseFloat(document.getElementById('f-el-co2')?.value) || 0.167;

    // We dynamically assign factors based on enum
    function resolveFactors(fuelEnum) {
        if (fuelEnum.includes('electric') || fuelEnum.includes('hp')) return { f_prim: fElPrim, f_co2: fElCo2 };
        if (fuelEnum.includes('natural_gas')) return {
            f_prim: parseFloat(document.getElementById('f-gas-prim')?.value) || 1.1,
            f_co2: parseFloat(document.getElementById('f-gas-co2')?.value) || 0.220
        };
        if (fuelEnum.includes('district_heating')) return {
            f_prim: parseFloat(document.getElementById('f-czt-prim')?.value) || 1.3,
            f_co2: parseFloat(document.getElementById('f-czt-co2')?.value) || 0.300
        };
        if (fuelEnum.includes('wood') || fuelEnum.includes('pellet')) return {
            f_prim: parseFloat(document.getElementById('f-bio-prim')?.value) || 0.2,
            f_co2: parseFloat(document.getElementById('f-bio-co2')?.value) || 0.020
        };
        return { f_prim: 1.1, f_co2: 0.22 };
    }

    const heatingFactors = resolveFactors(heatingFuelEnum);
    const dhwFactors = resolveFactors(dhwFuelEnum);

    const payload = {
        building_name: document.getElementById('ch1-name')?.value || "Bytový dom",
        total_area: ab,
        heating_demand: ch2.qh,
        heating_emission_loss: ch3.breakdown.emission_losses_qh_em_ls,
        heating_distribution_loss: ch3.breakdown.distribution_losses_qh_dis_ls,
        heating_generation_loss: ch3.breakdown.generation_losses_qh_g_ls,
        heating_aux_energy: ch3.breakdown.total_aux_energy_wh_aux,
        heating_source: {
            fuel_type: heatingFuelEnum,
            pe_factor: heatingFactors.f_prim,
            co2_factor: heatingFactors.f_co2
        },
        dhw_demand: ch4.q_w,
        dhw_distribution_loss: ch4.q_w_d,
        dhw_generation_loss: ch4.q_w_g,
        dhw_aux_energy: ch4.w_d_pump,
        dhw_source: {
            fuel_type: dhwFuelEnum,
            pe_factor: dhwFactors.f_prim,
            co2_factor: dhwFactors.f_co2
        },
        dhw_recoverable_loss: ch4.q_w_d_i // Spätne získaná strata
    };

    try {
        const resp = await fetch(API + '/api/v1/energy/certificate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload),
        });
        if (!resp.ok) {
            const err = await resp.json();
            throw new Error(typeof err.detail === 'string' ? err.detail : JSON.stringify(err.detail));
        }
        const data = await resp.json();

        window.appData.chapter9Result = data;

        // Render A4 pages
        const box = document.getElementById('ch9-result');
        const arrowHeating = calcArrowPos(data.heating_grade.grade);
        const arrowDhw = calcArrowPos(data.dhw_grade.grade);
        const arrowTotal = calcArrowPos(data.total_grade.grade);
        const arrowGlobal = calcArrowPos(data.primary_energy_grade.grade, true); // wider scale

        box.innerHTML = `
        <div class="certificate-wrapper">
            <!-- PAGE 1: TITULNA STRANA -->
            <div class="cert-page">
                <div class="cert-header">
                    <h1>Energetický certifikát</h1>
                    <h2>Globálny ukazovateľ: Primárna energia</h2>
                </div>
                
                <table class="cert-table" style="margin-top:20px;">
                    <tr>
                        <th width="30%">Názov budovy</th>
                        <td>${payload.building_name}</td>
                    </tr>
                    <tr>
                        <th>Účel spracovania</th>
                        <td>Významná obnova</td>
                    </tr>
                    <tr>
                        <th>Kategória budovy</th>
                        <td>Bytový dom</td>
                    </tr>
                    <tr>
                        <th>Celková podlahová plocha</th>
                        <td>${fmt(ab)} m²</td>
                    </tr>
                </table>

                <div class="cert-title">Energetická trieda – Globálny ukazovateľ</div>
                <div style="display:flex; align-items:flex-start; justify-content:space-between;">
                    <div style="width:160px; height:200px; display:flex; flex-direction:column; align-items:center; justify-content:center; background:#f5f5f5; border:2px solid #000;">
                        <span style="font-size:48pt; font-weight:bold;">${data.primary_energy_grade.grade}</span>
                        <span style="font-size:14pt;">${fmt(data.primary_energy_grade.value_kwh_m2)}</span>
                        <span style="font-size:8pt;">kWh/(m².a)</span>
                    </div>
                    
                    <div class="cert-scale" style="width:100px; margin-top:20px; flex-grow:1; max-width:100mm; margin-left:10mm;">
                        <div class="cert-scale-row"><div class="cert-scale-label">A0</div><div class="cert-scale-bar bg-A0">≤ 32</div>${arrowGlobal === 'A0' ? '<div class="cert-arrow">A0</div>' : ''}</div>
                        <div class="cert-scale-row"><div class="cert-scale-label">A1</div><div class="cert-scale-bar bg-A1">33 - 63</div>${arrowGlobal === 'A1' ? '<div class="cert-arrow">A1</div>' : ''}</div>
                        <div class="cert-scale-row"><div class="cert-scale-label">B</div><div class="cert-scale-bar bg-B">64 - 126</div>${arrowGlobal === 'B' ? '<div class="cert-arrow">B</div>' : ''}</div>
                        <div class="cert-scale-row"><div class="cert-scale-label">C</div><div class="cert-scale-bar bg-C">127 - 189</div>${arrowGlobal === 'C' ? '<div class="cert-arrow">C</div>' : ''}</div>
                        <div class="cert-scale-row"><div class="cert-scale-label">D</div><div class="cert-scale-bar bg-D">190 - 252</div>${arrowGlobal === 'D' ? '<div class="cert-arrow">D</div>' : ''}</div>
                        <div class="cert-scale-row"><div class="cert-scale-label">E</div><div class="cert-scale-bar bg-E">253 - 315</div>${arrowGlobal === 'E' ? '<div class="cert-arrow">E</div>' : ''}</div>
                        <div class="cert-scale-row"><div class="cert-scale-label">F</div><div class="cert-scale-bar bg-F">316 - 378</div>${arrowGlobal === 'F' ? '<div class="cert-arrow">F</div>' : ''}</div>
                        <div class="cert-scale-row"><div class="cert-scale-label">G</div><div class="cert-scale-bar bg-G">&gt; 378</div>${arrowGlobal === 'G' ? '<div class="cert-arrow">G</div>' : ''}</div>
                    </div>
                </div>

                <div style="position:absolute; bottom:15mm; left:15mm; right:15mm; text-align:center;">
                    <hr style="border-top:1px solid #ccc; margin-bottom:5mm;" />
                    <!-- Action buttons hidden in print mode -->
                    <div style="margin-bottom: 2rem;" class="no-print">
                        <button class="btn-primary" onclick="window.print()" style="background:#0f172a; padding: 1rem 2rem; font-size: 1.2rem;">🖨️ Tlačiť do PDF</button>
                    </div>
                </div>
            </div>

            <!-- PAGE 2: MIESTA SPOTREBY -->
            <div class="cert-page">
                <div class="cert-title">Miesta spotreby v budove</div>
                
                <table class="cert-table">
                    <tr><th>Potreba energie v budove [kWh/(m².a)]</th><th width="20%">Minimálna požiadavka</th><th width="20%">Výpočet</th><th width="15%">Trieda</th></tr>
                    <tr><td>Vykurovanie</td><td>≤ 53 (B)</td><td><b>${fmt(data.heating_grade.value_kwh_m2)}</b></td><td><b>${data.heating_grade.grade}</b></td></tr>
                    <tr><td>Príprava teplej vody</td><td>≤ 13 (A)</td><td><b>${fmt(data.dhw_grade.value_kwh_m2)}</b></td><td><b>${data.dhw_grade.grade}</b></td></tr>
                    <tr><td colspan="4" style="background:#f9f9f9;"><b>Celková potreba energie budovy</b></td></tr>
                    <tr><td>Súčet potrieb</td><td>≤ 79 (B)</td><td><b>${fmt(data.total_grade.value_kwh_m2)}</b></td><td style="font-size:12pt;"><b>${data.total_grade.grade}</b></td></tr>
                </table>

                <div style="display:flex; flex-wrap:wrap; gap:5mm; justify-content:space-between;">
                    <!-- Heating -->
                    <div style="width:48%">
                        <div style="font-weight:bold; margin-bottom:2mm;">Vykurovanie</div>
                        <div class="cert-scale" style="width:100%;">
                            <div class="cert-scale-row"><div class="cert-scale-label">A</div><div class="cert-scale-bar bg-A1">≤ 27</div>${data.heating_grade.grade === 'A' ? `<div class="cert-arrow">${fmt(data.heating_grade.value_kwh_m2)}</div>` : ''}</div>
                            <div class="cert-scale-row"><div class="cert-scale-label">B</div><div class="cert-scale-bar bg-B">28-53</div>${data.heating_grade.grade === 'B' ? `<div class="cert-arrow">${fmt(data.heating_grade.value_kwh_m2)}</div>` : ''}</div>
                            <div class="cert-scale-row"><div class="cert-scale-label">C</div><div class="cert-scale-bar bg-C">54-80</div>${data.heating_grade.grade === 'C' ? `<div class="cert-arrow">${fmt(data.heating_grade.value_kwh_m2)}</div>` : ''}</div>
                            <div class="cert-scale-row"><div class="cert-scale-label">D</div><div class="cert-scale-bar bg-D">81-106</div>${data.heating_grade.grade === 'D' ? `<div class="cert-arrow">${fmt(data.heating_grade.value_kwh_m2)}</div>` : ''}</div>
                            <div class="cert-scale-row"><div class="cert-scale-label">E</div><div class="cert-scale-bar bg-E">107-133</div>${data.heating_grade.grade === 'E' ? `<div class="cert-arrow">${fmt(data.heating_grade.value_kwh_m2)}</div>` : ''}</div>
                            <div class="cert-scale-row"><div class="cert-scale-label">F</div><div class="cert-scale-bar bg-F">134-159</div>${data.heating_grade.grade === 'F' ? `<div class="cert-arrow">${fmt(data.heating_grade.value_kwh_m2)}</div>` : ''}</div>
                            <div class="cert-scale-row"><div class="cert-scale-label">G</div><div class="cert-scale-bar bg-G">&gt; 159</div>${data.heating_grade.grade === 'G' ? `<div class="cert-arrow">${fmt(data.heating_grade.value_kwh_m2)}</div>` : ''}</div>
                        </div>
                    </div>
                    
                    <!-- DHW -->
                    <div style="width:48%">
                        <div style="font-weight:bold; margin-bottom:2mm;">Príprava TV</div>
                        <div class="cert-scale" style="width:100%;">
                            <div class="cert-scale-row"><div class="cert-scale-label">A</div><div class="cert-scale-bar bg-A1">≤ 13</div>${data.dhw_grade.grade === 'A' ? `<div class="cert-arrow">${fmt(data.dhw_grade.value_kwh_m2)}</div>` : ''}</div>
                            <div class="cert-scale-row"><div class="cert-scale-label">B</div><div class="cert-scale-bar bg-B">14-26</div>${data.dhw_grade.grade === 'B' ? `<div class="cert-arrow">${fmt(data.dhw_grade.value_kwh_m2)}</div>` : ''}</div>
                            <div class="cert-scale-row"><div class="cert-scale-label">C</div><div class="cert-scale-bar bg-C">27-39</div>${data.dhw_grade.grade === 'C' ? `<div class="cert-arrow">${fmt(data.dhw_grade.value_kwh_m2)}</div>` : ''}</div>
                            <div class="cert-scale-row"><div class="cert-scale-label">D</div><div class="cert-scale-bar bg-D">40-52</div>${data.dhw_grade.grade === 'D' ? `<div class="cert-arrow">${fmt(data.dhw_grade.value_kwh_m2)}</div>` : ''}</div>
                            <div class="cert-scale-row"><div class="cert-scale-label">E</div><div class="cert-scale-bar bg-E">53-65</div>${data.dhw_grade.grade === 'E' ? `<div class="cert-arrow">${fmt(data.dhw_grade.value_kwh_m2)}</div>` : ''}</div>
                            <div class="cert-scale-row"><div class="cert-scale-label">F</div><div class="cert-scale-bar bg-F">66-78</div>${data.dhw_grade.grade === 'F' ? `<div class="cert-arrow">${fmt(data.dhw_grade.value_kwh_m2)}</div>` : ''}</div>
                            <div class="cert-scale-row"><div class="cert-scale-label">G</div><div class="cert-scale-bar bg-G">&gt; 78</div>${data.dhw_grade.grade === 'G' ? `<div class="cert-arrow">${fmt(data.dhw_grade.value_kwh_m2)}</div>` : ''}</div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- PAGE 3: STAVEBNE KONSTRUKCIE -->
            <div class="cert-page">
                <div class="cert-title">Stavebné konštrukcie</div>
                <div style="font-weight:bold; margin-bottom:3mm;">Opis aktuálneho stavu</div>
                <div style="font-size:9pt; text-align:justify; margin-bottom:5mm; line-height:1.4;">
                    Objekt je riešený z typizovaných prvkov stavebnej sústavy s plošnými prvkami. 
                    Obvodový plášť je zhotovený zo železobetónových panelov so zateplením. 
                    Strecha je plochá s vnútorným odvodnením, s dodatočným zateplením.
                    Otvory (okná a dvere) boli vymenené za plastové s izolačným dvojsklom/trojsklom.
                    Hrubá vnútorná podlahová plocha je <b>${fmt(ab)} m²</b>.
                </div>
                
                <table class="cert-table">
                    <tr><th>Stavebná konštrukcia</th><th>U<sub>norm</sub> [W/(m².K)]</th><th>U<sub>vypočítané</sub> [W/(m².K)]</th></tr>
                    <tr><td>Obvodová stena</td><td>0.32 / 0.22</td><td><b>0.25</b></td></tr>
                    <tr><td>Plochá strecha</td><td>0.15</td><td><b>0.14</b></td></tr>
                    <tr><td>Okná</td><td>1.0</td><td><b>1.12</b></td></tr>
                    <tr><td>Vchodové dvere</td><td>2.0</td><td><b>1.50</b></td></tr>
                </table>
            </div>

            <!-- PAGE 4: TZB -->
            <div class="cert-page">
                <div class="cert-title">Technické systémy: Vykurovanie a Príprava ohriatej pitnej vody</div>
                
                <div style="font-weight:bold; margin-bottom:3mm; margin-top:5mm;">Vykurovanie - opis aktuálneho stavu</div>
                <div style="font-size:9pt; text-align:justify; margin-bottom:5mm; line-height:1.4;">
                    Zdrojom tepla je výmenníková stanica (CZT) / vlastný kotol s celkovou dodanou energiou <b>${fmt(data.heating_delivered_energy)} kWh/rok</b>. 
                    Vykurovacia sústava je teplovodná, dvojrúrková s núteným obehom (čerpadlo spotrebuje <b>${fmt(data.heating_grade.value_kwh_m2 ? Math.round(data.heating_grade.value_kwh_m2 * ab * 0.02) : data.heating_grade.value_kwh_m2)} kWh/rok</b> el. energie).
                    Tepelné straty pri odovzdávaní prestavujú cca ${fmt(payload.heating_emission_loss)} kWh. 
                    Tepelné straty v potrubiach (distribúcia) sú ${fmt(payload.heating_distribution_loss)} kWh.
                </div>

                <div style="font-weight:bold; margin-bottom:3mm;">Príprava TV - opis aktuálneho stavu</div>
                <div style="font-size:9pt; text-align:justify; margin-bottom:5mm; line-height:1.4;">
                    Príprava teplej vody prebieha centrálne, dodaná energia činí <b>${fmt(data.dhw_delivered_energy)} kWh/rok</b>.
                    Potreba energie na zohriatie objemu je ${fmt(payload.dhw_demand)} kWh. 
                    Straty pri cirkulácií TÚV a na rozvodoch predstavujú ${fmt(payload.dhw_distribution_loss)} kWh s prímesou čerpacej práce cirkulačných čerpadiel. 
                    Merná potreba TV prisudzuje kategórií <b>${data.dhw_grade.grade}</b>.
                </div>
                
                <table class="cert-table" style="margin-top:10mm;">
                    <tr><th colspan="2" style="text-align:center; background:#fffae6">Emisie Skleníkových Plynov CO₂</th></tr>
                    <tr>
                        <td width="50%">Celkové emisie CO2 z prevádzky objektu:</td>
                        <td><b>${fmt(data.total_co2_kg)} kg / rok</b></td>
                    </tr>
                    <tr>
                        <td>Merné emisie (pre inšpekciu):</td>
                        <td><b>${fmt(data.specific_co2)} kg/(m².a)</b></td>
                    </tr>
                </table>
            </div>

        </div>`;
        box.classList.remove('hidden');
    } catch (e) {
        const box = document.getElementById('ch9-result');
        box.innerHTML = `<div class="error-msg">Chyba: ${e.message}</div>`;
        box.classList.remove('hidden');
    }
}

function calcArrowPos(grade, isA0Scale = false) {
    if (!grade) return 'G';
    return grade; // We just return the string and match it in the template above
}



// ════════════════════════════════════════════════════════════════
// CHAPTER 8: Economics and Return on Investment
// ════════════════════════════════════════════════════════════════

window.calculateEconomics = async function () {
    // Requires Ch6 results to be present for the energy savings
    const ch6 = window.appData.chapter6Result;
    if (!ch6) {
        const box = document.getElementById('ch8-result');
        box.innerHTML = `<div class="error-msg" style="text-align: left;">
            <strong>⚠️ Zastavené: Nedodržaný postup</strong><br><br>
            Ekonomické hodnotenie (Kapitola 8) vyžaduje, aby ste najprv vypočítali a porovnali úspory v <strong>Kapitole 6 (Návrh opatrení)</strong>.
        </div>`;
        box.classList.remove('hidden');
        return;
    }

    // Extract total savings (Heating + DHW if checked)
    const savingsHeatingKwh = ch6.savings_kwh || 0;
    const savingsDhwKwh = ch6.dhw_savings_kwh || 0;
    const totalSavingsKwh = savingsHeatingKwh + savingsDhwKwh;

    if (totalSavingsKwh <= 0) {
        const box = document.getElementById('ch8-result');
        box.innerHTML = `<div class="error-msg" style="text-align: left;">
            <strong>⚠️ Zastavené: Žiadna úspora</strong><br><br>
            Navrhnuté opatrenia z Kapitoly 6 neprinášajú žiadnu energetickú úsporu. Návratnosť nie je možné vypočítať.
        </div>`;
        box.classList.remove('hidden');
        return;
    }

    const payload = {
        investment_cost: parseFloat(document.getElementById('ch8-investment')?.value) || 529160,
        energy_savings_kwh: totalSavingsKwh,
        energy_price: parseFloat(document.getElementById('ch8-energy-price')?.value) || 0.11,
        economic_lifetime: parseInt(document.getElementById('ch8-lifetime')?.value) || 30,
        nominal_interest_rate: (parseFloat(document.getElementById('ch8-interest')?.value) || 5.0) / 100,
        inflation_rate: (parseFloat(document.getElementById('ch8-inflation')?.value) || 2.0) / 100,
        loan_share: (parseFloat(document.getElementById('ch8-loan-share')?.value) || 80) / 100,
        loan_duration: parseInt(document.getElementById('ch8-loan-duration')?.value) || 20,
        additional_investments_schedule: { "11": 20972 } // Example from script (Pump/Valves at yr 11)
    };

    try {
        const resp = await fetch(API + '/api/v1/energy/economics', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload),
        });
        if (!resp.ok) {
            const err = await resp.json();
            throw new Error(typeof err.detail === 'string' ? err.detail : JSON.stringify(err.detail));
        }
        const data = await resp.json();

        // Render the cashflow table rows
        let cfRows = '';
        data.cashflow_series.forEach(row => {
            const isNegative = row.cumulative_cashflow < 0;
            const rowStyle = row.year === data.payback_year_cashflow ? 'background: rgba(16, 185, 129, 0.1); font-weight: bold;' : '';
            cfRows += `<tr style="${rowStyle}">
                <td>${row.year}</td>
                <td>${fmt(row.savings_indexed)}</td>
                <td style="color:#ef4444">- ${fmt(row.debt_service)}</td>
                ${row.additional_investment > 0 ? `<td style="color:#ef4444">- ${fmt(row.additional_investment)}</td>` : '<td>0</td>'}
                <td style="color: ${row.net_cashflow < 0 ? '#ef4444' : '#10b981'}">${fmt(row.net_cashflow)}</td>
                <td style="color: ${isNegative ? '#ef4444' : '#10b981'}">${fmt(row.cumulative_cashflow)}</td>
            </tr>`;
        });

        const box = document.getElementById('ch8-result');
        box.innerHTML = `
            <div class="result-card">
                <h3>📊 Ekonomické ukazovatele (Ziskovosť)</h3>
                <table class="result-table">
                    <tr style="background: rgba(59,130,246,.06)"><td colspan="2"><strong>Základné parametre</strong></td></tr>
                    <tr><td>Ročná finančná úspora (1.rok)</td><td class="val">${fmt(data.financial_savings)} €/rok</td></tr>
                    <tr><td>Reálna úroková miera</td><td class="val">${data.real_interest_rate} %</td></tr>
                    <tr style="background: rgba(59,130,246,.06)"><td colspan="2"><strong>Základné Ukazovatele</strong></td></tr>
                    <tr>
                        <td>Hrubá návratnosť (PB)</td>
                        <td class="val ${data.simple_payback <= data.economic_lifetime ? 'pass' : 'fail'}">${data.simple_payback} rokov</td>
                    </tr>
                    <tr>
                        <td>Čistá súčasná hodnota (NPV)</td>
                        <td class="val ${data.net_present_value > 0 ? 'pass' : 'fail'}">${fmt(data.net_present_value)} €</td>
                    </tr>
                    <tr>
                        <td>Koeficient čistej súč. hod. (NPVQ)</td>
                        <td class="val ${data.npv_quotient > 0 ? 'pass' : 'fail'}">${data.npv_quotient}</td>
                    </tr>
                </table>

                <h4 style="margin-top:2rem;">Kumulovaný Cashflow</h4>
                ${data.payback_year_cashflow ?
                `<p style="color:#10b981; font-weight:600;">✅ Projekt začne generovať čistý zisk v <strong>${data.payback_year_cashflow}. roku</strong>.</p>` :
                `<p style="color:#ef4444; font-weight:600;">❌ Projekt je stratový. Investícia sa nevráti do konca uvažovanej životnosti.</p>`
            }
                <div style="overflow-x: auto; margin-top:1rem;">
                    <table class="result-table" style="font-size: 0.85rem;">
                        <thead>
                            <tr style="background: var(--border);">
                                <th>Rok</th>
                                <th>Úspory (Cena energie) [€]</th>
                                <th>Splátka úveru [€]</th>
                                <th>Údržba / Výmena [€]</th>
                                <th>Čistý CF (rok) [€]</th>
                                <th>Kumulovaný CF [€]</th>
                            </tr>
                        </thead>
                        <tbody>
                            ${cfRows}
                        </tbody>
                    </table>
                </div>
            </div>
        `;
        box.classList.remove('hidden');
    } catch (e) {
        const box = document.getElementById('ch8-result');
        box.innerHTML = `<div class="error-msg">Chyba: ${e.message}</div>`;
        box.classList.remove('hidden');
    }
}

/**
 * Energetický Audit — Project Dashboard
 * Manages projects stored in localStorage and view navigation.
 */

'use strict';

/* ──────────────────────────────────────────────────────────────
   Constants
────────────────────────────────────────────────────────────── */
const STORAGE_KEY = 'ea_projects';

const BUILDING_ICONS = {
    'Bytový dom':      '🏢',
    'Rodinný dom':     '🏠',
    'Administratíva':  '🏛️',
    'Škola':           '🏫',
    'Nemocnica':       '🏥',
    'Priemysel':       '🏭',
    'Iné':             '🏗️',
};

/* ──────────────────────────────────────────────────────────────
   State
────────────────────────────────────────────────────────────── */
let currentProjectId = null;

/* ──────────────────────────────────────────────────────────────
   LocalStorage helpers
────────────────────────────────────────────────────────────── */
function loadProjects() {
    try {
        return JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]');
    } catch {
        return [];
    }
}

function saveProjects(projects) {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(projects));
}

function getProject(id) {
    return loadProjects().find(p => p.id === id) || null;
}

function upsertProject(project) {
    const projects = loadProjects();
    const idx = projects.findIndex(p => p.id === project.id);
    if (idx >= 0) {
        projects[idx] = project;
    } else {
        projects.unshift(project);
    }
    saveProjects(projects);
}

function deleteProject(id) {
    const projects = loadProjects().filter(p => p.id !== id);
    saveProjects(projects);
    if (currentProjectId === id) {
        currentProjectId = null;
    }
}

/* ──────────────────────────────────────────────────────────────
   View navigation
────────────────────────────────────────────────────────────── */
function showView(viewId) {
    ['view-dashboard', 'view-new-project', 'view-audit'].forEach(id => {
        const el = document.getElementById(id);
        if (el) el.style.display = (id === viewId) ? '' : 'none';
    });
    // Dark mode is handled by the global data-theme toggle
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

/* ──────────────────────────────────────────────────────────────
   Dashboard rendering
────────────────────────────────────────────────────────────── */
function renderDashboard(filter = '') {
    let projects = loadProjects();
    if (filter) {
        const q = filter.toLowerCase();
        projects = projects.filter(p =>
            (p.name || '').toLowerCase().includes(q) ||
            (p.address || '').toLowerCase().includes(q) ||
            (p.auditor || '').toLowerCase().includes(q)
        );
    }

    const grid = document.getElementById('projects-grid');
    const countEl = document.getElementById('dash-projects-count');
    if (!grid) return;

    if (countEl) {
        const total = loadProjects().length;
        countEl.textContent = filter
            ? `${projects.length} z ${total} projektov`
            : `${total} projekt${total === 1 ? '' : total < 5 ? 'y' : 'ov'}`;
    }

    if (projects.length === 0) {
        grid.innerHTML = `
            <div class="dash-empty">
                <div class="dash-empty-icon">📋</div>
                <h3>${filter ? 'Žiadne výsledky' : 'Zatiaľ žiadne projekty'}</h3>
                <p>${filter
                    ? 'Skúste iný vyhľadávací výraz.'
                    : 'Vytvorte prvý energetický audit kliknutím na tlačidlo vyššie.'
                }</p>
                ${!filter ? `<button class="btn-primary" onclick="showNewProject()">+ Nový projekt</button>` : ''}
            </div>`;
        return;
    }

    grid.innerHTML = projects.map(p => {
        const icon = BUILDING_ICONS[p.buildingType] || '🏗️';
        const date = p.createdAt
            ? new Date(p.createdAt).toLocaleDateString('sk-SK', { day: '2-digit', month: 'short', year: 'numeric' })
            : '—';
        return `
        <div class="project-card" onclick="openProject('${p.id}')">
            <div class="project-card-header">
                <div class="project-card-icon">${icon}</div>
                <div class="project-card-name" title="${escHtml(p.name || '')}">${escHtml(p.name || 'Bez názvu')}</div>
                <button class="project-card-menu" title="Zmazať projekt"
                    onclick="event.stopPropagation(); confirmDeleteProject('${p.id}', '${escHtml(p.name || 'projekt')}')">✕</button>
            </div>
            <div class="project-card-address">${escHtml(p.address || '—')}</div>
            <div class="project-card-meta">
                <span class="project-badge badge-type">${escHtml(p.buildingType || 'Neurčený')}</span>
                <span class="project-badge badge-date">📅 ${date}</span>
                ${p.auditor ? `<span class="project-badge badge-auditor">👤 ${escHtml(p.auditor)}</span>` : ''}
            </div>
        </div>`;
    }).join('');
}

/* ──────────────────────────────────────────────────────────────
   New project form
────────────────────────────────────────────────────────────── */
function showNewProject() {
    document.getElementById('new-project-form').reset();
    showView('view-new-project');
}

function handleNewProjectSubmit(e) {
    e.preventDefault();
    const form = e.target;
    const project = {
        id: 'ea_' + Date.now() + '_' + Math.random().toString(36).slice(2, 7),
        name:         form['np-name'].value.trim(),
        address:      form['np-address'].value.trim(),
        buildingType: form['np-type'].value,
        yearBuilt:    form['np-year'].value,
        floors:       form['np-floors'].value,
        auditor:      form['np-auditor'].value.trim(),
        auditNumber:  form['np-number'].value.trim(),
        createdAt:    new Date().toISOString(),
        updatedAt:    new Date().toISOString(),
        auditState:   null,
    };

    upsertProject(project);
    currentProjectId = project.id;
    enterAudit(project);
}

/* ──────────────────────────────────────────────────────────────
   Open existing project
────────────────────────────────────────────────────────────── */
function openProject(id) {
    const project = getProject(id);
    if (!project) { showToast('Projekt sa nenašiel', 'error'); return; }
    currentProjectId = id;
    enterAudit(project);
}

function enterAudit(project) {
    updateAuditHeader(project);

    // Restore saved audit state if available
    if (project.auditState) {
        try {
            restoreAuditState(project.auditState);
        } catch (err) {
            console.warn('Could not restore audit state:', err);
        }
    }

    // Pre-fill building name in ch2 from project
    const ch2name = document.getElementById('ch2-name');
    if (ch2name && !project.auditState) {
        ch2name.value = project.name || '';
    }

    showView('view-audit');
}

/* ──────────────────────────────────────────────────────────────
   Audit header — project info strip
────────────────────────────────────────────────────────────── */
function updateAuditHeader(project) {
    const strip = document.getElementById('audit-project-strip');
    if (!strip) return;
    strip.innerHTML = `
        <div class="header-project-info">
            <button class="btn-back-dashboard" onclick="goToDashboard()">← Projekty</button>
            <div class="header-project-name">
                📁 <span>${escHtml(project.name || 'Bez názvu')}</span>
                &nbsp;·&nbsp; ${escHtml(project.buildingType || '')}
                ${project.address ? `&nbsp;·&nbsp; <span>${escHtml(project.address)}</span>` : ''}
            </div>
            <button class="btn-save-project" onclick="saveCurrentProject()">💾 Uložiť</button>
        </div>`;
}

/* ──────────────────────────────────────────────────────────────
   Save & restore audit state
────────────────────────────────────────────────────────────── */
function saveCurrentProject() {
    if (!currentProjectId) { showToast('Žiadny aktívny projekt', 'error'); return; }

    const project = getProject(currentProjectId);
    if (!project) { showToast('Projekt sa nenašiel', 'error'); return; }

    project.auditState = captureAuditState();
    project.updatedAt  = new Date().toISOString();
    upsertProject(project);
    showToast('💾 Projekt uložený', 'success');
}

/**
 * Capture all form inputs in the audit view as a plain object.
 */
function captureAuditState() {
    const state = {};
    const auditView = document.getElementById('view-audit');
    if (!auditView) return state;

    // Named inputs with IDs
    auditView.querySelectorAll('input[id], select[id], textarea[id]').forEach(el => {
        if (el.type === 'checkbox') {
            state[el.id] = el.checked;
        } else {
            state[el.id] = el.value;
        }
    });

    // Dynamic rows — layers table
    const layerRows = [];
    document.querySelectorAll('#layers-tbody tr').forEach(tr => {
        const inputs = tr.querySelectorAll('input');
        if (inputs.length >= 6) {
            layerRows.push([...inputs].slice(0, 6).map(i => i.value));
        }
    });
    state['__layers__'] = layerRows;

    // Dynamic HT construction rows
    const htRows = [];
    document.querySelectorAll('#ht-constructions .ct-row').forEach(row => {
        htRows.push({
            name: row.querySelector('.ht-name')?.value || '',
            u:    row.querySelector('.ht-u')?.value || '',
            a:    row.querySelector('.ht-a')?.value || '',
            bx:   row.querySelector('.ht-bx')?.value || '',
        });
    });
    state['__ht_rows__'] = htRows;

    // Dynamic solar rows
    const solRows = [];
    document.querySelectorAll('#solar-rows .solar-row').forEach(row => {
        solRows.push({
            orient: row.querySelector('.sol-orient')?.value || '',
            area:   row.querySelector('.sol-area')?.value  || '',
            ggl:    row.querySelector('.sol-ggl')?.value   || '',
            fsh:    row.querySelector('.sol-fsh')?.value   || '',
        });
    });
    state['__solar_rows__'] = solRows;

    return state;
}

/**
 * Hydrate audit form from saved state.
 */
function restoreAuditState(state) {
    const auditView = document.getElementById('view-audit');
    if (!auditView) return;

    // Named inputs
    Object.entries(state).forEach(([id, val]) => {
        if (id.startsWith('__')) return;
        const el = document.getElementById(id);
        if (!el) return;
        if (el.type === 'checkbox') {
            el.checked = val;
        } else {
            el.value = val;
        }
    });

    // Layers
    if (Array.isArray(state['__layers__']) && state['__layers__'].length > 0) {
        const tbody = document.getElementById('layers-tbody');
        if (tbody && typeof addLayerRow === 'function') {
            tbody.innerHTML = '';
            state['__layers__'].forEach(row => {
                addLayerRow();
                const inputs = tbody.querySelectorAll('tr:last-child input');
                row.forEach((val, i) => { if (inputs[i]) inputs[i].value = val; });
            });
        }
    }

    // HT rows
    if (Array.isArray(state['__ht_rows__']) && state['__ht_rows__'].length > 0) {
        const container = document.getElementById('ht-constructions');
        if (container && typeof addHTRow === 'function') {
            container.innerHTML = '';
            state['__ht_rows__'].forEach(r => {
                addHTRow();
                const row = container.querySelector('.ct-row:last-child');
                if (!row) return;
                const n = row.querySelector('.ht-name'); if (n) n.value = r.name;
                const u = row.querySelector('.ht-u');    if (u) u.value = r.u;
                const a = row.querySelector('.ht-a');    if (a) a.value = r.a;
                const bx = row.querySelector('.ht-bx');  if (bx) bx.value = r.bx;
            });
        }
    }

    // Solar rows
    if (Array.isArray(state['__solar_rows__']) && state['__solar_rows__'].length > 0) {
        const container = document.getElementById('solar-rows');
        if (container && typeof addSolarRow === 'function') {
            container.innerHTML = '';
            state['__solar_rows__'].forEach(r => {
                addSolarRow();
                const row = container.querySelector('.solar-row:last-child');
                if (!row) return;
                const orient = row.querySelector('.sol-orient'); if (orient) orient.value = r.orient;
                const area   = row.querySelector('.sol-area');   if (area)   area.value   = r.area;
                const ggl    = row.querySelector('.sol-ggl');    if (ggl)    ggl.value    = r.ggl;
                const fsh    = row.querySelector('.sol-fsh');    if (fsh)    fsh.value    = r.fsh;
            });
        }
    }
}

/* ──────────────────────────────────────────────────────────────
   Delete project
────────────────────────────────────────────────────────────── */
function confirmDeleteProject(id, name) {
    if (!confirm(`Naozaj chcete zmazať projekt „${name}"?\nTáto akcia je nevratná.`)) return;
    deleteProject(id);
    renderDashboard(document.getElementById('dash-search')?.value || '');
    showToast('🗑️ Projekt zmazaný');
}

/* ──────────────────────────────────────────────────────────────
   Go back to dashboard
────────────────────────────────────────────────────────────── */
function goToDashboard() {
    renderDashboard();
    showView('view-dashboard');
}

/* ──────────────────────────────────────────────────────────────
   Toast
────────────────────────────────────────────────────────────── */
let _toastTimer = null;
function showToast(message, type = 'success') {
    const toast = document.getElementById('app-toast');
    if (!toast) return;
    toast.textContent = message;
    toast.className = `toast ${type}`;
    // Force reflow so re-triggering works
    void toast.offsetHeight;
    toast.classList.add('show');
    clearTimeout(_toastTimer);
    _toastTimer = setTimeout(() => toast.classList.remove('show'), 3000);
}

/* ──────────────────────────────────────────────────────────────
   Utils
────────────────────────────────────────────────────────────── */
function escHtml(str) {
    return String(str)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;');
}

/* ──────────────────────────────────────────────────────────────
   Init
────────────────────────────────────────────────────────────── */
document.addEventListener('DOMContentLoaded', () => {
    // Start on dashboard
    showView('view-dashboard');
    renderDashboard();

    // Search
    const searchInput = document.getElementById('dash-search');
    if (searchInput) {
        searchInput.addEventListener('input', () => renderDashboard(searchInput.value));
    }

    // New project form submit
    const form = document.getElementById('new-project-form');
    if (form) {
        form.addEventListener('submit', handleNewProjectSubmit);
    }
});

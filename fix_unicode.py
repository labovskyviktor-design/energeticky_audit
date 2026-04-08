import sys, re

filepath = r'c:\Users\42191\.gemini\antigravity\scratch\energy-audit\frontend\static\materials.js'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

new_content = """window.MATERIALS = {

    // ── Betón a konštrukčné materiály ──────────────────────────────
    concrete: {
        label: 'Betón a ŽB',
        icon: '🏗️',
        items: [
            { name: 'Betón hutný (2100 kg/m³)',       lambda: 1.23, rho: 2100, c: 1020, mu: 17,  d: 0.20  },
            { name: 'Betón hutný (2200 kg/m³)',       lambda: 1.30, rho: 2200, c: 1020, mu: 17,  d: 0.20  },
            { name: 'Betón hutný (2300 kg/m³)',       lambda: 1.36, rho: 2300, c: 1020, mu: 17,  d: 0.20  },
            { name: 'Železobetón (2300 kg/m³)',       lambda: 1.43, rho: 2300, c: 1020, mu: 23,  d: 0.20  },
            { name: 'Železobetón (2400 kg/m³)',       lambda: 1.58, rho: 2400, c: 1020, mu: 25,  d: 0.20  },
            { name: 'ŽB stena panelová',              lambda: 1.58, rho: 2400, c: 1020, mu: 25,  d: 0.15  },
            { name: 'Ľahký betón keramzitový 800',    lambda: 0.31, rho: 800,  c: 840,  mu: 5,   d: 0.15  },
            { name: 'Ľahký betón keramzitový 1200',   lambda: 0.56, rho: 1200, c: 840,  mu: 8,   d: 0.15  },
            { name: 'Pórobetón (580 kg/m³)',          lambda: 0.21, rho: 580,  c: 840,  mu: 7,   d: 0.30  },
        ]
    },

    // ── Priečky a obvodové murivo ─────────────────────────────────
    masonry: {
        label: 'Murovivo a kvádre',
        icon: '🧱',
        items: [
            { name: 'Tehla pálená plná (CPP)',        lambda: 0.80, rho: 1800, c: 900,  mu: 9,   d: 0.38  },
            { name: 'Tehla dierovaná (CDm)',          lambda: 0.55, rho: 1400, c: 960,  mu: 8,   d: 0.375 },
            { name: 'Keramické dutinové bloky',       lambda: 0.15, rho: 800,  c: 960,  mu: 10,  d: 0.30  },
            { name: 'Porotherm 38 P+D (Katalog)',     lambda: 0.14, rho: 800,  c: 960,  mu: 10,  d: 0.38  },
            { name: 'Porotherm 44 T Profi (s vatou)', lambda: 0.064,rho: 650,  c: 1000, mu: 10,  d: 0.44  },
            { name: 'Ytong Standard (P2-400)',        lambda: 0.11, rho: 400,  c: 1000, mu: 7,   d: 0.30  },
            { name: 'Ytong Statik (P4-500)',          lambda: 0.14, rho: 500,  c: 1000, mu: 7,   d: 0.25  },
            { name: 'Ytong Lambda YQ',                lambda: 0.08, rho: 300,  c: 1000, mu: 5,   d: 0.45  },
            { name: 'Vápennopiesková tehla (KS)',     lambda: 0.80, rho: 1800, c: 840,  mu: 15,  d: 0.20  },
            { name: 'Betónová tvárnica zo škváry',    lambda: 0.67, rho: 1200, c: 840,  mu: 30,  d: 0.20  },
        ]
    },

    // ── Tepelné izolácie ──────────────────────────────────────────
    insulation: {
        label: 'Tepelné izolácie',
        icon: '🌡️',
        items: [
            { name: 'Minerálna plsť (ČSN/STN)',       lambda: 0.056,rho: 100, c: 840,  mu: 1.5, d: 0.15  },
            { name: 'Minerálna vlna fasádna (Novšia)',lambda: 0.038,rho: 100, c: 840,  mu: 1.5, d: 0.15  },
            { name: 'EPS Polystyrén (20 kg/m³)',      lambda: 0.044,rho: 20,  c: 1270, mu: 40,  d: 0.15  },
            { name: 'EPS Polystyrén (30 kg/m³)',      lambda: 0.039,rho: 30,  c: 1270, mu: 40,  d: 0.10  },
            { name: 'EPS Grafit / sivý (100 F)',      lambda: 0.031,rho: 20,  c: 1270, mu: 40,  d: 0.15  },
            { name: 'XPS (Extrudovaný polystyrén)',   lambda: 0.034,rho: 30,  c: 2060, mu: 140, d: 0.10  },
            { name: 'PUR (Polyuretán tuhý)',          lambda: 0.032,rho: 35,  c: 1400, mu: 120, d: 0.12  },
            { name: 'Penové sklo (Foamglas)',         lambda: 0.069,rho: 140, c: 840,  mu: 70000,d: 0.10  },
            { name: 'Drevovláknitá doska mäkká',      lambda: 0.046,rho: 230, c: 2100, mu: 5,   d: 0.10  },
            { name: 'Celulóza striekaná/fúkaná',      lambda: 0.040,rho: 50,  c: 1900, mu: 2,   d: 0.20  },
        ]
    },

    // ── Drevo a konštrukčné dosky ─────────────────────────────────
    wood: {
        label: 'Drevo a dosky',
        icon: '🪵',
        items: [
            { name: 'Drevo mäkké (kolmo k vláknu)',   lambda: 0.18, rho: 400, c: 2510, mu: 157, d: 0.10  },
            { name: 'Drevo tvrdé (kolmo k vláknu)',   lambda: 0.22, rho: 600, c: 2510, mu: 157, d: 0.02  },
            { name: 'OSB doska',                      lambda: 0.13, rho: 600, c: 1700, mu: 50,  d: 0.022 },
            { name: 'Preglejka stavebná',             lambda: 0.15, rho: 600, c: 1600, mu: 70,  d: 0.018 },
            { name: 'Drevotriesková doska (DTD)',     lambda: 0.11, rho: 800, c: 1700, mu: 15,  d: 0.018 },
            { name: 'Drevovláknitá doska (lisovaná)', lambda: 0.075,rho: 800, c: 1700, mu: 20,  d: 0.016 },
        ]
    },

    // ── Omietky a obklady ─────────────────────────────────────────
    plaster: {
        label: 'Omietky a SDK',
        icon: '🪨',
        items: [
            { name: 'Vápenná omietka',                lambda: 0.88, rho: 1600, c: 840,  mu: 15,  d: 0.015 },
            { name: 'Vápenocementová omietka',        lambda: 0.99, rho: 2000, c: 840,  mu: 15,  d: 0.015 },
            { name: 'Cementová omietka',              lambda: 1.16, rho: 2000, c: 840,  mu: 19,  d: 0.015 },
            { name: 'Sadrová omietka',                lambda: 0.57, rho: 1300, c: 840,  mu: 10,  d: 0.012 },
            { name: 'Silikátová / silikónová omietka',lambda: 0.70, rho: 1700, c: 840,  mu: 40,  d: 0.003 },
            { name: 'Lepiaca stierka (ETICS)',        lambda: 0.80, rho: 1500, c: 840,  mu: 20,  d: 0.004 },
            { name: 'Sadrokartón GKB',                lambda: 0.22, rho: 750,  c: 1060, mu: 9,   d: 0.0125},
            { name: 'Sadrokartón GKFI (zelený)',      lambda: 0.22, rho: 800,  c: 1060, mu: 12,  d: 0.0125},
            { name: 'Sádrovláknitá doska',            lambda: 0.32, rho: 1150, c: 1100, mu: 13,  d: 0.0125},
        ]
    },

    // ── Konštrukcie podláh a stropov ──────────────────────────────
    floor: {
        label: 'Podlahy a potery',
        icon: '🏠',
        items: [
            { name: 'Cementový poter (Betón hutný)',  lambda: 1.23, rho: 2100, c: 1020, mu: 17,  d: 0.05  },
            { name: 'Cementový poter (Malta)',        lambda: 1.16, rho: 2000, c: 840,  mu: 19,  d: 0.05  },
            { name: 'Anhydritový poter',              lambda: 1.20, rho: 2100, c: 840,  mu: 20,  d: 0.04  },
            { name: 'Keramická dlažba hutná',         lambda: 1.01, rho: 2000, c: 840,  mu: 200, d: 0.01  },
            { name: 'Prírodný kameň (žula)',          lambda: 2.80, rho: 2600, c: 840,  mu: 10000, d: 0.02 },
            { name: 'Drevené parkety / dlážka',       lambda: 0.18, rho: 400,  c: 2510, mu: 157, d: 0.015 },
            { name: 'Laminátová podlaha',             lambda: 0.14, rho: 600,  c: 1600, mu: 50,  d: 0.01  },
            { name: 'Linoleum / PVC krytina',         lambda: 0.19, rho: 1200, c: 1400, mu: 1000,d: 0.003 },
            { name: 'Koberec',                        lambda: 0.06, rho: 200,  c: 1300, mu: 2,   d: 0.005 },
        ]
    },

    // ── Hydro a Parozábrany ───────────────────────────────────────
    membrane: {
        label: 'Fólie a hydroizolácie',
        icon: '🛡️',
        items: [
            { name: 'Asfaltový pás klasický (IPA)',   lambda: 0.21, rho: 1400, c: 1470, mu: 20000, d: 0.004 },
            { name: 'Asfaltový pás s AL vložkou',     lambda: 0.21, rho: 1400, c: 1470, mu: 500000,d: 0.004 },
            { name: 'Parozábrana PE fólia',           lambda: 0.35, rho: 930,  c: 1470, mu: 100000,d: 0.0002},
            { name: 'PVC Hydroizolačná fólia (mPVC)', lambda: 0.16, rho: 1400, c: 1470, mu: 20000, d: 0.0015},
            { name: 'Poistná hydroizolácia (difúzna)',lambda: 0.35, rho: 400,  c: 1470, mu: 100,   d: 0.0005},
        ]
    },

    // ── Ostatné ───────────────────────────────────────────────────
    other: {
        label: 'Zemina a výplne',
        icon: '🔩',
        items: [
            { name: 'Štrkopiesok / makadam (Štěrk)',  lambda: 0.93, rho: 1650, c: 920,  mu: 5,   d: 0.20  },
            { name: 'Piesok',                         lambda: 0.95, rho: 1750, c: 840,  mu: 5,   d: 0.10  },
            { name: 'Zemina prírodná (vlhká)',        lambda: 2.00, rho: 2000, c: 840,  mu: 2,   d: 0.50  },
            { name: 'Vzduchová medzera uzavretá',     lambda: 0.18, rho: 1.25, c: 1010, mu: 1,   d: 0.05  },
        ]
    }
}"""

content = re.sub(r'window\.MATERIALS\s*=\s*\{.*?\n\};\n', new_content + '\n;\n', content, flags=re.DOTALL)
with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print('Replaced window.MATERIALS.')

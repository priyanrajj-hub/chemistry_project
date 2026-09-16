// Custom Cursor Glow
const cursor = document.getElementById('cursor-glow');
document.addEventListener('mousemove', (e) => {
    cursor.style.left = e.clientX + 'px';
    cursor.style.top = e.clientY + 'px';
});
document.addEventListener('mousedown', () => cursor.style.transform = 'translate(-50%, -50%) scale(0.8)');
document.addEventListener('mouseup', () => cursor.style.transform = 'translate(-50%, -50%) scale(1)');

document.querySelectorAll('a, button, .glass-card').forEach(el => {
    el.addEventListener('mouseenter', () => {
        cursor.style.width = '60px';
        cursor.style.height = '60px';
        cursor.style.filter = 'blur(20px)';
    });
    el.addEventListener('mouseleave', () => {
        cursor.style.width = '30px';
        cursor.style.height = '30px';
        cursor.style.filter = 'blur(15px)';
    });
});

// GSAP Animations
gsap.registerPlugin(ScrollTrigger);

// Reveal elements on scroll
gsap.utils.toArray('.gs-reveal').forEach(function (elem) {
    gsap.fromTo(elem,
        { y: 50, opacity: 0 },
        {
            y: 0, opacity: 1, duration: 1,
            ease: "power3.out",
            scrollTrigger: {
                trigger: elem,
                start: "top 85%", // when top of element hits 85% viewport
                toggleActions: "play none none none"
            }
        }
    );
});

// Number Counter Animation
const formatNum = (num, isFloat) => isFloat ? num.toFixed(2) : Math.floor(num);
gsap.utils.toArray('.counter').forEach(function (counter) {
    const target = parseFloat(counter.getAttribute('data-target'));
    const isFloat = target % 1 !== 0;

    ScrollTrigger.create({
        trigger: counter,
        start: "top 90%",
        onEnter: () => {
            gsap.to(counter, {
                innerHTML: target,
                duration: 2,
                ease: "power2.out",
                snap: { innerHTML: isFloat ? 0.01 : 1 },
                onUpdate: function () {
                    counter.innerHTML = formatNum(this.targets()[0].innerHTML, isFloat);
                }
            });
        },
        once: true
    });
});


// ----------------------------------------------------
// THREE.JS HERO SCENE
// ----------------------------------------------------
const initHero3D = () => {
    const container = document.getElementById('hero-3d-container');
    const width = container.clientWidth;
    const height = container.clientHeight;

    const scene = new THREE.Scene();

    // Camera
    const camera = new THREE.PerspectiveCamera(45, width / height, 0.1, 1000);
    camera.position.z = 10;

    // Renderer (transparent)
    const renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });
    renderer.setSize(width, height);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    container.appendChild(renderer.domElement);

    // Torus Knot (Impedance spiral vibe)
    const isMobile = window.innerWidth < 900;
    const tubeGeometry = new THREE.TorusKnotGeometry(3, 1, isMobile ? 64 : 128, isMobile ? 8 : 16);

    const wireframeMat = new THREE.MeshBasicMaterial({
        color: 0x00e5ff,
        wireframe: true,
        transparent: true,
        opacity: 0.3
    });
    const solidMat = new THREE.MeshPhysicalMaterial({
        color: 0x0a0e17,
        metalness: 0.8,
        roughness: 0.2,
        clearcoat: 1.0,
        clearcoatRoughness: 0.1
    });

    const torus = new THREE.Mesh(tubeGeometry, solidMat);
    const torusWire = new THREE.Mesh(tubeGeometry, wireframeMat);
    torusWire.scale.set(1.02, 1.02, 1.02); // slightly larger so wire passes through

    const group = new THREE.Group();
    group.add(torus);
    group.add(torusWire);
    scene.add(group);

    // Lighting
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
    scene.add(ambientLight);

    const pointLight = new THREE.PointLight(0x00e5ff, 2);
    pointLight.position.set(5, 5, 5);
    scene.add(pointLight);

    // Mouse Parallax
    let mouseX = 0;
    let mouseY = 0;

    if (!isMobile) {
        document.addEventListener('mousemove', (event) => {
            mouseX = (event.clientX / window.innerWidth) * 2 - 1;
            mouseY = -(event.clientY / window.innerHeight) * 2 + 1;
        });
    }

    // Animation Loop
    const animate = () => {
        requestAnimationFrame(animate);

        group.rotation.x += 0.005;
        group.rotation.y += 0.007;

        if (!isMobile) {
            // Smooth mouse parallax
            scene.rotation.x += (mouseY * 0.5 - scene.rotation.x) * 0.05;
            scene.rotation.y += (mouseX * 0.5 - scene.rotation.y) * 0.05;
        }

        renderer.render(scene, camera);
    };
    animate();

    // Handle Resize
    window.addEventListener('resize', () => {
        camera.aspect = container.clientWidth / container.clientHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(container.clientWidth, container.clientHeight);
    });
};


// ----------------------------------------------------
// THREE.JS HARDWARE BREAKDOWN
// ----------------------------------------------------
const initHardware3D = () => {
    const container = document.getElementById('hardware-3d-container');
    if (!container) return;

    const width = container.clientWidth;
    const height = container.clientHeight;

    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(40, width / height, 0.1, 100);
    camera.position.set(0, 5, 12);
    camera.lookAt(0, 0, 0);

    const renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });
    renderer.setSize(width, height);
    container.appendChild(renderer.domElement);

    const group = new THREE.Group();

    // helper function to create styled boxes
    const createMod = (w, h, d, color = 0x00e5ff, labelStr) => {
        const mat = new THREE.MeshPhongMaterial({
            color: color,
            transparent: true,
            opacity: 0.8,
            specular: 0xffffff,
            shininess: 100
        });
        const geo = new THREE.BoxGeometry(w, h, d);
        const mesh = new THREE.Mesh(geo, mat);

        const edges = new THREE.EdgesGeometry(geo);
        const line = new THREE.LineSegments(edges, new THREE.LineBasicMaterial({ color: 0xffffff, opacity: 0.5, transparent: true }));
        mesh.add(line);
        return mesh;
    };

    // Build the diagram
    const esp32 = createMod(2, 0.5, 3, 0x028090); // ESP32
    esp32.position.set(-3, 0, 0);

    const ad9833 = createMod(1.5, 0.3, 1.5, 0x00e5ff); // Signal Gen
    ad9833.position.set(0, 0, -1.5);

    const ads1115 = createMod(1.5, 0.3, 1.5, 0x00A896); // ADC
    ads1115.position.set(0, 0, 1.5);

    const battery = createMod(1.5, 2.5, 1.5, 0xff4d4d); // Battery cell
    battery.position.set(3, 0, 0);

    group.add(esp32, ad9833, ads1115, battery);
    scene.add(group);

    // Lights
    scene.add(new THREE.AmbientLight(0x404040));
    const pl = new THREE.PointLight(0xffffff, 1, 100);
    pl.position.set(5, 5, 5);
    scene.add(pl);

    const animate = () => {
        requestAnimationFrame(animate);
        group.rotation.y += 0.005;
        renderer.render(scene, camera);
    };
    animate();

    window.addEventListener('resize', () => {
        const w = container.clientWidth;
        const h = container.clientHeight;
        camera.aspect = w / h;
        camera.updateProjectionMatrix();
        renderer.setSize(w, h);
    });
};

// ----------------------------------------------------
// PLOTLY 3D INTERACTIVE NYQUIST
// ----------------------------------------------------
const initPlotlyNyquist = async () => {
    try {
        const response = await fetch('nyquist_data.json');
        if (!response.ok) throw new Error("JSON not generated yet or missing");

        const data = await response.json();

        const plotData = [];
        const colors = { 'Fresh': '#00ffc8', 'Mid-life': '#028090', 'Aged': '#ff4d4d' };

        // Use logarithmic index as pseudo-frequency axis for Better 3D spacing
        // (Real physical frequencies pile up at one end otherwise)
        let logFreq = data.frequencies.map(f => Math.log10(f));

        for (const [state, series] of Object.entries(data.series)) {
            // Convert to Plotly 3D scatter
            plotData.push({
                type: 'scatter3d',
                mode: 'lines+markers',
                name: state,
                x: series.z_real,       // Z'
                y: logFreq,             // log(F)
                z: series.z_imag,       // -Z''
                line: {
                    width: 4,
                    color: colors[state]
                },
                marker: {
                    size: 3,
                    color: colors[state]
                }
            });
        }

        const layout = {
            paper_bgcolor: 'rgba(0,0,0,0)',
            plot_bgcolor: 'rgba(0,0,0,0)',
            font: { color: '#8a9fc2' },
            margin: { l: 0, r: 0, b: 0, t: 0 },
            scene: {
                xaxis: { title: "Z' (Real)", gridcolor: '#222', zerolinecolor: '#444', showbackground: false },
                yaxis: { title: "Log10(Freq) Hz", gridcolor: '#222', zerolinecolor: '#444', showbackground: false },
                zaxis: { title: "-Z'' (Imag)", gridcolor: '#222', zerolinecolor: '#444', showbackground: false },
                camera: { eye: { x: 1.5, y: -1.5, z: 1.2 } }
            },
            legend: { orientation: "h", y: 1.1 }
        };

        Plotly.newPlot('plotly-3d-nyquist', plotData, layout, { displayModeBar: false, responsive: true });

    } catch (e) {
        console.warn("Plotly Nyquist visualization failed:", e);
        document.getElementById('plotly-3d-nyquist').innerHTML =
            "<p style='text-align:center; padding-top:50px;'>Run Python pipeline first to generate nyquist_data.json</p>";
    }
};

// Initialize heavy libs only once DOM is ready
document.addEventListener("DOMContentLoaded", () => {
    initHero3D();

    // Intersection observer for lazy loading the next 3D scenes
    let hardwareLoaded = false;
    let plotlyLoaded = false;

    const hwObserver = new IntersectionObserver(entries => {
        if (entries[0].isIntersecting && !hardwareLoaded) {
            initHardware3D();
            hardwareLoaded = true;
        }
    });
    hwObserver.observe(document.getElementById('hardware'));

    const plotObserver = new IntersectionObserver(entries => {
        if (entries[0].isIntersecting && !plotlyLoaded) {
            initPlotlyNyquist();
            plotlyLoaded = true;
        }
    });
    plotObserver.observe(document.getElementById('results'));
});

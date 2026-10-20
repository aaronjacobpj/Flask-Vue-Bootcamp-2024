<script setup>
    import { animate, createTimeline, createMotionPath, set, stagger } from "animejs";
</script>

<template>
    <figure class="net-scene" ref="scene" aria-label="Animated diagram of a browser talking to a Flask server, database and Celery worker">
        <figcaption class="net-caption"><span class="live-dot"></span> Behind the scenes</figcaption>
        <svg viewBox="0 0 560 420" role="img" aria-hidden="true">
            <defs>
                <linearGradient id="ns-panel" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0" stop-color="#1e293b" />
                    <stop offset="1" stop-color="#0f172a" />
                </linearGradient>
                <filter id="ns-glow" x="-50%" y="-50%" width="200%" height="200%">
                    <feGaussianBlur stdDeviation="4" result="b" />
                    <feMerge><feMergeNode in="b" /><feMergeNode in="SourceGraphic" /></feMerge>
                </filter>
            </defs>

            <!-- connection wires -->
            <g class="wires">
                <path ref="pReq" class="wire" d="M242 82 C 285 40, 300 40, 330 62" />
                <path ref="pRes" class="wire" d="M330 138 C 295 172, 280 172, 242 158" />
                <path ref="pToDb" class="wire" d="M420 162 C 418 210, 428 240, 430 282" />
                <path ref="pFromDb" class="wire" d="M462 282 C 464 240, 474 210, 476 162" />
                <path ref="pToWorker" class="wire" d="M340 160 C 300 230, 260 250, 214 312" />
                <path ref="pFromWorker" class="wire" d="M214 356 C 300 360, 360 300, 372 162" />
            </g>

            <!-- Browser (Vue) -->
            <g class="node browser">
                <rect x="20" y="30" width="222" height="172" rx="12" class="panel" />
                <rect x="20" y="30" width="222" height="24" rx="12" class="titlebar" />
                <rect x="20" y="44" width="222" height="10" class="titlebar" />
                <circle cx="36" cy="42" r="4" fill="#f87171" />
                <circle cx="50" cy="42" r="4" fill="#fbbf24" />
                <circle cx="64" cy="42" r="4" fill="#34d399" />
                <rect x="78" y="35" width="150" height="14" rx="7" class="urlbar" />
                <text x="88" y="45.5" class="mono tiny" ref="url">localhost:5173/</text>

                <text x="34" y="76" class="label">Vue app</text>
                <g ref="spinner" class="spinner" opacity="0">
                    <circle cx="222" cy="72" r="6" class="spin-track" />
                    <path d="M222 66 A 6 6 0 0 1 228 72" class="spin-arc" />
                </g>

                <g class="skeleton">
                    <rect v-for="(w, i) in skeleton" x="34" :y="90 + i * 18" :width="w" height="9" rx="4.5" class="sk-bg" />
                    <rect v-for="(w, i) in skeleton" x="34" :y="90 + i * 18" :width="w" height="9" rx="4.5" class="sk-fill" />
                </g>

                <g ref="badge" class="badge" opacity="0">
                    <rect x="34" y="174" width="120" height="18" rx="9" class="badge-bg" />
                    <text x="44" y="186.5" class="tiny badge-text" ref="badgeText">✓ Logged in</text>
                </g>
            </g>

            <!-- Flask server -->
            <g class="node server">
                <rect x="330" y="30" width="210" height="132" rx="12" class="panel" />
                <text x="346" y="54" class="label">Flask API</text>
                <text x="414" y="54" class="mono tiny dim">:5000</text>
                <circle ref="led" cx="522" cy="50" r="4" class="led" />
                <rect x="342" y="66" width="186" height="84" rx="6" class="console" />
                <text v-for="(line, i) in logs" :key="line.id" x="350" :y="84 + i * 18" class="mono tiny log" :class="line.kind">
                    {{ line.text }}
                </text>
            </g>

            <!-- Database -->
            <g class="node db" ref="db">
                <path d="M400 290 v 70 a 46 12 0 0 0 92 0 v -70" class="panel" />
                <ellipse cx="446" cy="290" rx="46" ry="12" class="db-top" />
                <path d="M400 314 a 46 12 0 0 0 92 0" class="db-ring" />
                <path d="M400 338 a 46 12 0 0 0 92 0" class="db-ring" />
                <text x="446" y="392" text-anchor="middle" class="label">SQLite</text>
            </g>

            <!-- Celery worker -->
            <g class="node worker">
                <rect x="40" y="300" width="174" height="92" rx="12" class="panel" />
                <text x="56" y="324" class="label">Celery worker</text>
                <text x="56" y="342" class="mono tiny dim" ref="workerStatus">idle</text>
                <rect x="56" y="356" width="142" height="8" rx="4" class="sk-bg" />
                <rect ref="progress" x="56" y="356" width="142" height="8" rx="4" class="progress" />
                <text x="56" y="382" class="mono tiny dim">redis://queue</text>
            </g>

            <!-- travelling packets -->
            <g ref="packetA" class="packet" opacity="0">
                <rect class="packet-bg" x="-40" y="-10" width="80" height="20" rx="10" />
                <text class="mono tiny packet-text" text-anchor="middle" y="3.5"></text>
            </g>
            <g ref="packetB" class="packet" opacity="0">
                <rect class="packet-bg" x="-40" y="-10" width="80" height="20" rx="10" />
                <text class="mono tiny packet-text" text-anchor="middle" y="3.5"></text>
            </g>
        </svg>
    </figure>
</template>

<script>
    const COLORS = {
        req: "#38bdf8",
        res: "#42b883",
        db: "#f59e0b",
        task: "#a78bfa",
    };

    export default {
        data() {
            return {
                skeleton: [150, 180, 120, 165],
                logs: [],
                logId: 0,
            };
        },
        methods: {
            log(text, kind) {
                this.logs.push({ id: this.logId++, text, kind });
                if (this.logs.length > 4) this.logs.shift();
            },
            setPacket(el, label, kind) {
                const w = label.length * 6.3 + 22;
                const rect = el.querySelector("rect");
                rect.setAttribute("width", w);
                rect.setAttribute("x", -w / 2);
                rect.setAttribute("stroke", COLORS[kind]);
                el.querySelector("text").textContent = label;
                el.querySelector("text").setAttribute("fill", COLORS[kind]);
            },
            buildTimeline() {
                const r = this.$refs;
                const sk = r.scene.querySelectorAll(".sk-fill");
                const tl = createTimeline({ loop: true, loopDelay: 1200 });
                let t = 0;

                // Moves a labelled packet along a wire, starting at time `at`
                const send = (packet, path, label, kind, at, duration = 1100) => {
                    const { translateX, translateY } = createMotionPath(path);
                    tl.call(() => this.setPacket(packet, label, kind), at);
                    tl.add(packet, {
                        translateX,
                        translateY,
                        opacity: [0, 1, 1, 1, 0],
                        duration,
                        ease: "inOutSine",
                    }, at);
                    tl.add(path, {
                        stroke: [COLORS[kind], "rgba(148,163,184,.25)"],
                        strokeWidth: [2.5, 1.5],
                        duration: duration + 400,
                        ease: "outQuad",
                    }, at);
                    return at + duration;
                };
                const flash = (at, color = COLORS.res) => {
                    tl.add(r.led, { fill: [color, "#22c55e"], r: [7, 4], duration: 600, ease: "outQuad" }, at);
                };
                const loading = (on, at) => {
                    tl.add(r.spinner, { opacity: on ? 1 : 0, duration: 200 }, at);
                };
                const fillPage = (at) => {
                    tl.add(sk, { scaleX: [0, 1], delay: stagger(90), duration: 600, ease: "outExpo" }, at);
                };

                // reset state at the top of every loop
                tl.call(() => {
                    this.logs = [];
                    r.url.textContent = "localhost:5173/";
                    r.workerStatus.textContent = "idle";
                    set(sk, { scaleX: 0 });
                    set(r.progress, { scaleX: 0 });
                    set(r.badge, { opacity: 0 });
                }, 0);

                // 1) GET /api/courses → DB → 200 JSON
                t = 300;
                loading(true, t);
                t = send(r.packetA, r.pReq, "GET /api/courses", "req", t);
                tl.call(() => this.log("GET /api/courses", "req"), t);
                flash(t, COLORS.req);
                t = send(r.packetA, r.pToDb, "SELECT * FROM course", "db", t + 150, 900);
                tl.add(r.db, { scale: [1, 1.06, 1], duration: 500, ease: "outQuad" }, t);
                t = send(r.packetA, r.pFromDb, "18 rows", "db", t + 200, 900);
                tl.call(() => this.log("200 OK  42ms", "res"), t);
                flash(t);
                t = send(r.packetA, r.pRes, "200 OK · JSON", "res", t + 150);
                loading(false, t);
                fillPage(t);

                // 2) POST /api/login → DB → token
                t += 1100;
                tl.call(() => { r.url.textContent = "localhost:5173/login"; set(sk, { scaleX: 0 }); }, t);
                loading(true, t);
                t = send(r.packetA, r.pReq, "POST /api/login", "req", t + 200);
                tl.call(() => this.log("POST /api/login", "req"), t);
                flash(t, COLORS.req);
                t = send(r.packetA, r.pToDb, "SELECT user", "db", t + 150, 900);
                tl.add(r.db, { scale: [1, 1.06, 1], duration: 500, ease: "outQuad" }, t);
                t = send(r.packetA, r.pFromDb, "1 row", "db", t + 200, 900);
                tl.call(() => this.log("200 OK  token", "res"), t);
                flash(t);
                t = send(r.packetA, r.pRes, "200 · auth-token", "res", t + 150);
                loading(false, t);
                fillPage(t);
                tl.call(() => { r.badgeText.textContent = "✓ Logged in"; }, t);
                tl.add(r.badge, { opacity: [0, 1], translateY: [8, 0], duration: 500, ease: "outBack(2)" }, t);

                // 3) POST /api/export → Celery task (async) → CSV ready
                t += 1300;
                tl.call(() => { r.url.textContent = "localhost:5173/export"; }, t);
                tl.add(r.badge, { opacity: 0, duration: 300 }, t);
                t = send(r.packetA, r.pReq, "POST /api/export", "req", t + 200);
                tl.call(() => this.log("POST /api/export", "req"), t);
                flash(t, COLORS.req);
                const queued = t + 150;
                send(r.packetB, r.pRes, "202 Accepted", "res", queued);
                t = send(r.packetA, r.pToWorker, "send_task()", "task", queued, 1200);
                tl.call(() => { this.log("202 task queued", "task"); r.workerStatus.textContent = "running export…"; }, t);
                tl.add(r.progress, { scaleX: [0, 1], duration: 1800, ease: "inOutQuad" }, t);
                t += 1800;
                tl.call(() => { r.workerStatus.textContent = "SUCCESS"; }, t);
                t = send(r.packetA, r.pFromWorker, "task done", "task", t + 100, 1200);
                tl.call(() => this.log("task SUCCESS", "res"), t);
                flash(t, COLORS.task);
                t = send(r.packetA, r.pRes, "📄 CSV ready", "res", t + 150);
                tl.call(() => { r.badgeText.textContent = "📄 export.csv"; }, t);
                tl.add(r.badge, { opacity: [0, 1], translateY: [8, 0], duration: 500, ease: "outBack(2)" }, t);
                tl.add(r.badge, { opacity: 0, duration: 400 }, t + 1600);

                return tl;
            },
        },
        mounted() {
            const reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
            const r = this.$refs;
            if (reduced) {
                this.logs = [
                    { id: 0, text: "GET /api/courses", kind: "req" },
                    { id: 1, text: "200 OK  42ms", kind: "res" },
                ];
                return;
            }

            set(r.scene.querySelectorAll(".sk-fill"), { scaleX: 0 });
            set(r.progress, { scaleX: 0 });

            this.anims = [
                // animate the children so the wrapper keeps its own CSS opacity/transform
                animate(r.scene.children, { opacity: [0, 1], translateY: [30, 0], duration: 1200, delay: stagger(150, { start: 900 }), ease: "outExpo" }),
                // data flowing along the wires
                animate(r.scene.querySelectorAll(".wire"), {
                    strokeDashoffset: [0, -24],
                    duration: 1200,
                    ease: "linear",
                    loop: true,
                }),
                animate(r.spinner, { rotate: 360, duration: 800, ease: "linear", loop: true }),
                animate(r.scene.querySelectorAll(".live-dot"), {
                    opacity: [1, 0.3],
                    duration: 700,
                    alternate: true,
                    loop: true,
                }),
            ];
            this.tl = this.buildTimeline();
            this.anims.push(this.tl);
        },
        beforeUnmount() {
            this.anims?.forEach((a) => a.pause());
        },
    };
</script>

<style scoped>
    .net-scene {
        position: relative;
        margin: 0;
        pointer-events: none;
    }

    .net-caption {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        font-size: .72rem;
        font-weight: 600;
        letter-spacing: .1em;
        text-transform: uppercase;
        color: #94a3b8;
        margin-bottom: 6px;
    }

    .live-dot {
        width: 7px;
        height: 7px;
        border-radius: 50%;
        background: #f87171;
        box-shadow: 0 0 8px #f87171;
    }

    svg {
        width: 100%;
        height: auto;
        overflow: visible;
        font-family: 'Inter', sans-serif;
    }

    svg * {
        transform-box: fill-box;
    }

    .wire {
        fill: none;
        stroke: rgba(148, 163, 184, .25);
        stroke-width: 1.5;
        stroke-dasharray: 4 8;
        stroke-linecap: round;
    }

    .panel {
        fill: url(#ns-panel);
        stroke: rgba(148, 163, 184, .25);
        stroke-width: 1;
    }

    .titlebar {
        fill: #273449;
    }

    .urlbar {
        fill: #0f172a;
    }

    .label {
        fill: #e2e8f0;
        font-size: 12px;
        font-weight: 600;
    }

    .mono {
        font-family: 'JetBrains Mono', monospace;
    }

    .tiny {
        font-size: 9.5px;
        fill: #94a3b8;
    }

    .dim {
        fill: #64748b;
    }

    .spin-track {
        fill: none;
        stroke: rgba(148, 163, 184, .25);
        stroke-width: 2;
    }

    .spin-arc {
        fill: none;
        stroke: #38bdf8;
        stroke-width: 2;
        stroke-linecap: round;
    }

    .spinner {
        transform-origin: center;
    }

    .sk-bg {
        fill: rgba(148, 163, 184, .12);
    }

    .sk-fill {
        fill: rgba(66, 184, 131, .55);
        transform-origin: left center;
    }

    .badge-bg {
        fill: rgba(66, 184, 131, .18);
        stroke: rgba(66, 184, 131, .6);
    }

    .badge-text {
        fill: #a7f3d0;
    }

    .led {
        fill: #22c55e;
        filter: url(#ns-glow);
    }

    .console {
        fill: #020617;
        stroke: rgba(148, 163, 184, .15);
    }

    .log.req {
        fill: #7dd3fc;
    }

    .log.res {
        fill: #86efac;
    }

    .log.task {
        fill: #c4b5fd;
    }

    .db {
        transform-origin: center;
    }

    .db-top {
        fill: #273449;
        stroke: rgba(148, 163, 184, .3);
    }

    .db-ring {
        fill: none;
        stroke: rgba(148, 163, 184, .2);
    }

    .progress {
        fill: #a78bfa;
        transform-origin: left center;
    }

    .packet-bg {
        fill: #0b1222;
        stroke-width: 1.5;
    }

    .packet {
        filter: url(#ns-glow);
    }

    .packet-text {
        font-weight: 500;
    }
</style>

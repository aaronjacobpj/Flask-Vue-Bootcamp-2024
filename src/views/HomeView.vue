<script setup>
  import { RouterLink } from "vue-router";
  import store from "@/store";
  import NetworkScene from "@/components/NetworkScene.vue";
  import { animate, createTimeline, createAnimatable, createDrawable, stagger, set, random, spring } from "animejs";
</script>

<template>
  <main>
    <div class="scroll-progress" ref="progress" aria-hidden="true"></div>

    <section class="hero" ref="hero" @mousemove="onHeroMove" @mouseleave="onHeroLeave">
      <div class="orbs" aria-hidden="true">
        <span class="orb orb-1"></span>
        <span class="orb orb-2"></span>
        <span class="orb orb-3"></span>
      </div>
      <div class="grid-bg" aria-hidden="true"></div>
      <div class="particles" aria-hidden="true">
        <span v-for="n in 36" class="particle"></span>
      </div>
      <div class="spotlight" ref="spotlight" aria-hidden="true"></div>

      <div class="hero-inner">
        <div class="hero-copy">
        <span class="hero-pill"><span class="pulse"></span>IITM · Modern Application Development II</span>
        <div class="title-wrap">
          <h1 class="hero-title" aria-label="Hi, there!">
            <span v-for="c in title" class="char" aria-hidden="true">{{ c === ' ' ? '\u00a0' : c }}</span>
            <span class="wave" aria-hidden="true">👋</span>
          </h1>
          <svg class="squiggle" viewBox="0 0 300 24" preserveAspectRatio="none" aria-hidden="true">
            <path d="M4 14 Q 40 2, 76 14 T 150 14 T 224 14 T 296 14" />
          </svg>
        </div>
        <p class="rotator">
          Build full-stack apps with
          <span class="rot-window"><span class="rot-word" ref="rotWord">{{ words[wordIndex] }}</span></span>
        </p>
        <p class="lead-text">
          This project helps students implement their projects with expertise. It dives deep
          into the architecture, design and implementation of web apps with Python, HTML, CSS,
          JavaScript, SQL and frameworks such as Vue, Flask and Celery — covering front-ends,
          database design, user experience and security.
        </p>
        <div class="stack">
          <span v-for="tech in stack" class="chip" @mouseenter="popChip" @mouseleave="unpopChip">{{ tech }}</span>
        </div>

        <div class="stats">
          <div v-for="stat in stats" class="stat">
            <span class="stat-value" :data-value="stat.value">0</span>
            <span class="stat-label">{{ stat.label }}</span>
          </div>
        </div>

        <div class="course-cards" v-if="courses.length">
          <RouterLink v-for="course in courses" class="course-card"
            :to="{name: 'course', params: {name: course['name'], term: term, year: year}}"
            @mousemove="tiltCard" @mouseleave="untiltCard">
            <span class="card-shine"></span>
            <span class="course-name">{{ course["name"] }}</span>
            <span class="course-meta">{{ course["sessions"].length }} sessions <span class="arrow">→</span></span>
          </RouterLink>
        </div>
        </div>
        <NetworkScene class="hero-scene" />
      </div>

      <button class="scroll-cue" type="button" @click="scrollToGuide" aria-label="Scroll to walkthrough">
        <span class="mouse"><span class="wheel"></span></span>
      </button>
    </section>

    <div class="page">
      <article class="guide card-surface" ref="guide">
        <h1 id="project-walk-through">Project Walk Through</h1>
        <p>After you go through the problem statement you can start with setting
          up the environment for the project, including creating a virtual
          environment in Flask or in Node. In our case we need both, so you
          can start with either Node or Python. So let's start!</p>

        <h2 id="setting-up-the-environments">Setting up the environments</h2>
        <h3 id="frontend"><span class="tag tag-vue">Frontend</span></h3>
        <p>Because we are using Vue 3 we need to make sure that we have Node up and
          running in our system.</p>
        <p>If you haven’t done so already, you can install it from
          <a href="https://nodejs.org/en/download">Node.js</a>.
        </p>
        <p>After installing Node.js, you can move on to creating the Vue project.</p>

        <h4 id="creating-vue-project">Creating Vue project</h4>
        <p>You can create the Vue project by running the command below. This will take
          care of creating the project and installing the basic packages that you
          need to start working on your project.</p>
        <pre><code>npm create vue@latest</code></pre>
        <p>The output looks something like this.</p>
        <figure class="shot"><img src="/images/vue-setup.png" alt="Output of npm create vue"></figure>
        <p>After that we can navigate to the frontend project folder.</p>
        <pre><code>cd &lt;project-name&gt;</code></pre>
        <p>Now that we are in the folder, we have to install the packages to move
          further. We can install all of them by running…</p>
        <pre><code>npm install</code></pre>
        <p>After installing the packages we can test out the project by running
          the development server.</p>
        <pre><code>npm run dev</code></pre>
        <p>Now our frontend project is ready for further modification.</p>
        <div class="callout">
          <strong>Tip:</strong> while developing the frontend you may need new packages.
          Just like in Python, installing a package in Node is quite straightforward.
        </div>
        <pre><code>npm install &lt;package-name@version&gt;</code></pre>

        <h3 id="how-the-code-would-look-like">How would the code look?</h3>
        <h4 id="backend"><span class="tag tag-flask">Backend</span></h4>
        <p><a href="https://flask.palletsprojects.com/en/stable/quickstart/#apis-with-json">Reference ↗</a></p>
        <pre data-lang="python"><code>@app.route(&quot;/&lt;url&gt;&quot;, methods=[&quot;&lt;method-type&gt;&quot;])
def function_name():
    # get data from the user like form or json
    # do necessary validation for each data attribute
    # send appropriate response
    # if the form is valid modify database if needed.
    # return the final response</code></pre>
        <h4 id="frontend-1"><span class="tag tag-vue">Frontend</span></h4>
        <p><a href="https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch">Reference ↗</a></p>
        <pre data-lang="javascript"><code>fetch(&quot;&lt;url&gt;&quot;, {
    headers: {
        &quot;Content-Type&quot;: &quot;type of data you are sending&quot;
        // https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Content-Type
        &quot;Authentication-Token&quot;: &lt;token&gt;
        // https://flask-security-too.readthedocs.io/en/stable/configuration.html#SECURITY_TOKEN_AUTHENTICATION_HEADER
    }
}).then(r =&gt; {
    if(r.status == 200){
        r.json().then(x =&gt; {
            // do something with the data
        })
    }
})</code></pre>
      </article>
    </div>
  </main>
</template>

<script>
  export default {
    props: ["year", "term"],
    data() {
      return {
        title: "Hi, there!",
        words: ["Flask", "Vue 3", "Celery", "SQLAlchemy", "Redis", "REST APIs"],
        wordIndex: 0,
        stack: ["Python", "Flask", "Vue 3", "SQL", "Celery", "HTML & CSS", "JavaScript"]
      };
    },
    computed: {
      courses() {
        if (!this.year || !this.term) return [];
        return store.getters.filterCourses(this.year, this.term);
      },
      stats() {
        const all = store.getters.getCourses;
        return [
          { label: "Years", value: new Set(all.map((c) => c.year)).size },
          { label: "Cohorts", value: all.length },
          { label: "Sessions", value: all.reduce((n, c) => n + c.sessions.length, 0) },
          { label: "Technologies", value: this.stack.length },
        ];
      }
    },
    watch: {
      // HomeView is reused between "/" and "/:year/:term", so animate cards that appear later
      courses() {
        if (this.reducedMotion) return;
        this.$nextTick(() => this.animateCards(0));
      }
    },
    methods: {
      q(sel) {
        return this.$refs.hero.querySelectorAll(sel);
      },
      animateCards(delay) {
        return animate(this.q(".course-card"), {
          opacity: [0, 1],
          translateY: [40, 0],
          rotateX: [-25, 0],
          scale: [0.92, 1],
          delay: stagger(110, { start: delay }),
          duration: 900,
          ease: "outExpo",
        });
      },
      countUp(el, delay = 0) {
        const counter = { v: 0 };
        const target = Number(el.dataset.value);
        animate(counter, {
          v: target,
          delay,
          duration: 1800,
          ease: "outExpo",
          onUpdate: () => { el.textContent = Math.round(counter.v); },
        });
      },
      rotateWord() {
        const el = this.$refs.rotWord;
        if (!el) return;
        animate(el, {
          translateY: [0, "-110%"],
          opacity: [1, 0],
          rotateX: [0, 70],
          duration: 400,
          ease: "inQuad",
          onComplete: () => {
            this.wordIndex = (this.wordIndex + 1) % this.words.length;
            animate(el, {
              translateY: ["110%", 0],
              opacity: [0, 1],
              rotateX: [-70, 0],
              duration: 700,
              ease: "outBack(1.6)",
            });
          },
        });
      },
      onHeroMove(e) {
        if (!this.spot) return;
        const r = this.$refs.hero.getBoundingClientRect();
        this.spot.translateX(e.clientX - r.left - 200);
        this.spot.translateY(e.clientY - r.top - 200);
        this.spot.opacity(1);
        // subtle parallax on the background layers
        const dx = (e.clientX - r.left) / r.width - 0.5;
        const dy = (e.clientY - r.top) / r.height - 0.5;
        this.parallax.translateX(dx * -30);
        this.parallax.translateY(dy * -20);
      },
      onHeroLeave() {
        this.spot?.opacity(0);
        this.parallax?.translateX(0);
        this.parallax?.translateY(0);
      },
      popChip(e) {
        if (this.reducedMotion || !this.chipsReady) return;
        animate(e.currentTarget, {
          scale: 1.15,
          rotate: random(-6, 6),
          ease: spring({ stiffness: 260, damping: 10 }),
        });
      },
      unpopChip(e) {
        if (this.reducedMotion || !this.chipsReady) return;
        animate(e.currentTarget, { scale: 1, rotate: 0, ease: spring({ stiffness: 200, damping: 12 }) });
      },
      tiltCard(e) {
        if (this.reducedMotion) return;
        const card = e.currentTarget;
        const r = card.getBoundingClientRect();
        const x = (e.clientX - r.left) / r.width - 0.5;
        const y = (e.clientY - r.top) / r.height - 0.5;
        animate(card, { rotateY: x * 16, rotateX: y * -16, scale: 1.04, duration: 400, ease: "outQuad" });
        animate(card.querySelector(".card-shine"), {
          opacity: 1,
          translateX: (x + 0.5) * r.width - 100,
          translateY: (y + 0.5) * r.height - 100,
          duration: 300,
          ease: "outQuad",
        });
      },
      untiltCard(e) {
        if (this.reducedMotion) return;
        const card = e.currentTarget;
        animate(card, { rotateY: 0, rotateX: 0, scale: 1, ease: spring({ stiffness: 120, damping: 9 }) });
        animate(card.querySelector(".card-shine"), { opacity: 0, duration: 400 });
      },
      scrollToGuide() {
        this.$refs.guide.scrollIntoView({ behavior: "smooth", block: "start" });
      },
      onScroll() {
        const doc = document.documentElement;
        const max = doc.scrollHeight - doc.clientHeight;
        this.$refs.progress.style.transform = `scaleX(${max > 0 ? doc.scrollTop / max : 0})`;
      },
      typeOut(code) {
        const text = code.textContent;
        code.textContent = "";
        code.parentElement.classList.add("typing");
        const state = { n: 0 };
        animate(state, {
          n: text.length,
          duration: Math.min(1400, 40 * text.length),
          ease: "linear",
          onUpdate: () => { code.textContent = text.slice(0, Math.round(state.n)); },
          onComplete: () => {
            code.textContent = text;
            setTimeout(() => code.parentElement.classList.remove("typing"), 1200);
          },
        });
      },
      setupReveal() {
        const guide = this.$refs.guide;
        const reveal = guide.querySelectorAll("h1, h2, h3, h4, p, pre, .shot, .callout");
        set(reveal, { opacity: 0, translateY: 30 });
        set(guide.querySelectorAll("h2, h3, h4"), { translateX: -40, translateY: 0 });
        set(guide.querySelectorAll(".shot"), { scale: 0.85, rotateX: 18, translateY: 60 });

        this.observer = new IntersectionObserver((entries) => {
          const visible = entries.filter((e) => e.isIntersecting).map((e) => e.target);
          if (!visible.length) return;
          visible.forEach((el) => this.observer.unobserve(el));
          animate(visible, {
            opacity: 1,
            translateY: 0,
            translateX: 0,
            scale: 1,
            rotateX: 0,
            delay: stagger(90),
            duration: 900,
            ease: "outExpo",
          });
          visible.forEach((el, i) => {
            if (el.matches("h2")) {
              animate(el, { "--underline": [0, 1], delay: i * 90 + 200, duration: 900, ease: "outExpo" });
            }
            if (el.matches(".callout")) {
              animate(el, { borderLeftWidth: [0, 4], backgroundPosition: ["100% 0", "0% 0"], delay: i * 90, duration: 1200, ease: "outExpo" });
            }
            if (el.matches("pre")) {
              const code = el.querySelector("code");
              if (code.textContent.length < 60) setTimeout(() => this.typeOut(code), i * 90 + 250);
            }
          });
        }, { threshold: 0.2 });
        reveal.forEach((el) => this.observer.observe(el));
      },
    },
    mounted() {
      this.reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
      this.loops = [];

      this.onScroll();
      this._onScroll = () => this.onScroll();
      window.addEventListener("scroll", this._onScroll, { passive: true });

      if (this.reducedMotion) {
        this.q(".stat-value").forEach((el) => { el.textContent = el.dataset.value; });
        return;
      }

      // Hero intro choreography
      const drawable = createDrawable(this.q(".squiggle path"));
      this.intro = createTimeline({ defaults: { duration: 800, ease: "outExpo" } })
        .add(this.q(".hero-pill"), { opacity: [0, 1], translateY: [-20, 0], scale: [0.6, 1], ease: "outBack(2)" })
        .add(this.q(".char"), {
          opacity: [0, 1],
          translateY: [80, 0],
          rotateZ: [() => random(-40, 40), 0],
          scale: [0.3, 1],
          delay: stagger(45),
          duration: 1100,
          ease: "outElastic(1, .6)",
        }, "-=500")
        .add(this.q(".wave"), {
          opacity: [0, 1],
          scale: [0, 1.2, 1],
          rotate: [0, 18, -10, 18, -6, 12, 0],
          duration: 1800,
          ease: "inOutSine",
        }, "-=900")
        .add(drawable, { draw: ["0 0", "0 1"], duration: 1200, ease: "inOutQuart" }, "-=1500")
        .add(this.q(".rotator"), { opacity: [0, 1], translateX: [-30, 0] }, "-=900")
        .add(this.q(".lead-text"), { opacity: [0, 1], translateY: [20, 0], filter: ["blur(8px)", "blur(0px)"] }, "-=600")
        .add(this.q(".chip"), {
          opacity: [0, 1],
          translateY: [30, 0],
          scale: [0.4, 1],
          rotate: [() => random(-20, 20), 0],
          delay: stagger(60, { from: "center" }),
          ease: "outBack(2.5)",
          duration: 700,
        }, "-=600")
        .add(this.q(".stat"), {
          opacity: [0, 1],
          translateY: [30, 0],
          delay: stagger(100),
          onBegin: () => this.q(".stat-value").forEach((el, i) => this.countUp(el, i * 100)),
        }, "-=400")
        .add(this.q(".scroll-cue"), { opacity: [0, 1], translateY: [-10, 0] }, "-=300")
        .add(this.$refs.guide, { opacity: [0, 1], translateY: [80, 0], scale: [0.96, 1], duration: 1200 }, "-=900")
        .call(() => {
          this.chipsReady = true;
          // gentle idle bobbing for the chips once they've landed
          this.q(".chip").forEach((chip, i) => {
            this.loops.push(animate(chip, {
              translateY: [0, -6],
              duration: 1600 + (i % 3) * 300,
              delay: i * 120,
              ease: "inOutSine",
              loop: true,
              alternate: true,
            }));
          });
        });

      if (this.courses.length) this.animateCards(1600);

      // Pulsing status dot on the pill
      this.loops.push(animate(this.q(".pulse"), {
        scale: [1, 2.4],
        opacity: [0.8, 0],
        duration: 1600,
        ease: "outQuad",
        loop: true,
      }));

      // Scroll cue wheel
      this.loops.push(animate(this.q(".wheel"), {
        translateY: [0, 10],
        opacity: [1, 0],
        duration: 1400,
        ease: "inOutQuad",
        loop: true,
      }));

      // Drifting glow orbs
      this.q(".orb").forEach((orb, i) => {
        this.loops.push(animate(orb, {
          translateX: [0, (i % 2 ? -1 : 1) * (80 + i * 40)],
          translateY: [0, (i % 2 ? 1 : -1) * (60 + i * 30)],
          scale: [1, 1.3],
          duration: 5000 + i * 1500,
          ease: "inOutSine",
          loop: true,
          alternate: true,
        }));
      });

      // Floating particle field
      const hero = this.$refs.hero;
      this.q(".particle").forEach((p) => {
        set(p, {
          left: `${random(0, 100)}%`,
          top: `${random(0, 100)}%`,
          width: random(2, 6),
          height: random(2, 6),
          opacity: random(0.15, 0.7, 2),
        });
        this.loops.push(animate(p, {
          translateX: () => random(-80, 80),
          translateY: () => random(-120, 40),
          opacity: [() => random(0.1, 0.3, 2), () => random(0.5, 0.9, 2)],
          duration: () => random(4000, 9000),
          delay: () => random(0, 2000),
          ease: "inOutSine",
          loop: true,
          alternate: true,
        }));
      });

      // Slowly drifting grid
      this.loops.push(animate(this.q(".grid-bg"), {
        backgroundPosition: ["0px 0px", "48px 48px"],
        duration: 6000,
        ease: "linear",
        loop: true,
      }));

      // Heading letters do a little wave every few seconds
      this.loops.push(animate(this.q(".char"), {
        translateY: [0, -12, 0],
        delay: stagger(60, { start: 3500 }),
        loopDelay: 4000,
        duration: 700,
        ease: "inOutSine",
        loop: true,
      }));

      // Mouse-follow spotlight + background parallax
      this.spot = createAnimatable(this.$refs.spotlight, {
        translateX: 700, translateY: 700, opacity: 500, ease: "out(3)",
      });
      this.parallax = createAnimatable(hero.querySelectorAll(".orbs, .particles, .grid-bg"), {
        translateX: 1200, translateY: 1200, ease: "out(4)",
      });

      this.wordTimer = setInterval(() => this.rotateWord(), 2600);

      this.setupReveal();
    },
    beforeUnmount() {
      window.removeEventListener("scroll", this._onScroll);
      clearInterval(this.wordTimer);
      this.observer?.disconnect();
      this.intro?.pause();
      this.loops?.forEach((a) => a.pause());
    }
  }
</script>

<style scoped>
  .hero {
    position: relative;
    overflow: hidden;
    background:
      radial-gradient(1000px 400px at 85% -10%, rgba(66, 184, 131, .35), transparent 60%),
      radial-gradient(800px 400px at -10% 110%, rgba(53, 73, 94, .7), transparent 60%),
      #0f172a;
    color: #cbd5e1;
    padding: 72px 20px 80px;
  }

  .hero-inner {
    position: relative;
    max-width: 960px;
    margin: 0 auto;
  }

  .hero-pill {
    display: inline-block;
    font-size: .8rem;
    font-weight: 500;
    color: #a7f3d0;
    background: rgba(66, 184, 131, .15);
    border: 1px solid rgba(66, 184, 131, .35);
    padding: 5px 12px;
    border-radius: 999px;
    margin-bottom: 20px;
  }

  .hero h1 {
    color: #fff;
    font-size: clamp(2.25rem, 6vw, 3.5rem);
    font-weight: 800;
    margin: 0 0 16px;
  }

  .wave {
    display: inline-block;
    transform-origin: 70% 70%;
  }

  .orbs {
    position: absolute;
    inset: 0;
    pointer-events: none;
  }

  .orb {
    position: absolute;
    border-radius: 50%;
    filter: blur(60px);
    opacity: .55;
  }

  .orb-1 {
    width: 320px;
    height: 320px;
    top: -80px;
    right: 8%;
    background: rgba(66, 184, 131, .55);
  }

  .orb-2 {
    width: 260px;
    height: 260px;
    bottom: -100px;
    left: 4%;
    background: rgba(56, 189, 248, .35);
  }

  .orb-3 {
    width: 200px;
    height: 200px;
    top: 40%;
    left: 45%;
    background: rgba(129, 140, 248, .3);
  }

  .lead-text {
    font-size: 1.125rem;
    line-height: 1.7;
    max-width: 680px;
    color: #cbd5e1;
  }

  .stack {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-top: 24px;
  }

  .chip {
    font-size: .8rem;
    font-weight: 500;
    color: #e2e8f0;
    background: rgba(255, 255, 255, .06);
    border: 1px solid rgba(255, 255, 255, .12);
    padding: 5px 12px;
    border-radius: 8px;
  }

  .course-cards {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
    gap: 14px;
    margin-top: 36px;
  }

  .course-card {
    display: flex;
    flex-direction: column;
    gap: 6px;
    padding: 18px 20px;
    border-radius: var(--radius);
    background: rgba(255, 255, 255, .06);
    border: 1px solid rgba(255, 255, 255, .12);
    text-decoration: none;
    transition: transform .15s, background .15s, border-color .15s;
  }

  .course-card:hover {
    transform: translateY(-2px);
    background: rgba(66, 184, 131, .14);
    border-color: rgba(66, 184, 131, .5);
  }

  .course-name {
    color: #fff;
    font-weight: 600;
    font-size: 1.05rem;
  }

  .course-meta {
    color: #a7f3d0;
    font-size: .85rem;
  }

  .page {
    margin-top: -40px;
    position: relative;
  }

  .guide {
    padding: clamp(24px, 5vw, 48px);
    line-height: 1.75;
    font-size: 1.02rem;
  }

  .guide h1 {
    margin-top: 0;
    font-size: 2rem;
  }

  .guide h2 {
    font-size: 1.5rem;
    margin-top: 2.2em;
    padding-bottom: .4em;
    border-bottom: 1px solid var(--line);
  }

  .guide h3 {
    font-size: 1.2rem;
    margin-top: 1.8em;
  }

  .guide h4 {
    font-size: 1.05rem;
    margin-top: 1.6em;
  }

  .tag {
    display: inline-block;
    font-size: .85rem;
    font-weight: 600;
    padding: 3px 10px;
    border-radius: 6px;
  }

  .tag-vue {
    color: var(--vue-dark);
    background: var(--accent-soft);
  }

  .tag-flask {
    color: var(--flask);
    background: #e7edf3;
  }

  .guide pre {
    position: relative;
    background: #0f172a;
    color: #e2e8f0;
    padding: 18px 20px;
    border-radius: 10px;
    font-size: .875rem;
    line-height: 1.6;
    overflow-x: auto;
    margin: 1em 0 1.4em;
    border-left: 3px solid var(--vue);
  }

  .guide pre[data-lang]::before {
    content: attr(data-lang);
    position: absolute;
    top: 8px;
    right: 12px;
    font-size: .7rem;
    text-transform: uppercase;
    letter-spacing: .08em;
    color: #64748b;
  }

  .guide pre code {
    color: inherit;
    white-space: pre;
  }

  .shot {
    margin: 1em 0 1.4em;
  }

  .shot img {
    max-width: 100%;
    border-radius: 10px;
    border: 1px solid var(--line);
    box-shadow: var(--shadow-md);
  }

  .callout {
    background: var(--accent-soft);
    border-left: 3px solid var(--vue);
    padding: 12px 16px;
    border-radius: 8px;
    color: var(--ink-soft);
    margin: 1.2em 0 .4em;
  }

  @media (max-width: 600px) {
    .hero {
      padding: 48px 16px 64px;
    }

    .page {
      padding-left: 16px;
      padding-right: 16px;
    }
  }
  /* ---------- behind-the-scenes diagram ---------- */
  .hero-copy {
    position: relative;
    z-index: 1;
  }

  .hero-scene {
    position: absolute;
    top: 50%;
    right: -8%;
    width: min(620px, 100%);
    transform: translateY(-50%);
    opacity: .16;
    z-index: 0;
  }

  @media (min-width: 1100px) {
    .hero-inner {
      max-width: 1240px;
      display: grid;
      grid-template-columns: minmax(0, 1.05fr) minmax(0, .95fr);
      gap: 48px;
      align-items: center;
    }

    .hero-scene {
      position: relative;
      top: auto;
      right: auto;
      width: 100%;
      transform: none;
      opacity: 1;
    }

    .page {
      max-width: 1000px;
    }
  }

  /* ---------- animation extras ---------- */
  .scroll-progress {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
    z-index: 2000;
    transform-origin: 0 50%;
    transform: scaleX(0);
    background: linear-gradient(90deg, var(--vue), #38bdf8, #818cf8);
  }

  .hero {
    min-height: calc(100vh - 65px);
    display: flex;
    flex-direction: column;
    justify-content: center;
  }

  .hero-inner {
    width: 100%;
    z-index: 1;
  }

  .hero-pill, .rotator, .lead-text, .chip, .stat, .course-card, .scroll-cue, .char, .wave {
    will-change: transform, opacity;
  }

  .hero-pill {
    position: relative;
    display: inline-flex;
    align-items: center;
    gap: 8px;
  }

  .pulse {
    position: relative;
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: var(--vue);
    box-shadow: 0 0 0 0 var(--vue);
  }

  .grid-bg {
    position: absolute;
    inset: -60px;
    background-image:
      linear-gradient(rgba(255, 255, 255, .04) 1px, transparent 1px),
      linear-gradient(90deg, rgba(255, 255, 255, .04) 1px, transparent 1px);
    background-size: 48px 48px;
    mask-image: radial-gradient(ellipse at 50% 40%, #000 30%, transparent 75%);
    -webkit-mask-image: radial-gradient(ellipse at 50% 40%, #000 30%, transparent 75%);
    pointer-events: none;
  }

  .particles {
    position: absolute;
    inset: 0;
    pointer-events: none;
  }

  .particle {
    position: absolute;
    border-radius: 50%;
    background: #a7f3d0;
    box-shadow: 0 0 8px rgba(167, 243, 208, .8);
  }

  .spotlight {
    position: absolute;
    top: 0;
    left: 0;
    width: 400px;
    height: 400px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(66, 184, 131, .22), transparent 65%);
    pointer-events: none;
    opacity: 0;
  }

  @media (hover: none) {
    .spotlight {
      display: none;
    }
  }

  .title-wrap {
    position: relative;
    display: block;
    width: fit-content;
    margin-bottom: 8px;
  }

  .hero-title {
    display: flex;
    flex-wrap: wrap;
    align-items: baseline;
    perspective: 600px;
  }

  .char {
    display: inline-block;
    background: linear-gradient(180deg, #fff 30%, #a7f3d0);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
  }

  .wave {
    margin-left: .3em;
  }

  .squiggle {
    position: absolute;
    left: 0;
    bottom: -6px;
    width: 72%;
    height: 18px;
    overflow: visible;
  }

  .squiggle path {
    fill: none;
    stroke: var(--vue);
    stroke-width: 4;
    stroke-linecap: round;
    filter: drop-shadow(0 0 6px rgba(66, 184, 131, .7));
  }

  .rotator {
    font-size: clamp(1.1rem, 2.5vw, 1.4rem);
    font-weight: 600;
    color: #e2e8f0;
    margin: 4px 0 18px;
  }

  .rot-window {
    display: inline-block;
    vertical-align: bottom;
    overflow: hidden;
    perspective: 400px;
    padding: 0 2px;
  }

  .rot-word {
    display: inline-block;
    color: var(--vue);
    background: linear-gradient(90deg, var(--vue), #38bdf8);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
    transform-origin: 50% 50% -20px;
  }

  .chip {
    display: inline-block;
    cursor: default;
    transition: border-color .2s, background .2s, color .2s;
  }

  .chip:hover {
    color: #fff;
    border-color: rgba(66, 184, 131, .6);
    background: rgba(66, 184, 131, .18);
  }

  .stats {
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: 14px;
    margin-top: 32px;
    max-width: 640px;
  }

  .stat {
    display: flex;
    flex-direction: column;
    padding: 14px 16px;
    border-radius: 12px;
    background: rgba(255, 255, 255, .04);
    border: 1px solid rgba(255, 255, 255, .08);
  }

  .stat-value {
    font-size: clamp(1.5rem, 4vw, 2.1rem);
    font-weight: 800;
    color: #fff;
    font-variant-numeric: tabular-nums;
    line-height: 1.1;
  }

  .stat-label {
    font-size: .75rem;
    text-transform: uppercase;
    letter-spacing: .08em;
    color: #94a3b8;
  }

  @media (max-width: 600px) {
    .stats {
      grid-template-columns: repeat(2, minmax(0, 1fr));
    }
  }

  .course-cards {
    perspective: 900px;
  }

  .course-card {
    position: relative;
    overflow: hidden;
    transform-style: preserve-3d;
  }

  .course-card:hover {
    transform: none;
  }

  .card-shine {
    position: absolute;
    top: 0;
    left: 0;
    width: 200px;
    height: 200px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(255, 255, 255, .18), transparent 65%);
    opacity: 0;
    pointer-events: none;
  }

  .arrow {
    display: inline-block;
    transition: transform .25s;
  }

  .course-card:hover .arrow {
    transform: translateX(6px);
  }

  .scroll-cue {
    position: relative;
    align-self: center;
    margin-top: 40px;
    border: 0;
    background: none;
    padding: 8px;
    z-index: 1;
    opacity: 0;
  }

  .mouse {
    display: block;
    width: 24px;
    height: 38px;
    border: 2px solid rgba(255, 255, 255, .45);
    border-radius: 14px;
    position: relative;
  }

  .wheel {
    position: absolute;
    top: 7px;
    left: 50%;
    width: 4px;
    height: 8px;
    margin-left: -2px;
    border-radius: 2px;
    background: #fff;
  }

  .guide {
    perspective: 900px;
  }

  .guide h2 {
    position: relative;
    border-bottom: 0;
    --underline: 1;
  }

  .guide h2::after {
    content: "";
    position: absolute;
    left: 0;
    right: 0;
    bottom: 0;
    height: 2px;
    background: linear-gradient(90deg, var(--vue), #38bdf8, transparent);
    transform-origin: 0 50%;
    transform: scaleX(var(--underline));
  }

  .callout {
    background: linear-gradient(90deg, var(--accent-soft) 50%, transparent 50%);
    background-size: 200% 100%;
    background-position: 0% 0;
  }

  .guide pre.typing code::after {
    content: "▋";
    margin-left: 2px;
    color: var(--vue);
    animation: blink 1s steps(1) infinite;
  }

  @keyframes blink {
    50% { opacity: 0; }
  }

  @media (prefers-reduced-motion: reduce) {
    .scroll-cue {
      opacity: 1;
    }
  }
</style>
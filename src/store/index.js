import { createStore } from "vuex";
import {default as flaskj24} from "@/assets/2024/Flask/January.json";
import {default as vuej24} from "@/assets/2024/Vue/January.json";
import {default as flaskm24} from "@/assets/2024/Flask/March.json";
import {default as vuem24} from "@/assets/2024/Vue/March.json";
import {default as vuejuly24} from "@/assets/2024/Vue/July.json";
import {default as flasks24} from "@/assets/2024/Flask/September.json";
import {default as vues24} from "@/assets/2024/Vue/September.json";
import {default as vuen24} from "@/assets/2024/Vue/November.json";
import {default as flaskj25} from "@/assets/2025/Flask/January.json";
import {default as vuemarch25} from "@/assets/2025/Vue/March.json";
import {default as vuemayeve25} from "@/assets/2025/Vue/MayEve.json";
import {default as flaskmay25} from "@/assets/2025/Flask/MayM.json";
import {default as vuemaymorn25} from "@/assets/2025/Vue/MayMorn.json";
import {default as vuejulym25} from "@/assets/2025/Vue/JulyM.json";
import {default as vuejulye25} from "@/assets/2025/Vue/JulyE.json";
import {default as vueOct25} from "@/assets/2025/Vue/October.json";
import {default as vuejunem26} from "@/assets/2026/Vue/JuneM.json";
import {default as vuejunee26} from "@/assets/2026/Vue/JuneE.json";

const store = createStore({
    state() {
        return {
            courses: [
                flaskj24,
                vuej24,
                flaskm24,
                vuem24,
                vuejuly24,
                flasks24,
                vues24,
                vuen24,
                flaskj25,
                vuemarch25,
                vuemayeve25,
                flaskmay25,
                vuemaymorn25,
                vuejulym25,
                vuejulye25,
                vueOct25,
                vuejunem26,
                vuejunee26,
            ]
        }
    },
    getters: {
        getCourses(state) {
            return state.courses;
        },
        filterCourses: (state) => (year, term) => {
            return state.courses.filter(x => x["year"] == year && x["term"] == term)
        }
    }
})

export default store;
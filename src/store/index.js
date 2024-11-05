import { createStore } from "vuex";
import {default as flaskj24} from "@/assets/2024/Flask/January.json";
import {default as vuej24} from "@/assets/2024/Vue/January.json";
import {default as flaskm24} from "@/assets/2024/Flask/March.json";
import {default as vuem24} from "@/assets/2024/Vue/March.json";
import {default as vuejuly24} from "@/assets/2024/Vue/July.json";
import {default as flasks24} from "@/assets/2024/Flask/September.json";
import {default as vues24} from "@/assets/2024/Vue/September.json";

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
                {
                    name: "Vue",
                    "base-url": "/weeks/bootcamp/2024/November/MAD ll/",
                    term: "November",
                    year: 2024,
                    sessions: [
                        {
                            "source-code": "day0.zip",
                            "youtube-video-id": "MS7qnmIJjfg",
                            "notes": "",
                            "slides": "",
                            "name": "Web Development Bootcamp Using Flask and Vue - Day 0"
                        },
                        {
                            "source-code": "day1.zip",
                            "youtube-video-id": "QMDiaSZ5eNc",
                            "notes": "",
                            "slides": "",
                            "name": "Web Development Bootcamp Using Flask and Vue - Day 1"
                        },
                    ]
                }

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
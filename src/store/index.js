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
                        {
                            "source-code": "day2.zip",
                            "youtube-video-id": "H5CJmEVwBY0",
                            "notes": "",
                            "slides": "",
                            "name": "Web Development Bootcamp Using Flask and Vue - Day 2"
                        },
                        {
                            "source-code": "day3.zip",
                            "youtube-video-id": "d5qhNjwgMzA",
                            "notes": "",
                            "slides": "",
                            "name": "Web Development Bootcamp Using Flask and Vue - Day 3"
                        },
                        {
                            "source-code": "day4.zip",
                            "youtube-video-id": "mzn-dTY72Zg",
                            "notes": "",
                            "slides": "",
                            "name": "Web Development Bootcamp Using Flask and Vue - Day 4"
                        },
                        {
                            "source-code": "day5.zip",
                            "youtube-video-id": "MfCkRzA_r1c",
                            "notes": "",
                            "slides": "",
                            "name": "Web Development Bootcamp Using Flask and Vue - Day 5"
                        },
                        {
                            "source-code": "day6.zip",
                            "youtube-video-id": "WS_UOnStPgQ",
                            "notes": "",
                            "slides": "",
                            "name": "Web Development Bootcamp Using Flask and Vue - Day 6"
                        },
                        {
                            "source-code": "day7.zip",
                            "youtube-video-id": "8xj-XPgLS_M",
                            "notes": "",
                            "slides": "",
                            "name": "Web Development Bootcamp Using Flask and Vue - Day 7"
                        },
                        {
                            "source-code": "day8.zip",
                            "youtube-video-id": "dP_SXI43LMQ",
                            "notes": "",
                            "slides": "",
                            "name": "Web Development Bootcamp Using Flask and Vue - Day 8"
                        },
                        {
                            "source-code": "day9.zip",
                            "youtube-video-id": "3DdrlLEdG54",
                            "notes": "",
                            "slides": "",
                            "name": "Web Development Bootcamp Using Flask and Vue - Day 9"
                        },
                        {
                            "source-code": "day10.zip",
                            "youtube-video-id": "y1RWmw2UYAQ",
                            "notes": "",
                            "slides": "",
                            "name": "Web Development Bootcamp Using Flask and Vue - Day 10"
                        },
                        {
                            "source-code": "day11.zip",
                            "youtube-video-id": "GDMmVEdwvmA",
                            "notes": "",
                            "slides": "",
                            "name": "Web Development Bootcamp Using Flask and Vue - Day 11"
                        },
                        {
                            "source-code": "day12.zip",
                            "youtube-video-id": "GDMmVEdwvmA",
                            "notes": "",
                            "slides": "",
                            "name": "Web Development Bootcamp Using Flask and Vue - Day 12 (Appologies the video export failed.)"
                        },
                        {
                            "source-code": "caching-and-celery-old.zip",
                            "youtube-video-id": "COTr9u2Eb5I",
                            "notes": "",
                            "slides": "",
                            "name": "Caching and Celery"
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
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
                {
                    "name": "Vue (Evening)",
                    "base-url": "/weeks/bootcamp/2025/May/MAD ll (Evening)/",
                    "term": "May",
                    "year": 2025,
                    "sessions": [
                            {
                                "source-code": "",
                                "youtube-video-id": "1EoJMBCbCR4",
                                "notes": "",
                                "slides": "",
                                "name": "Web Development Bootcamp Using Flask and Vue - Git"
                            },
                            {
                                "source-code": "day0.zip",
                                "youtube-video-id": "f1gLzgGHqgo",
                                "notes": "",
                                "slides": "",
                                "name": "Web Development Bootcamp Using Flask and Vue - Day 0"
                            },
                            {
                                "source-code": "day1.zip",
                                "youtube-video-id": "LB-8mliWeJ8",
                                "notes": "",
                                "slides": "",
                                "name": "Web Development Bootcamp Using Flask and Vue - Day 1"
                            },
                            {
                                "source-code": "day2.zip",
                                "youtube-video-id": "djaDEgL8tn8",
                                "notes": "",
                                "slides": "",
                                "name": "Web Development Bootcamp Using Flask and Vue - Day 2"
                            },
                            {
                                "source-code": "day3.zip",
                                "youtube-video-id": "JMyLmmtGH4U",
                                "notes": "",
                                "slides": "",
                                "name": "Web Development Bootcamp Using Flask and Vue - Day 3"
                            },
                            {
                                "source-code": "day4.zip",
                                "youtube-video-id": "aXYOpuKnvl8",
                                "notes": "",
                                "slides": "",
                                "name": "Web Development Bootcamp Using Flask and Vue - Day 4"
                            },
                            {
                                "source-code": "day5.zip",
                                "youtube-video-id": "XOunq7Q7XdY",
                                "notes": "",
                                "slides": "",
                                "name": "Web Development Bootcamp Using Flask and Vue - Day 5"
                            },
                            {
                                "source-code": "day6.zip",
                                "youtube-video-id": "mY_bzUVn-Ls",
                                "notes": "",
                                "slides": "",
                                "name": "Web Development Bootcamp Using Flask and Vue - Day 6"
                            },
                            {
                                "source-code": "day7.zip",
                                "youtube-video-id": "mNEjgqWVyb0",
                                "notes": "",
                                "slides": "",
                                "name": "Web Development Bootcamp Using Flask and Vue - Day 7"
                            },
                            {
                                "source-code": "day8.zip",
                                "youtube-video-id": "GW3oE5dFvnM",
                                "notes": "",
                                "slides": "",
                                "name": "Web Development Bootcamp Using Flask and Vue - Day 8"
                            },
                            {
                                "source-code": "day9.zip",
                                "youtube-video-id": "h55iD4apiIg",
                                "notes": "",
                                "slides": "",
                                "name": "Web Development Bootcamp Using Flask and Vue - Day 9"
                            }
                    ]
                },
                {
                    "name": "Flask",
                    "base-url": "/weeks/bootcamp/2025/May/MAD l/",
                    "term": "May",
                    "year": 2025,
                    "sessions": [
                            {
                                "source-code": "",
                                "youtube-video-id": "1EoJMBCbCR4",
                                "notes": "",
                                "slides": "",
                                "name": "Web Development Bootcamp Using Flask and HTML - Git"
                            },
                            {
                                "source-code": "day0.zip",
                                "youtube-video-id": "euEnbr_TJiI",
                                "notes": "",
                                "slides": "",
                                "name": "Web Development Bootcamp Using Flask and HTML - Day 0 (HTML and CSS)"
                            },
                            {
                                "source-code": "day1.zip",
                                "youtube-video-id": "gznd3flAwv0",
                                "notes": "",
                                "slides": "",
                                "name": "Web Development Bootcamp Using Flask and HTML - Day 1 (Flask)"
                            },
                            {
                                "source-code": "day2.zip",
                                "youtube-video-id": "dxg7ly-zp-w",
                                "notes": "",
                                "slides": "",
                                "name": "Web Development Bootcamp Using Flask and HTML - Day 2 (Models)"
                            },
                            {
                                "source-code": "day3.zip",
                                "youtube-video-id": "qcjYVc-4Zcw",
                                "notes": "",
                                "slides": "",
                                "name": "Web Development Bootcamp Using Flask and HTML - Day 3 (Session)"
                            },
                            {
                                "source-code": "day4.zip",
                                "youtube-video-id": "Gdgt658royQ",
                                "notes": "",
                                "slides": "",
                                "name": "Web Development Bootcamp Using Flask and HTML - Day 4 (CRUD Operations)"
                            },
                            {
                                "source-code": "day5.zip",
                                "youtube-video-id": "9enErb_TGC0",
                                "notes": "",
                                "slides": "",
                                "name": "Web Development Bootcamp Using Flask and HTML - Day 5 (CRUD Operations)"
                            },
                    ]
                },
                {
                    "name": "Vue (Morning)",
                    "base-url": "/weeks/bootcamp/2025/May/MAD ll (Morning)/",
                    "term": "May",
                    "year": 2025,
                    "sessions": [
                            {
                                "source-code": "",
                                "youtube-video-id": "1EoJMBCbCR4",
                                "notes": "",
                                "slides": "",
                                "name": "Web Development Bootcamp Using Flask and Vue - Git"
                            },
                            {
                                "source-code": "day0.zip",
                                "youtube-video-id": "6rsxC22BId4",
                                "notes": "",
                                "slides": "",
                                "name": "Web Development Bootcamp Using Flask and Vue - Day 0"
                            },
                            {
                                "source-code": "day1.zip",
                                "youtube-video-id": "UMEfqyhwQEY",
                                "notes": "",
                                "slides": "",
                                "name": "Web Development Bootcamp Using Flask and Vue - Day 1"
                            },
                            {
                                "source-code": "day2.zip",
                                "youtube-video-id": "Bu30HTvLl40",
                                "notes": "",
                                "slides": "",
                                "name": "Web Development Bootcamp Using Flask and Vue - Day 2"
                            },
                            {
                                "source-code": "day3.zip",
                                "youtube-video-id": "6dEsYtfGNYU",
                                "notes": "",
                                "slides": "",
                                "name": "Web Development Bootcamp Using Flask and Vue - Day 3"
                            },
                            {
                                "source-code": "day4.zip",
                                "youtube-video-id": "V6RUCa2spI8",
                                "notes": "",
                                "slides": "",
                                "name": "Web Development Bootcamp Using Flask and Vue - Day 4"
                            },
                            {
                                "source-code": "day5.zip",
                                "youtube-video-id": "G4VmAfv2QGg",
                                "notes": "",
                                "slides": "",
                                "name": "Web Development Bootcamp Using Flask and Vue - Day 5"
                            },
                            {
                                "source-code": "day6.zip",
                                "youtube-video-id": "h55iD4apiIg",
                                "notes": "",
                                "slides": "",
                                "name": "Web Development Bootcamp Using Flask and Vue - Day 6"
                            }
                     ]
                },
                {
                    "name": "Vue (Morning)",
                    "base-url": "/weeks/bootcamp/2025/May/MAD ll (Morning)/",
                    "term": "July",
                    "year": 2025,
                    "sessions": [
                            {
                                "source-code": "day0.zip",
                                "youtube-video-id": "-IVLxh2c3ss",
                                "notes": "",
                                "slides": "",
                                "name": "Web Development Bootcamp Using Flask and Vue - Day 0"
                            },
                            {
                                "source-code": "day1.zip",
                                "youtube-video-id": "5sx5aXDKgSA",
                                "notes": "",
                                "slides": "",
                                "name": "Web Development Bootcamp Using Flask and Vue - Day 1"
                            },
                            {
                                "source-code": "day2.zip",
                                "youtube-video-id": "ZaEdROvUR1g",
                                "notes": "",
                                "slides": "",
                                "name": "Web Development Bootcamp Using Flask and Vue - Day 2"
                            },
                    ]
                },
                {
                    "name": "Vue (Evening)",
                    "base-url": "/weeks/bootcamp/2025/May/MAD ll (Evening)/",
                    "term": "July",
                    "year": 2025,
                    "sessions": [
                            {
                                "source-code": "day0.zip",
                                "youtube-video-id": "EpH57BaH90Y",
                                "notes": "",
                                "slides": "",
                                "name": "Web Development Bootcamp Using Flask and Vue - Day 0"
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
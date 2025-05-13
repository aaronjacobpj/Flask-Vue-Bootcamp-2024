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
                                "source-code": "day0.zip",
                                "youtube-video-id": "f1gLzgGHqgo",
                                "notes": "",
                                "slides": "",
                                "name": "Web Development Bootcamp Using Flask and Vue - Day 0"
                            },
                    ]
                },
                {
                    "name": "Flask",
                    "base-url": "/weeks/bootcamp/2025/May/MAD l",
                    "term": "May",
                    "year": 2025,
                    "sessions": [
                            {
                                "source-code": "day0.zip",
                                "youtube-video-id": "euEnbr_TJiI",
                                "notes": "",
                                "slides": "",
                                "name": "Web Development Bootcamp Using Flask and HTML - Day 0"
                            },
                    ]
                },
                // {
                //     "name": "Vue (Morning)",
                //     "base-url": "/weeks/bootcamp/2025/May/MAD ll (Morning)/",
                //     "term": "May",
                //     "year": 2025,
                //     "sessions": [
                //             {
                //                 "source-code": "day0.zip",
                //                 "youtube-video-id": "1zSasOy9JiE",
                //                 "notes": "",
                //                 "slides": "",
                //                 "name": "Web Development Bootcamp Using Flask and Vue - Day 0"
                //             },
                //      ]
                // }

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
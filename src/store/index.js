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
                {
                    "name": "Vue",
                        "base-url": "/weeks/bootcamp/2025/March/MAD ll/",
                        "term": "March",
                        "year": 2025,
                        "sessions": [
                            {
                                "source-code": "day0.zip",
                                "youtube-video-id": "1zSasOy9JiE",
                                "notes": "",
                                "slides": "",
                                "name": "Web Development Bootcamp Using Flask and Vue - Day 0"
                            },
                            {
                                "source-code": "day1.zip",
                                "youtube-video-id": "haok7VVPfsM",
                                "notes": "",
                                "slides": "",
                                "name": "Web Development Bootcamp Using Flask and Vue - Day 1"
                            },
                            {
                                "source-code": "day2.zip",
                                "youtube-video-id": "iMR7qj-h-0I",
                                "notes": "",
                                "slides": "",
                                "name": "Web Development Bootcamp Using Flask and Vue - Day 2"
                            },
                            {
                                "source-code": "day3.zip",
                                "youtube-video-id": "iHVEMRtt89h8",
                                "notes": "",
                                "slides": "",
                                "name": "Web Development Bootcamp Using Flask and Vue - Day 3"
                            },
                            {
                                "source-code": "day4.zip",
                                "youtube-video-id": "eKQAjop6iVI",
                                "notes": "",
                                "slides": "",
                                "name": "Web Development Bootcamp Using Flask and Vue - Day 4"
                            },
                            {
                                "source-code": "day5.zip",
                                "youtube-video-id": "H3kHPepdO18",
                                "notes": "",
                                "slides": "",
                                "name": "Web Development Bootcamp Using Flask and Vue - Day 5"
                            },
                            {
                                "source-code": "day6.zip",
                                "youtube-video-id": "Dt-tobcsE-g",
                                "notes": "",
                                "slides": "",
                                "name": "Web Development Bootcamp Using Flask and Vue - Day 6"
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
import { createStore } from "vuex";
import {default as flaskj24} from "@/assets/2024/Flask/January.json";
import {default as vuej24} from "@/assets/2024/Vue/January.json";
import {default as flaskm24} from "@/assets/2024/Flask/March.json";
import {default as vuem24} from "@/assets/2024/Vue/March.json";
import {default as vuejuly24} from "@/assets/2024/Vue/July.json";
import {default as flasks24} from "@/assets/2024/Flask/September.json";
import {default as vues24} from "@/assets/2024/Vue/September.json";
import {default as vuen24} from "@/assets/2024/Vue/November.json";


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
                {
                    name: "Flask",
                    "base-url": "/weeks/bootcamp/2025/January/MAD l/",
                    term: "January",
                    year: 2025,
                    sessions: [
                        {
                            "source-code": "",
                            "youtube-video-id": "1EoJMBCbCR4",
                            "notes": "",
                            "slides": "",
                            "name": "Web Development Bootcamp Using Flask and HTML - Git"
                        },
                        {
                            "source-code": "day0.zip",
                            "youtube-video-id": "r9GmWa4u3CI",
                            "notes": "",
                            "slides": "",
                            "name": "Web Development Bootcamp Using Flask and HTML - Day 0"
                        },
                        {
                            "source-code": "day1.zip",
                            "youtube-video-id": "Bk9H1NE3LjM",
                            "notes": "",
                            "slides": "",
                            "name": "Web Development Bootcamp Using Flask and HTML - Day 1"
                        },
                        {
                            "source-code": "day2.zip",
                            "youtube-video-id": "eXBZp1uK50w",
                            "notes": "",
                            "slides": "",
                            "name": "Web Development Bootcamp Using Flask and HTML - Day 2"
                        },
                        {
                            "source-code": "day3.zip",
                            "youtube-video-id": "GTzssgxvj-Y",
                            "notes": "",
                            "slides": "",
                            "name": "Web Development Bootcamp Using Flask and HTML - Day 3"
                        },
                        {
                            "source-code": "day4.zip",
                            "youtube-video-id": "DJhXGrNsFwc",
                            "notes": "",
                            "slides": "",
                            "name": "Web Development Bootcamp Using Flask and HTML - Day 4"
                        },
                        {
                            "source-code": "day5.zip",
                            "youtube-video-id": "40SQLzP8OFM",
                            "notes": "",
                            "slides": "",
                            "name": "Web Development Bootcamp Using Flask and HTML - Day 5"
                        },
                        {
                            "source-code": "day6.zip",
                            "youtube-video-id": "W5LCZS6g6VM",
                            "notes": "",
                            "slides": "",
                            "name": "Web Development Bootcamp Using Flask and HTML - Day 6"
                        },
                        {
                            "source-code": "day7.zip",
                            "youtube-video-id": "6-oqYR-biPQ",
                            "notes": "",
                            "slides": "",
                            "name": "Web Development Bootcamp Using Flask and HTML - Day 7"
                        },
                        {
                            "source-code": "day8.zip",
                            "youtube-video-id": "amZxflSasG0",
                            "notes": "",
                            "slides": "",
                            "name": "Web Development Bootcamp Using Flask and HTML - Day 8"
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
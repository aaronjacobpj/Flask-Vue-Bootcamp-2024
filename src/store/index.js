import { createStore } from "vuex";

const store = createStore({
    state() {
        return {
            courses: [
                {
                    name: "Flask",
                    "base-url": "/weeks/bootcamp/2024/January/MAD l/",
                    term: "January",
                    year: 2024,
                    sessions: [
                        {
                         "source-code": "Day 0.zip",
                         "youtube-video-id": "YkpTsFRJm7g",
                         "notes": "",
                         "slides": "",
                         "name": "Web Development Bootcamp Using Flask and HTML - Day 0"
                        },
                        {
                         "source-code": "Day 1.zip",
                         "youtube-video-id": "qsdZjIMWj-U",
                         "notes": "",
                         "slides": "",
                         "name": "Web Development Bootcamp Using Flask and HTML - Day 1"
                        },
                        {
                         "source-code":"Day 2.zip",
                         "youtube-video-id": "EKsmJsf_O0M",
                         "notes": "",
                         "slides": "",
                         "name": "Web Development Bootcamp Using Flask and HTML - Day 2"
                        },
                        {
                         "source-code": "Day 3.zip",
                         "youtube-video-id": "nZUGQc37qLg",
                         "notes": "",
                         "slides": "",
                         "name": "Web Development Bootcamp Using Flask and HTML - Day 3"
                        },
                        {
                         "source-code": "Day 4.zip",
                         "youtube-video-id": "mSxGdnAq4W4",
                         "notes": "",
                         "slides": "",
                         "name": "Web Development Bootcamp Using Flask and HTML - Day 4"
                        },
                        {
                         "source-code": "Day 5.zip",
                         "youtube-video-id": "ZGzJH1ZuoKE",
                         "notes": "",
                         "slides": "",
                         "name": "Web Development Bootcamp Using Flask and HTML - Day 5"
                        },
                        {
                            "source-code": "Day 6.zip",
                            "youtube-video-id": "diCcyc-ihC0",
                            "notes": "",
                            "slides": "",
                            "name": "Web Development Bootcamp Using Flask and HTML - Day 6"
                        },
                        {
                            "source-code": "Day 7.zip",
                            "youtube-video-id": "1EoJMBCbCR4",
                            "notes": "",
                            "slides": "",
                            "name": "Web Development Bootcamp Using Flask and HTML - Git - Day 7"
                        }
                    ]

                },
                {
                    name: "Vue",
                    "base-url": "/weeks/bootcamp/2024/January/MAD ll/",
                    term: "January",
                    year: 2024,
                    sessions: [
                        {
                         "source-code": "Day 0.zip",
                         "youtube-video-id": "sWKKW_S8U8A",
                         "notes": "",
                         "slides": "",
                         "name": "Web Development Bootcamp Using Flask and Vue - Day 0"
                        },
                        {
                         "source-code": "Day 1.zip",
                         "youtube-video-id": "Jpqm5tCnCqA",
                         "notes": "",
                         "slides": "",
                         "name": "Web Development Bootcamp Using Flask and Vue - Day 1"
                        },
                        {
                         "source-code": "Day 2.zip",
                         "youtube-video-id": "iEiGdPmz0K4",
                         "notes": "",
                         "slides": "",
                         "name": "Web Development Bootcamp Using Flask and Vue - Day 2"
                        },
                        {
                         "source-code": "Day 3.zip",
                         "youtube-video-id": "dpIcjpGw_G4",
                         "notes": "",
                         "slides": "",
                         "name": "Web Development Bootcamp Using Flask and Vue - Day 3"
                        },
                        {
                            "source-code": "Day 4.zip",
                            "youtube-video-id": "UX0Rry3SLf4",
                            "notes": "",
                            "slides": "",
                            "name": "Web Development Bootcamp Using Flask and Vue - Day 4"
                        },
                        {
                            "source-code": "Day 5.zip",
                            "youtube-video-id": "WHHxp70GfHU",
                            "notes": "",
                            "slides": "",
                            "name": "Web Development Bootcamp Using Flask and Vue - Day 5"
                        },
                        {
                            "source-code": "Day 6.zip",
                            "youtube-video-id": "043mDEJAmQw",
                            "notes": "",
                            "slides": "",
                            "name": "Web Development Bootcamp Using Flask and Vue - Day 6"
                        },
                        {
                            "source-code": "Day 7.zip",
                            "youtube-video-id": "1EoJMBCbCR4",
                            "notes": "",
                            "slides": "",
                            "name": "Web Development Bootcamp Using Flask and Vue - Git - Day 7"
                        }
                    ]
                },
                {
                    name: "Flask",
                    "base-url": "/weeks/bootcamp/2024/March/MAD l/",
                    term: "March",
                    year: 2024,
                    sessions: [
                        {
                            "source-code": "Day 0.zip",
                            "youtube-video-id": "FS0Pscydnqo",
                            "notes": "",
                            "slides": "",
                            "name": "Web Development Bootcamp Using Flask and HTML - Day 0"
                        },
                        {
                            "source-code": "Day 1.zip",
                            "youtube-video-id": "gFJ7ORRht6k",
                            "notes": "",
                            "slides": "",
                            "name": "Web Development Bootcamp Using Flask and HTML - Day 1"
                        },
                        {
                            "source-code": "Day 2.zip",
                            "youtube-video-id": "VZVaaFApmPo",
                            "notes": "",
                            "slides": "",
                            "name": "Web Development Bootcamp Using Flask and HTML - Day 2"
                        },
                    ]
                },
                {
                    name: "Vue",
                    "base-url": "/weeks/bootcamp/2024/March/MAD ll/",
                    term: "March",
                    year: 2024,
                    sessions: [
                        {
                            "source-code": "Day 0.zip",
                            "youtube-video-id": "XLPqWsgtT40",
                            "notes": "",
                            "slides": "",
                            "name": "Web Development Bootcamp Using Flask and Vue - Day 0"
                        },
                        {
                            "source-code": "Day 1.zip",
                            "youtube-video-id": "9162EnsWaG0",
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
//import { ResearchPaperRadio, ResearchPaperInput } from "./taskEnums/researchPaper.js";

let ResearchPaperInput = {}
let ResearchPaperRadio = {}

export const CrawlingOptions = {
    RESEARCH_PAPER: {
        value: 1,
        label: 'Research Paper',
        placeholder: 'Enter your keyword',
        inputLabel: 'Keyword',
        fields: {
            radio: ResearchPaperRadio,
            input: ResearchPaperInput
        },
        name: "",
        area: ".research-paper-area"
    },
    NEWS: {
        value: 2,
        label: 'News',
        placeholder: 'Enter keyword',
        inputLabel: 'Keyword',
        name: "",
        area: ".news-area"
    },
    FACEBOOK: {
        value: 3,
        label: 'Facebook',
        placeholder: 'Enter username',
        inputLabel: 'Username',
        name: "",
        area: ".facebook-area"
    },
    GOOGLE_IMAGE: {
        value: 4,
        label: 'Google Image',
        placeholder: 'Enter keyword',
        inputLabel: 'Keyword',
        name: "",
        area: ".google-image-area"
    }
}
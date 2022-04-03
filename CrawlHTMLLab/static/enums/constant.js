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
        name: ""
    },
    NEWS: {
        value: 2,
        label: 'News',
        placeholder: 'Enter keyword',
        inputLabel: 'Keyword',
        name: ""
    },
    FACEBOOK: {
        value: 3,
        label: 'Facebook',
        placeholder: 'Enter username',
        inputLabel: 'Username',
        name: ""
    },
    GOOGLE_IMAGE: {
        value: 4,
        label: 'Google Image',
        placeholder: 'Enter keyword',
        inputLabel: 'Keyword',
        name: ""
    }
}
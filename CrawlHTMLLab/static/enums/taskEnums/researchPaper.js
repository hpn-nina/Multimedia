export const ResearchPaperRadio = [{
        label: "Is author or keyword",
        name: 'author',
        value: [{
                value: true,
                label: 'isAuthor'
            },
            {
                value: false,
                label: 'isNotAuthor'
            }
        ],
        required: true
    },
    {
        label: "Which site you want to crawl from?",
        name: 'site',
        value: [{
                value: 'ieee',
                label: 'IEEE',
                isDefault: true
            },
            {
                value: 'researchgate',
                label: 'ResearchGate',
                isDefault: false
            }, {
                value: 'acm',
                label: 'ACM',
                isDefault: false
            }
        ],
        required: false
    }
]



export const ResearchPaperInput = [{
    label: "Number of papers to crawl",
    name: 'quantity',
    defaultValue: '',
    placeholder: 'Enter number of paper you want to crawl',
    required: false
}]
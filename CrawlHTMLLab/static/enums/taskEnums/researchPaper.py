REASEARCH_PAPER_RADIO = [{
    "label": "Is author or keyword",
    "name": 'author',
    "value": [{
            "value": True,
            "label": 'isAuthor'
        },
        {
            "value": False,
            "label": 'isNotAuthor'
        }
    ],
    "required": True
},
{
    "label": "Which site you want to crawl from?",
    "name": 'site',
    "value": [{
            "value": 'ieee',
            "label": 'IEEE',
            "isDefault": True
        },
        {
            "value": 'researchgate',
            "label": 'ResearchGate',
            "isDefault": False
        }, {
            "value": 'acm',
            "label": 'ACM',
            "isDefault": False
        }
    ],
    "required": False
}]

RESEARCH_PAPER_INPUT = [{
    "label": "Number of papers to crawl",
    "name": 'quantity',
    "defaultValue": '',
    "placeholder": 'Enter number of paper you want to crawl',
    "required": False
}]
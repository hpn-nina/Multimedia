from taskEnums import facebook, news, researchPaper, googleImage

CRAWLING_OPTIONS = {
    'RESEARCH_PAPER': {
        'value': 1,
        'label': 'Research Paper',
        'fields': {
            "radio": researchPaper.REASEARCH_PAPER_RADIO,
            "input": researchPaper.RESEARCH_PAPER_INPUT
        }
    },
    'NEWS': {
        'value': 2,
        'label': 'News',
        "fields": {
            "input": news.NEWS_INPUT
        }
    },
    'FACEBOOK': {
        'value': 3,
        'label': 'Facebook',
        "fields": {
            "input": facebook.FACEBOOK_INPUT
        }
    },
    'GOOGLE_IMAGE': {
        'value': 4,
        'label': 'Google Image',
        "fields": {
            "input": googleImage.GOOGLE_IMAGE_INPUT
        }
    }
}

SELECT_VALUE = {
  1: CRAWLING_OPTIONS['RESEARCH_PAPER'],
  2: CRAWLING_OPTIONS['NEWS'],
  3: CRAWLING_OPTIONS['FACEBOOK'],
  4: CRAWLING_OPTIONS['GOOGLE_IMAGE']
}
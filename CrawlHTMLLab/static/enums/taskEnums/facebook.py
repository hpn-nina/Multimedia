FACEBOOK_INPUT = {
1: {
    "label": "Number of posts to crawl",
    "name": 'quantity-facebook',
    "defaultValue": '',
    "placeholder": 'Enter number of posts you want to crawl',
    "required": False,
    "type": "number"
},
2: {
    "label": "Username",
    "name": "username",
    "defaultValue": "",
    "placeholder": "Enter your facebook username",
    "required": True,
    "type": "text"
},
3: {
    "label": "Password",
    "name": "password",
    "defaultValue": "",
    "placeholder": "Enter your facebook password",
    "required": True,
    "type": "password"
},
4: {
    "label": "Target Page",
    "name": "target-page-input",
    "defaultValue": "",
    "placeholder": "Enter your target page",
    "required": True,
    "type": "text"
}}

FACEBOOK_RADIO = {
1:    {
    "label": "Is all or keyword",
    "name": 'isKeyword',
    "value": [{
            "value": True,
            "label": 'isKeyword'
        },
        {
            "value": False,
            "label": 'isNotKeyword'
        }
    ],
    "required": True
}
}
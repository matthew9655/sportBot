from site_scraper import Scraper
import requests
from requests.structures import CaseInsensitiveDict


def parse_info_dict(info_dict):
    text = ''
    for key, val in info_dict.items():
        if len(val) == 1:
            continue
        text += f'{key} - {val[0]} \n'
        for i in range(1, len(val)):
            text += f'{val[i]} \n'
        text += '\n'
    
    return text


if __name__ == '__main__':
    test_webhook = 'https://hooks.slack.com/services/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'
    sports_channel_webhook = 'https://hooks.slack.com/services/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'


    # curl -X POST -H 'Content-type: application/json' --data '{"text":"Hello, World!"}' https://hooks.slack.com/services/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

    s = Scraper()
    info_dict = s.scrape_courts()
    text = parse_info_dict(info_dict)

    data = '{"text":"' + text + '"}'

    headers = CaseInsensitiveDict()
    headers["Content-Type"] = "application/json"

    requests.post(sports_channel_webhook, headers=headers, data=data)


    


from site_scraper import Scraper
import requests
from requests.structures import CaseInsensitiveDict
import emoji

def parse_info_dict(info_dict):
    info_list = []

    emoji_list = [':one:', ':two:', ':three:', ':four:', ':five:', ':six:', ':seven:', 
              ':eight:', ':nine:', ':ten:', ':grinning:', ':smiley:', ':muscle:', ":innocent:",
              ':pray:', ":beers:", ":laughing:", ":joy:"]
    
    for key, val in info_dict.items():
        text = ''
        if len(val) == 1:
            continue
        text += f'{key} - {val[0]} \n'
        for i in range(1, min(18, len(val))):
            text += emoji.emojize(emoji_list[i-1], language='alias')
            text += f': {val[i]} \n'
        info_list.append(text)
    
    return info_list


if __name__ == '__main__':
    test_webhook = 'https://hooks.slack.com/services/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'
    sports_channel_webhook = 'https://hooks.slack.com/services/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'
    bot_tester_webhook = 'https://hooks.slack.com/services/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'


    # curl -X POST -H 'Content-type: application/json' --data '{"text":"Hello, World!"}' https://hooks.slack.com/services/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

    s = Scraper(mode='test')
    info_dict = s.scrape_courts()
    print(info_dict)
    info_list = parse_info_dict(info_dict)

    for text in info_list:
        data = '{"text":"' + text + '"}'

        headers = CaseInsensitiveDict()
        headers["Content-Type"] = "application/json"
        headers["charset"]='utf-8'

        requests.post(bot_tester_webhook, headers=headers, data=data.encode('utf-8'))


    


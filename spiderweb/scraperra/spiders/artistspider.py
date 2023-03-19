from scrapy.exceptions import CloseSpider
import re
from datetime import datetime
import scrapy
import datetime
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

#ISO3166
country_codes = {
        'AD': 'Andorra',
        'AE': 'United Arab Emirates',
        'AF': 'Afghanistan',
        'AG': 'Antigua & Barbuda',
        'AI': 'Anguilla',
        'AL': 'Albania',
        'AM': 'Armenia',
        'AN': 'Netherlands Antilles',
        'AO': 'Angola',
        'AQ': 'Antarctica',
        'AR': 'Argentina',
        'AS': 'American Samoa',
        'AT': 'Austria',
        'AU': 'Australia',
        'AW': 'Aruba',
        'AZ': 'Azerbaijan',
        'BA': 'Bosnia and Herzegovina',
        'BB': 'Barbados',
        'BD': 'Bangladesh',
        'BE': 'Belgium',
        'BF': 'Burkina Faso',
        'BG': 'Bulgaria',
        'BH': 'Bahrain',
        'BI': 'Burundi',
        'BJ': 'Benin',
        'BM': 'Bermuda',
        'BN': 'Brunei Darussalam',
        'BO': 'Bolivia',
        'BR': 'Brazil',
        'BS': 'Bahama',
        'BT': 'Bhutan',
        'BU': 'Burma (no longer exists)',
        'BV': 'Bouvet Island',
        'BW': 'Botswana',
        'BY': 'Belarus',
        'BZ': 'Belize',
        'CA': 'Canada',
        'CC': 'Cocos (Keeling) Islands',
        'CF': 'Central African Republic',
        'CG': 'Congo',
        'CH': 'Switzerland',
        'CI': 'Côte D\'ivoire (Ivory Coast)',
        'CK': 'Cook Iislands',
        'CL': 'Chile',
        'CM': 'Cameroon',
        'CN': 'China',
        'CO': 'Colombia',
        'CR': 'Costa Rica',
        'CS': 'Czechoslovakia (no longer exists)',
        'CU': 'Cuba',
        'CV': 'Cape Verde',
        'CX': 'Christmas Island',
        'CY': 'Cyprus',
        'CZ': 'Czech Republic',
        'DD': 'German Democratic Republic (no longer exists)',
        'DE': 'Germany',
        'DJ': 'Djibouti',
        'DK': 'Denmark',
        'DM': 'Dominica',
        'DO': 'Dominican Republic',
        'DZ': 'Algeria',
        'EC': 'Ecuador',
        'EE': 'Estonia',
        'EG': 'Egypt',
        'EH': 'Western Sahara',
        'ER': 'Eritrea',
        'ES': 'Spain',
        'ET': 'Ethiopia',
        'FI': 'Finland',
        'FJ': 'Fiji',
        'FK': 'Falkland Islands (Malvinas)',
        'FM': 'Micronesia',
        'FO': 'Faroe Islands',
        'FR': 'France',
        'FX': 'France, Metropolitan',
        'GA': 'Gabon',
        'GB': 'United Kingdom (Great Britain)',
        'GD': 'Grenada',
        'GE': 'Georgia',
        'GF': 'French Guiana',
        'GH': 'Ghana',
        'GI': 'Gibraltar',
        'GL': 'Greenland',
        'GM': 'Gambia',
        'GN': 'Guinea',
        'GP': 'Guadeloupe',
        'GQ': 'Equatorial Guinea',
        'GR': 'Greece',
        'GS': 'South Georgia and the South Sandwich Islands',
        'GT': 'Guatemala',
        'GU': 'Guam',
        'GW': 'Guinea-Bissau',
        'GY': 'Guyana',
        'HK': 'Hong Kong',
        'HM': 'Heard & McDonald Islands',
        'HN': 'Honduras',
        'HR': 'Croatia',
        'HT': 'Haiti',
        'HU': 'Hungary',
        'ID': 'Indonesia',
        'IE': 'Ireland',
        'IL': 'Israel',
        'IN': 'India',
        'IO': 'British Indian Ocean Territory',
        'IQ': 'Iraq',
        'IR': 'Islamic Republic of Iran',
        'IS': 'Iceland',
        'IT': 'Italy',
        'JM': 'Jamaica',
        'JO': 'Jordan',
        'JP': 'Japan',
        'KE': 'Kenya',
        'KG': 'Kyrgyzstan',
        'KH': 'Cambodia',
        'KI': 'Kiribati',
        'KM': 'Comoros',
        'KN': 'St. Kitts and Nevis',
        'KP': 'Korea, Democratic People\'s Republic of',
        'KR': 'Korea, Republic of',
        'KW': 'Kuwait',
        'KY': 'Cayman Islands',
        'KZ': 'Kazakhstan',
        'LA': 'Lao People\'s Democratic Republic',
        'LB': 'Lebanon',
        'LC': 'Saint Lucia',
        'LI': 'Liechtenstein',
        'LK': 'Sri Lanka',
        'LR': 'Liberia',
        'LS': 'Lesotho',
        'LT': 'Lithuania',
        'LU': 'Luxembourg',
        'LV': 'Latvia',
        'LY': 'Libyan Arab Jamahiriya',
        'MA': 'Morocco',
        'MC': 'Monaco',
        'MD': 'Moldova, Republic of',
        'MG': 'Madagascar',
        'MH': 'Marshall Islands',
        'ML': 'Mali',
        'MN': 'Mongolia',
        'MM': 'Myanmar',
        'MO': 'Macau',
        'MP': 'Northern Mariana Islands',
        'MQ': 'Martinique',
        'MR': 'Mauritania',
        'MS': 'Monserrat',
        'MT': 'Malta',
        'MU': 'Mauritius',
        'MV': 'Maldives',
        'MW': 'Malawi',
        'MX': 'Mexico',
        'MY': 'Malaysia',
        'MZ': 'Mozambique',
        'NA': 'Namibia',
        'NC': 'New Caledonia',
        'NE': 'Niger',
        'NF': 'Norfolk Island',
        'NG': 'Nigeria',
        'NI': 'Nicaragua',
        'NL': 'Netherlands',
        'NO': 'Norway',
        'NP': 'Nepal',
        'NR': 'Nauru',
        'NT': 'Neutral Zone (no longer exists)',
        'NU': 'Niue',
        'NZ': 'New Zealand',
        'OM': 'Oman',
        'PA': 'Panama',
        'PE': 'Peru',
        'PF': 'French Polynesia',
        'PG': 'Papua New Guinea',
        'PH': 'Philippines',
        'PK': 'Pakistan',
        'PL': 'Poland',
        'PM': 'St. Pierre & Miquelon',
        'PN': 'Pitcairn',
        'PR': 'Puerto Rico',
        'PT': 'Portugal',
        'PW': 'Palau',
        'PY': 'Paraguay',
        'QA': 'Qatar',
        'RE': 'Réunion',
        'RO': 'Romania',
        'RU': 'Russian Federation',
        'RW': 'Rwanda',
        'SA': 'Saudi Arabia',
        'SB': 'Solomon Islands',
        'SC': 'Seychelles',
        'SD': 'Sudan',
        'SE': 'Sweden',
        'SG': 'Singapore',
        'SH': 'St. Helena',
        'SI': 'Slovenia',
        'SJ': 'Svalbard & Jan Mayen Islands',
        'SK': 'Slovakia',
        'SL': 'Sierra Leone',
        'SM': 'San Marino',
        'SN': 'Senegal',
        'SO': 'Somalia',
        'SR': 'Suriname',
        'ST': 'Sao Tome & Principe',
        'SU': 'Union of Soviet Socialist Republics (no longer exists)',
        'SV': 'El Salvador',
        'SY': 'Syrian Arab Republic',
        'SZ': 'Swaziland',
        'TC': 'Turks & Caicos Islands',
        'TD': 'Chad',
        'TF': 'French Southern Territories',
        'TG': 'Togo',
        'TH': 'Thailand',
        'TJ': 'Tajikistan',
        'TK': 'Tokelau',
        'TM': 'Turkmenistan',
        'TN': 'Tunisia',
        'TO': 'Tonga',
        'TP': 'East Timor',
        'TR': 'Turkey',
        'TT': 'Trinidad & Tobago',
        'TV': 'Tuvalu',
        'TW': 'Taiwan, Province of China',
        'TZ': 'Tanzania, United Republic of',
        'UA': 'Ukraine',
        'UG': 'Uganda',
        'UK': 'United Kingdom',
        'UM': 'United States Minor Outlying Islands',
        'US': 'United States of America',
        'UY': 'Uruguay',
        'UZ': 'Uzbekistan',
        'VA': 'Vatican City State (Holy See)',
        'VC': 'St. Vincent & the Grenadines',
        'VE': 'Venezuela',
        'VG': 'British Virgin Islands',
        'VI': 'United States Virgin Islands',
        'VN': 'Viet Nam',
        'VU': 'Vanuatu',
        'WF': 'Wallis & Futuna Islands',
        'WS': 'Samoa',
        'YD': 'Democratic Yemen (no longer exists)',
        'YE': 'Yemen',
        'YT': 'Mayotte',
        'YU': 'Yugoslavia',
        'ZA': 'South Africa',
        'ZM': 'Zambia',
        'ZR': 'Zaire',
        'ZW': 'Zimbabwe',
        'ZZ': 'Unknown or unspecified country',
}

class PostsSpider(scrapy.Spider):

    page_number = 0
    name = 'my_spider'
    allowed_domains = ['ra.co']
    start_urls = []


    def __init__(self, names=None, maxval=None, runtime=None, *args, **kwargs):
            super(PostsSpider, self).__init__(*args, **kwargs)
            self.names = names
            self.maxval = maxval
            self.runtime = float(runtime)
            self.start_time = datetime.datetime.now()

            self.start_urls = [
                    f'https://ra.co/dj/{self.names}/past-events?'
            ]

    def parse(self, response):
            # check if runtime exceeded, close spider if it has
        elapsed_time = (datetime.datetime.now() - self.start_time).total_seconds() / 60
        if elapsed_time > self.runtime:
            self.logger.info(f'Runtime of {self.runtime} minutes exceeded. Closing spider.')
            self.crawler.engine.close_spider(self, f"Runtime of {self.runtime} minutes exceeded.")

        print(f'Found {len(response.css("li.Column-sc-18hsrnn-0.inVJeD div h3 a::attr(href)"))} acts on page {self.page_number}')

        for link in response.css('li.Column-sc-18hsrnn-0.inVJeD div h3 a::attr(href)'):
            yield response.follow(link.get(), callback=self.parse_act)

        next_page = f'https://ra.co/dj/{self.names}/past-events?&page={str(self.page_number)}'
        self.page_number += 1

        if len(response.css('li.Column-sc-18hsrnn-0.inVJeD div h3 a::attr(href)')) == 20:
                yield response.follow(next_page, callback=self.parse)

    def parse_act(self, response):
        from datetime import datetime
        date = response.xpath('//*[@id="__next"]/div[2]/header/div/div[2]//div/ul/li[2]/div/div[2]/a/span/text()').get()
        event = response.xpath('//*[@id="__next"]/div[2]/header/div//div/div/div[2]/h1/span/text()').get()
        promotors = response.xpath('//*[@id="__next"]/div[2]/header/div/div[2]/div[2]/div/ul/li[3]/div/div[2]/a/span/text()').getall()
        location = response.xpath('//*[@id="__next"]/div[2]/header/div//div[1]/div/div/div[1]/nav/ul/li[1]/div/a/span/text()').get()
        country_link = response.xpath('//*[@id="__next"]/div[2]/header/div//div[1]/div/div/div[1]/nav/ul/li[1]/div/a').attrib['href']
        venue = response.xpath('//*[@id="__next"]/div[2]/header/div/div[2]//div/ul/li[1]/div//span/text()')[1].get()
        acts = response.xpath('//*[@id="__next"]/div[2]/section[1]/div/section[1]/div/div/div[2]/ul/li[1]/div/span/a/span/text()').getall()

        date = re.sub(r'^.*?, ', '', date)

        promotors = ', '.join(promotors)

        if len(date) < 5:
            print(f'XXXXXXXXXXXXXXXXXX {date} XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
            date = f'01-01-{date}'

        elif len(date) >= 15:
            date = date[5:]

        elif date[-4: -2] == '20':
            date = datetime.strptime(date, '%b %d, %Y').strftime('%d-%m-%Y')
        else:
            date = datetime.strptime(date, '%d %b').strftime('%d-%m') + '-2023'

        country_code = country_link.split('/')[-2].upper()

        try:
            country = country_codes[country_code]
        except:
            country = country_code

        acts = ', '.join(acts)

        item = {
            'Day': date[:2],
            'Month': date[3:5],
            'Year': date[-4:],
            'Event': event,
            'promotors': promotors,
            'Location': location,
            'Country': country,
            'Venue': venue,
            'Acts': acts
        }

        yield item

if __name__== '__main__':
    process = CrawlerProcess()
    process.crawl(PostsSpider)
    process.start()
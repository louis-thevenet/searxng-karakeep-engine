from json import loads
from searx.result_types import EngineResults

_base_url = None
_api_key = None
_number_of_results = None


def init(engine_settings):
    global _api_key
    global _base_url
    global _number_of_results
    _api_key = engine_settings.get('api_key', None)
    _base_url = engine_settings.get('base_url', None)
    _number_of_results = engine_settings.get('number_of_results', 3)


def request(query, params):
    if not _api_key:
        raise ValueError("Missing API key for Karakeep engine")

    if not _base_url:
        raise ValueError("Missing search API URL for Karakeep engine")

    url = _base_url + 'api/v1/bookmarks/search' + '?q=' + query + '&limit=' + str(
        _number_of_results)

    headers = {
        'Authorization': f'Bearer {_api_key}',
        'Accept': 'application/json',
    }

    params['url'] = url
    params['headers'] = headers

    return params


def response(resp) -> EngineResults:
    res = EngineResults()
    json_data = loads(resp.text)

    for result in json_data['bookmarks']:
        content = result['content']

        infobox_data = {
            'infobox': content.get('title', 'No Title'),
            'img_src': content.get('imageUrl', ''),
            'content': content.get('description', ''),
            'template': 'infobox.html',
        }
        attributes = []
        if content.get('author'):
            attributes.append({'label': 'Author', 'value': content['author']})

        # if content.get('publisher'):
        #     attributes.append({
        #         'label': 'Publisher',
        #         'value': content['publisher']
        #     })

        if content.get('datePublished'):
            attributes.append({
                'label': 'Date Published',
                'value': content['datePublished']
            })

        # if result.get('createdAt'):
        #     attributes.append({
        #         'label': 'Bookmarked',
        #         'value': result['createdAt']
        #     })

        tag_list = result.get('tags', [])
        if len(tag_list) > 0:
            attributes.append({
                'label':
                "Tags",
                'value':
                ', '.join([tag['name'] for tag in tag_list if 'name' in tag])
            })

        if attributes:
            infobox_data['attributes'] = attributes

        urls = []
        if content.get('url'):
            urls.append({'url': content['url'], 'title': 'Original page'})
        urls.append({
            'url': f"{_base_url}/dashboard/preview/{result['id']}",
            'title': 'On Karakeep'
        })

        if urls:
            infobox_data['urls'] = urls

        res.append(infobox_data)

    return res

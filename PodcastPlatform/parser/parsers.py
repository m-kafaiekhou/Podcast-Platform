import requests
from xml.etree import ElementTree as ET


response = requests.get('https://rss.art19.com/apology-line')
print(type(response.content))

root = ET.fromstring(response.content)

print(root.find('channel/item').find('title').text)
print(root.find('channel/title').text)
print(root.find('channel/{http://www.itunes.com/dtds/podcast-1.0.dtd}category').get('text'))



class RSSParser:
    def __init__(self, podcastModel: object, episodeModel: object):
        self.podcastModel = podcastModel
        self.episodeModel = episodeModel

    def get_rss_content_from_url(self):
        """
        Sends a GET request to model rss url and returns the content

        Returns:
            type: bytes
        """

        response = requests.get(self.podcastModel.rss_url)
        return response.content
    
    def get_element_tree(self):
        tree = ET.fromstring(self.get_rss_content_from_url())

        return tree
    
    def get_channel_feed_data_dict(self):
        """
        gets the rss element tree and turns the channel data to a dict
          with keys and values such that it can be unpacked to make an model object out of it

        Returns:
            Dict
        """
        root = self.get_element_tree()

        data_dict = {}

        for field in self.podcastModel._meta.get_fields():
            path = getattr(self.podcastModel, field).split()

            if len(path) > 1:
                data_dict[f'{field}'] = root.find(path[0]).get(path[1])

            else:
                data_dict[f'{field}'] = root.find(path[0])

        return data_dict

    def get_episodes_feed_list_dict(self):
        root = self.get_element_tree()

        data_dict = {}

        for field in self.podcastModel._meta.get_fields():
            path = getattr(self.podcastModel, field).split()

            if len(path) > 1:
                data_dict[f'{field}'] = root.findall(path[0]).get(path[1])

            else:
                data_dict[f'{field}'] = root.findall(path[0])

        return data_dict
    
    
    
import requests
from xml.etree import ElementTree as ET


response = requests.get('https://rss.art19.com/apology-line')
print(type(response.content))

root = ET.fromstring(response.content)

print(root.find('channel/item').find('title').text)
print(root.find('channel/title').text)
print(root.find('channel/{http://www.itunes.com/dtds/podcast-1.0.dtd}category').get('text'))



# class RSSParser:
#     def __init__(self, podcastModel: object, episodeModel: object):
#         self.podcastModel = podcastModel
#         self.episodeModel = episodeModel

#     def get_rss_content_from_url(self):
#         """
#         Sends a GET request to model rss url and returns the content

#         Returns:
#             type: bytes
#         """

#         response = requests.get(self.podcastModel.rss_url)
#         return response.content
    
#     def get_element_tree(self):
#         tree = ET.fromstring(self.get_rss_content_from_url())

#         return tree
    
#     def get_channel_feed_data_dict(self):
#         """
#         gets the rss element tree and turns the channel data to a dict
#           with keys and values such that it can be unpacked to make an model object out of it

#         Returns:
#             Dict
#         """
#         root = self.get_element_tree()

#         data_dict = {}

#         for field in self.podcastModel._meta.get_fields():
#             path = getattr(self.podcastModel, field).split()

#             if len(path) > 1:
#                 data_dict[f'{field}'] = root.find(path[0]).get(path[1])

#             else:
#                 data_dict[f'{field}'] = root.find(path[0])

#         return data_dict

#     def get_episodes_feed_list_dict(self):
#         root = self.get_element_tree()

#         data_dict = {}

#         for field in self.podcastModel._meta.get_fields():
#             path = getattr(self.podcastModel, field).split()

#             if len(path) > 1:
#                 data_dict[f'{field}'] = root.findall(path[0]).get(path[1])

#             else:
#                 data_dict[f'{field}'] = root.findall(path[0])

#         return data_dict
    
#     def get_new_episodes(self, *args, **kwargs):
#         pass

#     def create_model_objects_instances(self, *args, **kwargs):
#         pass

#     def save_model_objects(self, *args, **kwargs):
#         pass
    


class PodcastRSSParser:
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
    
    def get_channel_data_model_obj(self):
        """
        gets the rss element tree and turns the channel data to a dict
          with keys and values such that it can be unpacked to make an model object out of it

        Returns:
            Dict
        """
        root = self.get_element_tree()

        data_dict = {
            'title': root.find('channel/title'),
            'description': root.find('channel/description'),
            'copyright': root.find('channel/copyright'),
            'generator': root.find('channel/generator'),
            'link': root.find('channel/link'),
            'owner_name': root.find('channel/{http://www.itunes.com/dtds/podcast-1.0.dtd}owner/{http://www.itunes.com/dtds/podcast-1.0.dtd}name'),
            'owner_email': root.find('channel/{http://www.itunes.com/dtds/podcast-1.0.dtd}owner/{http://www.itunes.com/dtds/podcast-1.0.dtd}email'),
            'author': root.find('channel/{http://www.itunes.com/dtds/podcast-1.0.dtd}author'),
            'summary': root.find('channel/{http://www.itunes.com/dtds/podcast-1.0.dtd}summary'),
            'language': root.find('channel/language'),
            'explicit': root.find('channel/{http://www.itunes.com/dtds/podcast-1.0.dtd}explicit'),
            'category': root.find('channel/{http://www.itunes.com/dtds/podcast-1.0.dtd}category').get('text'),
            'keywords': root.find('channel/{http://www.itunes.com/dtds/podcast-1.0.dtd}keywords'),
            'type': root.find('channel/{http://www.itunes.com/dtds/podcast-1.0.dtd}type'),
            'icon_image_url': root.find('channel/{http://www.itunes.com/dtds/podcast-1.0.dtd}image').get('href'),
            'image_url': root.find('channel/image/url'),
            'image_link': root.find('channel/image/link'),
            'image_title': root.find('channel/image/title'),
            }
        
        obj = self.podcastModel(**data_dict)

        return obj

    def get_episodes_model_obj_list(self):
        root = self.get_element_tree()

        items = root.findall('channel/item')

        item_lst = [
            self.episodeModel(

            )
        ]

        

        return 1
    
    def get_new_episodes(self, *args, **kwargs):
        pass

    def create_model_objects_instances(self, *args, **kwargs):
        pass

    def save_model_objects(self, *args, **kwargs):
        pass
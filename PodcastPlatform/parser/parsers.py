import requests
from xml.etree import ElementTree as ET


# response = requests.get('https://rss.art19.com/apology-line')
# print(type(response.content))

# root = ET.fromstring(response.content)

# print(root.find('channel/item').findtext(
# ".//content:eoded",
# namespaces={"content": "http://purl.org/rss/1.0/modules/content/"},
# ))
# print(root.find('channel/title').text)
# print(root.find('channel/{http://www.itunes.com/dtds/podcast-1.0.dtd}category').get('text'))



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

    NAMESPACES = {
        "itunes": "http://www.itunes.com/dtds/podcast-1.0.dtd",
        "content": "http://purl.org/rss/1.0/modules/content/",
    }

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
    
    def get_channel_data_model_dict(self):
        """
        gets the rss element tree and turns the channel data to a dict
          with keys and values such that it can be unpacked to make an model object out of it

        Returns:
            Dict
        """
        root = self.get_element_tree()

        data_dict = {
            'title': root.findtext('channel/title'),
            'description': root.findtext('channel/description'),
            'copyright': root.findtext('channel/copyright'),
            'generator': root.findtext('channel/generator'),
            'link': root.findtext('channel/link'),
            'owner_name': root.findtext('channel/itunes:owner/itunes:name', namespaces={'itunes': self.NAMESPACES['itunes']}),
            'owner_email': root.findtext('channel/itunes:owner/itunes:email', namespaces={'itunes': self.NAMESPACES['itunes']}),
            'author': root.findtext('channel/itunes:author', namespaces={'itunes': self.NAMESPACES['itunes']}),
            'summary': root.findtext('channel/itunes:summary', namespaces={'itunes': self.NAMESPACES['itunes']}),
            'language': root.findtext('channel/language'),
            'explicit': root.findtext('channel/itunes:explicit', namespaces={'itunes': self.NAMESPACES['itunes']}),
            'category': root.find('channel/itunes:category', namespaces={'itunes': self.NAMESPACES['itunes']}).get('text'),
            'keywords': root.findtext('channel/itunes:keywords', namespaces={'itunes': self.NAMESPACES['itunes']}),
            'type': root.findtext('channel/itunes:type', namespaces={'itunes': self.NAMESPACES['itunes']}),
            'icon_image_url': root.find('channel/itunes:image', namespaces={'itunes': self.NAMESPACES['itunes']}).get('href'),
            'image_url': root.findtext('channel/image/url'),
            'image_link': root.findtext('channel/image/link'),
            'image_title': root.findtext('channel/image/title'),
            }
        
        for key, val in data_dict.items():
            setattr(self.podcastModel, key, val)

        self.podcastModel.save()

    def get_episodes_model_obj_list(self):
        root = self.get_element_tree()

        items = root.findall('channel/item')

        item_lst = []

        for item in items:
            title = item.findtext('title')
            description = item.findtext('description')
            
            episode_num = item.findtext('.//itunes:episode', namespaces={"itunes": self.NAMESPACES['itunes']})
            summary = item.findtext('.//itunes:summary', namespaces={"itunes": self.NAMESPACES['itunes']})
            content = item.findtext(
                        ".//content:encoded",
                        namespaces={"content": self.NAMESPACES['content']}
                        )
            guid = item.findtext('guid')
            publish_date = item.findtext('pubDate')
            explicit = item.findtext('.//itunes:explicit', namespaces={"itunes": self.NAMESPACES['itunes']})
            image_url = item.find('.//itunes:image', namespaces={"itunes": self.NAMESPACES['itunes']}).get('href') if item.find('.//itunes:image', namespaces={"itunes": self.NAMESPACES['itunes']}) else None
            keywords = item.findtext('.//itunes:keywords', namespaces={"itunes": self.NAMESPACES['itunes']})
            duration = item.findtext('.//itunes:duration', namespaces={"itunes": self.NAMESPACES['itunes']})
            enclosure_url = item.find('enclosure').get('url')
            enclosure_type = item.find('enclosure').get('type')
            enclosure_length = item.find('enclosure').get('length')
    
            obj = self.episodeModel(
                podcast=self.podcastModel,
                title=title,
                description=description,
                episode_num=episode_num,
                summary=summary,
                content=content,
                guid=guid,
                publish_date=publish_date,
                explicit=explicit,
                image_url=image_url,
                keywords=keywords,
                duration=duration,
                enclosure_url=enclosure_url,
                enclosure_type=enclosure_type,
                enclosure_length=enclosure_length
            )

            item_lst.append(obj)
    
        return item_lst

    def create_episode_model_objects(self, instances):
        self.episodeModel.objects.bulk_create(instances, ignore_conflicts=True)

    def fill_db(self):
        self.get_channel_data_model_dict()
        lst = self.get_episodes_model_obj_list()
        self.create_episode_model_objects(lst)

import os
import requests
from typing import List
from insta import RobotCore




class Download(RobotCore):
    def get_pics(self,
                 user: str,
                 video: bool = False) -> List[str]:

        same_body = self.find_user_post(user, video)
        container = same_body.find_element_by_class_name('_2z6nI')
        a_tag = container.find_elements_by_tag_name('a')  # list
        linked = [x.get_attribute('href') for x in a_tag]  # ALL
        self.links = [*linked]
        return self.links

    def download(self,
                 total=100,
                 video=True) -> None:  # video
        """function downloads video or image file from selected links generated from get_pics method """
        curr_mkdir = os.getcwd()
        vid_path = os.path.join(curr_mkdir, 'vid_file')
        os.makedirs(vid_path, exist_ok=True)
        content = '.mp4' if video else 'png'
        download_content = [x for x in os.listdir(vid_path) if x.endswith(content)]
        links = self.links
        if links:
            try:
                for num, link in enumerate(links):
                    self.driver.get(link)
                    if num <= total:
                        vid_link = self.driver.find_element_by_xpath('//video[@src]')
                        vid_url = vid_link.get_attribute('src')
                        re = requests.get(vid_url)
                        name = ''  # customise
                        content_name = f'{name}{num}.{content}'
                        if download_content:
                            if content_name in download_content:
                                continue
                        else:
                            with open(content_name, 'wb') as f:
                                f.write(re.content)
                    else:
                        break

            except Exception:
                raise NotImplemented
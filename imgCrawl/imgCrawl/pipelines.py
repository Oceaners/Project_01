# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from urllib.parse import urlparse
from scrapy.pipelines.images import ImagesPipeline
from scrapy import Request
import os
from scrapy.utils.project import get_project_settings
import shutil


class ImgcrawlPipeline(ImagesPipeline):
    img_store = get_project_settings().get('IMAGES_STORE')

    # 重写ImagePipeline类方法
    def get_media_requests(self, item, info):
        for image_url in item['img_url']:
            yield Request(image_url)

    # 将不同板块的图片保存到不同文件夹下
    def item_completed(self, results, item, info):
        image_path = [x["path"] for ok, x in results if ok]
        # print(image_path[0])
        # print("上为下载的返回".center(60, "*"))

        # 定义保存的路径
        img_path = "%s%s" % (self.img_store, str(item['img_title']).strip("''"))
        # print(img_path)
        # print("不同的路径".center(60, "*"))

        # 如果路径不存在
        if os.path.exists(img_path) == False:
            os.mkdir(img_path)

        # 文件从默认的下载路径移动到指定保存路径下
        _, img_name = image_path[0].split('/')

        print(img_path+"/"+img_name)
        # print("展示下载后的文件名字".center(60, "*"))
        shutil.move(self.img_store + image_path[0], img_path + "/" + img_name)


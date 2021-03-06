# coding: utf-8
# @Time    : 2018/05/15 19:08
# @Author  : xavier


from rest_framework import serializers

from models import Comic, ComicChapter


class ComicSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comic
        fields = ('id', 'name', 'cover', 'intro', 'upt')


class ComicChapterSerializer(serializers.ModelSerializer):
    img_list = serializers.SerializerMethodField()

    def get_img_list(self, obj):
        return obj.imgs[1:-1].replace('"', '').split(',')

    class Meta:
        model = ComicChapter
        fields = ('id', 'chapter', 'img_list')

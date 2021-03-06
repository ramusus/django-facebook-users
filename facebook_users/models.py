# -*- coding: utf-8 -*-
'''
Copyright 2011-2015 ramusus
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''
from django.db import models
from facebook_api.models import FacebookGraphIDModel, FacebookGraphManager
from facebook_api import fields
import logging

log = logging.getLogger('facebook_users')

class FacebookUserGraphManager(FacebookGraphManager):

    def fetch(self, *args, **kwargs):
        if 'fields' not in kwargs:
            kwargs['fields'] = 'bio,address,email,gender,id,languages,link,installed,first_name,cover,about,education,currency,devices,birthday,religion,favorite_athletes,favorite_teams,hometown,inspirational_people,interested_in,sports,quotes,meeting_for,username,middle_name,work,website,last_name,video_upload_limits,is_verified,name,locale,location,payment_pricepoints,political,security_settings,relationship_status,significant_other,third_party_id,timezone,updated_time,age_range'
        return super(FacebookUserGraphManager, self).fetch(*args, **kwargs)

class User(FacebookGraphIDModel):
    class Meta:
        verbose_name = 'Facebook user'
        verbose_name_plural = 'Facebook users'

    name = models.CharField(max_length=300, help_text='The user\'s full name')

    first_name = models.CharField(max_length=300, help_text='The user\'s first name')
    last_name = models.CharField(max_length=300, help_text='The user\'s last name')
    middle_name = models.CharField(max_length=300, help_text='The user\'s middle name')

    gender = models.CharField(max_length=10, help_text='The user\'s gender: female or male')
    locale = models.CharField(max_length=5, help_text='The user\'s locale')
    link = models.URLField(max_length=300, help_text='The URL of the profile for the user on Facebook')
    cover = fields.JSONField(max_length=500, null=True, help_text='The user\'s cover photo (must be explicitly requested using fields=cover parameter)')

    username = models.CharField(max_length=300, help_text='The user\'s Facebook username')
    third_party_id = models.CharField(max_length=300, help_text='An anonymous, but unique identifier for the user')
    updated_time = models.DateTimeField(null=True, help_text='The last time the user\'s profile was updated; changes to the languages, link, timezone, verified, interested_in, favorite_athletes, favorite_teams, and video_upload_limits are not not reflected in this value')

    # fields from https://developers.facebook.com/docs/reference/api/user/
    email = models.CharField(max_length=100, help_text='The proxied or contact email address granted by the user')
    timezone = models.IntegerField(null=True, help_text='The user\'s timezone offset from UTC')
    bio = models.TextField(help_text='The user\'s biography')
    birthday = models.CharField(max_length=300, help_text='The user\'s birthday')

    languages = fields.JSONField(max_length=500, null=True, help_text='The user\'s languages')
    installed = fields.JSONField(max_length=500, null=True, help_text='Specifies whether the user has installed the application associated with the app access token that is used to make the request; only returned if specifically requested via the fields URL parameter')

    # TODO: rename to is_verified according to https://developers.facebook.com/tools/explorer/291716840848442/?method=GET&path=100000007637389%3Ffields%3Dcover%2Ccurrency%2Cemail%2Cabout%2Cage_range%2Cbirthday%2Cgender%2Chometown%2Cid%2Cdevices%2Cfirst_name%2Clast_name%2Caddress%2Cinstall_type%2Cinstalled%2Cinterested_in%2Clanguages%2Clink%2Clocation%2Cmeeting_for%2Cbio%2Ceducation%2Cmiddle_name%2Cname_format%2Cname%2Cinspirational_people%2Cpolitical%2Cquotes%2Crelationship_status%2Creligion%2Csecurity_settings%2Csignificant_other%2Csports%2Cwork%2Cwebsite%2Ctimezone%2Ctelevision%2Ctagged%2Cupdated_time%2Cvideo_upload_limits%2Cphotos%2Cpicture%2Cposts%2Calbums%2Cgames%2Cverified%2Cvideos%2Cbooks%2Cmusic%2Cis_verified&
    verified = models.BooleanField(default=False, help_text='The user\'s account verification status, either true or false (see below)')

    currency = fields.JSONField(max_length=500, null=True, help_text='The user\'s currency settings (must be explicitly requested using a fields=currency URL parameter)')
    devices = fields.JSONField(max_length=500, null=True, help_text='A list of the user\'s devices beyond desktop')
    education = fields.JSONField(max_length=500, null=True, help_text='A list of the user\'s education history')

    hometown = fields.JSONField(max_length=500, null=True, help_text='The user\'s hometown')
    interested_in = fields.JSONField(max_length=500, null=True, help_text='The genders the user is interested in')
    location = fields.JSONField(max_length=500, null=True, help_text='The user\'s current city')
    payment_pricepoints = fields.JSONField(max_length=500, null=True, help_text='The payment price-points available for that user')
    favorite_athletes = fields.JSONField(max_length=500, null=True, help_text='The user\'s favorite athletes; this field is deprecated and will be removed in the near future')
    favorite_teams = fields.JSONField(max_length=500, null=True, help_text='The user\'s favorite teams; this field is deprecated and will be removed in the near future')

    political = models.CharField(max_length=100, help_text='The user\'s political view')
    picture = models.CharField(max_length=100, help_text='The URL of the user\'s profile pic (only returned if you explicitly specify a \'fields=picture\' param)')
    quotes = models.CharField(max_length=100, help_text='The user\'s favorite quotes')
    relationship_status = models.CharField(max_length=100, help_text='The user\'s relationship status: Single, In a relationship, Engaged, Married, It\'s complicated, In an open relationship, Widowed, Separated, Divorced, In a civil union, In a domestic partnership')
    religion = models.CharField(max_length=100, help_text='The user\'s religion')

    security_settings = fields.JSONField(max_length=500, null=True, help_text='Information about security settings enabled on the user\'s account (must be explicitly requested using a fields=security_settings URL parameter)')
    significant_other = fields.JSONField(max_length=500, null=True, help_text='The user\'s significant other')
    video_upload_limits = fields.JSONField(max_length=500, null=True, help_text='The size of the video file and the length of the video that a user can upload; only returned if specifically requested via the fields URL parameter')

    website = models.URLField(max_length=100, help_text='The URL of the user\'s personal website')
    work = fields.JSONField(max_length=500, null=True, help_text='A list of the user\'s work history')

    objects = models.Manager()
    remote = FacebookUserGraphManager()

    def __unicode__(self):
        return self.name

    def picture_url(self, w, h):
        return 'https://graph.facebook.com/%s/picture?width=%d&height=%d' % (self.graph_id, w, h)

    def set_name(self, name):
        name_parts = name.split()
        self.first_name = name_parts[0]
        if len(name_parts) == 2:
            self.last_name = name_parts[1]
        elif len(name_parts) > 2:
            self.middle_name = name_parts[1]
            self.last_name = ' '.join(name_parts[2:])

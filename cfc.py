#!/usr/bin/env python

import os
import requests
import argparse


class BaseCloudFlareApi(object):
    PREFIX = 'https://api.cloudflare.com/client/v4'

    def __init__(self, email, token):
        assert email
        assert token

        self.email = email
        self.token = token

    def _headers(self):
        return {
            'X-Auth-Email': self.email,
            'X-Auth-Key': self.token,
        }

    def _request(self, method, path):
        return requests.request(method, self.PREFIX + path, headers=self._headers()).json()


class CloudFlareApi(BaseCloudFlareApi):
    def get_zones(self):
        return {zone['name']: zone for zone in api._request('GET', '/zones')['result']}

    def check_ssl_status(self):
        zones = api.get_zones()
        for name, zone in zones.items():
            ssl = api._request('GET', '/zones/%s/settings/ssl' % zone['id'])['result']
            print '%25s %10s %10s' % (name, ssl['certificate_status'], ssl['value'])


EMAIL = os.environ.get('CFC_EMAIL')
TOKEN = os.environ.get('CFC_TOKEN')


root_parser = argparse.ArgumentParser()
root_parser.add_argument('--cf-email', default=None)
root_parser.add_argument('--cf-token', default=None)

commands_subparsers = root_parser.add_subparsers(dest='command1')
parser = commands_subparsers.add_parser('check_ssl_status')


args = root_parser.parse_args()


api = CloudFlareApi(args.cf_email or EMAIL, args.cf_token or TOKEN)


{
    'check_ssl_status': lambda args: api.check_ssl_status(),
}[args.command1](args)



#!/usr/bin/env python

import sys
import requests

import irc.bot
import rospy
from std_msgs.msg import String

# Globals
TWITCH_PORT = 6667

class ChatReader(irc.bot.SingleServerIRCBot):
    def __init__(self, username, client_id, token, channel):
        # Rospy setup
        self.pub = rospy.Publisher('twitch_chat', String, queue_size=50)
        rospy.init_node('twitch_chat_pub', anonymous=True)

        # IRC setup
        self.client_id = client_id
        self.token = token
        self.channel = '#' + channel

        # url = 'https://api.twitch.tv/kraken/users?login={chan}'.format(chan=channel)
        # headers = {'Client-ID': client_id, 'Accept': 'application/vnd.twitchtv.v5+json'}
        # req = requests.get(url, headers=headers).json()
        # self.channel_id = req['users'][0]['_id']

        server = 'irc.chat.twitch.tv'
        port = 6667
        rospy.loginfo("Connecting to {ser} on port {port}...".format(ser=server, port=port))
        irc.bot.SingleServerIRCBot.__init__(self, [(server, port, 'oauth:'+token)], username, username)

    def on_welcome(self, c, e):
        rospy.loginfo("Joining %s" % self.channel)

        c.cap('REQ', ':twitch.tv/membership')
        c.cap('REQ', ':twitch.tv/tags')
        c.cap('REQ', ':twitch.tv/commands')
        c.join(self.channel)

    def on_pubmsg(self, c, e):
        rospy.loginfo(str(e.arguments))
        self.pub.publish(str(e.arguments))

if __name__ == '__main__':

    try:
        bot = ChatReader('trywitchyrobots', 'http://localhost',  '0dhx2iyi6lwtgngshdtesubcriki23', 'twitchyrobots')
        bot.start()
    except rospy.ROSInterruptException:
        pass
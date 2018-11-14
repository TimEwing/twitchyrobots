#!/usr/bin/env python2

import sys
import requests

import irc.bot
import rospy
from std_msgs.msg import String

# Globals
TWITCH_PORT = 6667

class ChatReader(irc.bot.SingleServerIRCBot):
    def __init__(self, username, token, channel):
        # Rospy setup
        self.pub = rospy.Publisher('twitch_chat', String, queue_size=50)
        rospy.init_node('twitch_chat_pub', anonymous=True)

        # IRC setup
        self.token = token
        self.channel = '#' + channel

        server = 'irc.chat.twitch.tv'
        port = 6667
        rospy.loginfo("Connecting to {ser} on port {port}...".format(ser=server, port=port))
        irc.bot.SingleServerIRCBot.__init__(self, [(server, port, 'oauth:'+token)], username, username)

    def on_welcome(self, channel, event):
        rospy.loginfo("Joining %s" % self.channel)

        channel.cap('REQ', ':twitch.tv/membership')
        channel.cap('REQ', ':twitch.tv/tags')
        channel.cap('REQ', ':twitch.tv/commands')
        channel.join(self.channel)

    def on_pubmsg(self, channel, event):
    	# Useful Keys:
    	# 	- 
    	args = {a['key'] : a['value'] for a in event.tags}
    	args['message'] = event.arguments[0]
    	output = str(args['message'])
        rospy.loginfo(output)
        self.pub.publish(output)

if __name__ == '__main__':

    try:
        bot = ChatReader('twitchyrobots', '0dhx2iyi6lwtgngshdtesubcriki23', 'twitchyrobots')
        bot.start()
    except rospy.ROSInterruptException:
        pass
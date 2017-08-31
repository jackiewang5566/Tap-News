""" import json module for parsing json """
import json
import pika

class CloudAMQPClient(object):
    """ Define class for customized AMQP class which can have different parameters """
    def __init__(self, cloud_amqp_url, queue_name):
        self.cloud_amqp_url = cloud_amqp_url
        self.queue_name = queue_name
        self.params = pika.URLParameters(cloud_amqp_url)
        # self.params.socket_time_timeout = 3
        # change to below after using homebrew install python and pika
        self.params.socket_timeout = 3
        self.connection = pika.BlockingConnection(self.params)
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=queue_name)

    # send a message
    def send_message(self, message):
        """ send message function """
        self.channel.basic_publish(exchange='',
                                   routing_key=self.queue_name,
                                   body=json.dumps(message))
        # routing is used to specify where the message pointing to
		# json.dumps(message) is used to turn json format to string format,
		# because when sending message, you have to send string;
		# when it has been received, use json.loads to regenerate to json from string
        print "[x] Sent message to %s: %s" % (self.queue_name, message)

    # get a message
    def get_message(self):
        """ get message function """
        method_frame, header_frame, body = self.channel.basic_get(self.queue_name)
        if method_frame:
            print "[x] Received message from %s: %s" % (self.queue_name, body)
			# basic_ack method is to tell AMQP that we have received the message, only
			# send a basic_ack back after receiving basic_get, the message can be removed
			# from AMQP
            self.channel.basic_ack(method_frame.delivery_tag)
            return json.loads(body)
        else:
            print "No message returned."
            return None
    # BlockingConnection.sleep is a safer way to sleep than time.sleep().
    def sleep(self, seconds):
        """ define sleep function """
        self.connection.sleep(seconds)

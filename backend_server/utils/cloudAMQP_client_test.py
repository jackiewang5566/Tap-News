from cloudAMQP_client import CloudAMQPClient

CLOUDAMQP_URL = "amqp://mcyrgohw:CB44sIsZxuz-IInG5a5ESFGrnP0iIda4@crane.rmq.cloudamqp.com/mcyrgohw"
TEST_QUEUE_NAME = "test"

def test_basic():
    client = CloudAMQPClient(CLOUDAMQP_URL, TEST_QUEUE_NAME)

    sentMsg = {"test": "test"}
    client.sendMessage(sentMsg)
    receivedMsg = client.getMessage()

    assert sentMsg == receivedMsg
    print "test_basic passed."

if __name__ == "__main__":
    test_basic()

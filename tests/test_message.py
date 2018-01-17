import copy

import pytest

from Facebook import message

msg_dict = {
    "sender": {
        "id": "1022980129309",
    },
    "recipient": {
        "id": "99028301980",
    },

}


@pytest.fixture
def message_dict():
    return msg_dict


# msg_dict_text = copy.deepcopy(message_dict)


msg_dict_text = {"message": {
    "mid": "mid.23jh4v342jh4b2",
    "text": "ping pong",
},
}

dict_delivered = {
    "delivery": {
        "mids": [
            "mid.1458668856218:ed81099e15d3f4f233",
            "mid.1458668856218:ed812139e15d3f4f233"
        ],
        "watermark": 14586123856253,
        "seq": 37
    }
}


@pytest.fixture
def message_dict_text():
    return msg_dict_text


@pytest.fixture
def message_dict_text1():
    msg_dict_text1 = copy.deepcopy(msg_dict_text)
    msg_dict_text1["message"]["mid"] = "mid.23jh4v342jh4b28asdgasd"
    msg_dict_text1["message"]["text"] = "ping pong"
    return msg_dict_text1


msg_dict_image = {"message": {
    "mid": "mid.127381b23t8712b1728b",
    "attachments": [
        {
            "type": "image",
            "payload": {
                "url": "https://thumbs.gfycat.com/FancyWateryHumpbackwhale-size_restricted.gif",
            },
        },
        {
            "type": "image",
            "payload": {
                "url": "https://thumbs.gfycat.com/ImpoliteSafeDorking-size_restricted.gif",
            }
        }
    ]
}}


@pytest.fixture
def message_dict_image_attach():
    return msg_dict_image


@pytest.fixture
def message_dict_image_attach1():
    msg_dict_image1 = copy.deepcopy(msg_dict_image)
    msg_dict_image1["mid"] = "mid.128973gb129ub1i2kb3"
    return msg_dict_image1


@pytest.fixture
def message_dict_received():
    return dict_delivered


def test_message_attrs(message_dict):
    msg_inst = message.Message(message_dict)
    assert msg_inst.user_id == message_dict["sender"]["id"]
    assert msg_inst.page_id == message_dict["recipient"]["id"]
    assert isinstance(msg_inst.message_received, message.Received)
    assert isinstance(msg_inst.message_delivered, message.Delivered)
    assert isinstance(msg_inst.message_read, message.Read)


def test_message_received(message_dict_text):
    msg_rec = message.Received(message_dict_text)
    assert msg_rec
    assert bool(msg_rec)
    assert msg_rec.mid
    assert msg_rec.mid == message_dict_text["message"]["mid"]
    assert msg_rec.text == message_dict_text["message"]["text"]
    assert not msg_rec.attachments
    assert msg_rec.message
    assert msg_rec.message == message_dict_text["message"]
    assert not hasattr(msg_rec, "postback_payload")


def test_message_equality(message_dict_text, message_dict_text1):
    msg_rec = message.Received(message_dict_text)
    msg_rec1 = message.Received(message_dict_text1)
    assert msg_rec == msg_rec1
    assert msg_rec is not msg_rec1
    msg_rec1.text = "king kong"
    assert not msg_rec == msg_rec1
    assert msg_rec is not msg_rec1


def test_message_image_attach(message_dict_image_attach):
    msg_rec_image = message.Received(message_dict_image_attach)
    assert isinstance(msg_rec_image.attachments, list)
    assert isinstance(msg_rec_image.attachments[0], message.Attachments)
    assert msg_rec_image.attachments[0].type == message_dict_image_attach["message"]["attachments"][0]["type"]
    assert msg_rec_image.attachments[1].type == message_dict_image_attach["message"]["attachments"][1]["type"]
    assert msg_rec_image.attachments[0].url == message_dict_image_attach["message"]["attachments"][0]["payload"]["url"]
    assert msg_rec_image.attachments[1].url == message_dict_image_attach["message"]["attachments"][1]["payload"]["url"]
    assert bool(msg_rec_image)
    assert not msg_rec_image.text


def test_message_image_attach_equality(message_dict_image_attach, message_dict_image_attach1):
    msg_rec_image = message.Received(message_dict_image_attach)
    msg_rec_image1 = message.Received(message_dict_image_attach1)
    assert msg_rec_image == msg_rec_image1
    assert msg_rec_image is not msg_rec_image1
    msg_rec_image1.attachments[0].url = "wuba luba dub dub"
    assert not msg_rec_image == msg_rec_image1
    assert msg_rec_image is not msg_rec_image1

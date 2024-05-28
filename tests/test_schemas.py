from email.schema import SenderConfig


def test_sender_configuration():
    sender = SenderConfig(email="test@kilo.com", password="test")
    assert sender.email == "test@kilo.com"
    assert sender.password == "test"

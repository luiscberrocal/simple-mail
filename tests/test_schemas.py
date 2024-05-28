from simple_mail.email.schema import SenderConfig


def test_sender_configuration() -> None:
    sender = SenderConfig(email="test@kilo.com", password="test")
    assert sender.email == "test@kilo.com"
    assert sender.password == "test"

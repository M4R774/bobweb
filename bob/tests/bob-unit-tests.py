import telepot
import sys
sys.path.append('../src')  # needed for sibling import
import message_handler
import bob
import wisdom

bot = telepot.Bot("1028389396:AAFXTRhz0efUWoDTgnbxvexkpaPktoR3X_I")
basic_message = {
    "from": {
        "id": "1234",
        "username": "TestiMies",
        "first_name": "Teemu",
        "last_name": "Teekkari"},
    "chat": {
        "id": "12345"
    },
    "text": "Tämä on ihan tavallinen viesti"
}
no_name_message = {"from": {
                       "id": "1234"}}
no_username_message = {"from": {
                       "id": "1234",
                       "first_name": "Teemu",
                       "last_name": "Teekkari"}}
only_lastname_message = {"from": {
                       "id": "1234",
                       "last_name": "Teekkari"}}
huutista_message_0 = {
    "from": {"id": "1234"},
    "text": "Huutista"
}
huutista_message_1 = {
    "from": {"id": "1234"},
    "text": "Huutista"
}
huutista_message_2 = {
    "from": {"id": "1234"},
    "text": "hUuTiStA"
}
wisdom_message_0 = {
    "from": {"id": "1234"},
    "text": "Viisaus"
}
wisdom_message_1 = {
    "from": {"id": "1234"},
    "text": "viisaus"
}
wisdom_message_2 = {
    "from": {"id": "1234"},
    "text": "vIiSaUs"
}
wisdom_message_invalid = {
    "from": {"id": "1234"},
    "text": "vIiSaUs!"
}
new_wisdom_0 = {
    "from": {"id": "1234"},
    "text": "uusi viisaus: Tämä on uusi viisaus"
}
new_wisdom_1 = {
    "from": {"id": "1234"},
    "text": "Uusi viisaus: ::!!Tämä on uusi viisaus!!"
}
new_wisdom_2 = {
    "from": {"id": "1234"},
    "text": "uUsI ViIsAuS: ::!!Tämä on uusi viisaus!!"
}
new_wisdom_invalid_0 = {
    "from": {"id": "1234"},
    "text": "uUsI ViIsAuS:"
}
new_wisdom_invalid_1 = {
    "from": {"id": "1234"},
    "text": "uusi viisaus Tämä on uusi viisaus"
}
new_wisdom_invalid_2 = {
    "from": {"id": "1234"},
    "text": "uusi viisaus:: Tämä on uusi viisaus"
}


class TestSuite:
    def test_tests(self):
        assert True == True

    def test_get_nickname(self):
        assert "TestiMies" == message_handler.get_nickname_from_message(basic_message)
        assert "1234" == message_handler.get_nickname_from_message(no_name_message)
        assert "Teemu" == message_handler.get_nickname_from_message(no_username_message)
        assert "Teekkari" == message_handler.get_nickname_from_message(only_lastname_message)

    def test_msg_sorter_huutista(self, mocker):
        mocker.patch("message_handler.joka_tuutista")
        message_handler.msg_sorter(basic_message, "Dummy parameter")
        message_handler.msg_sorter(huutista_message_0, "Dummy parameter")
        message_handler.joka_tuutista.assert_called_once_with(huutista_message_0, "Dummy parameter")
        message_handler.msg_sorter(huutista_message_1, "Dummy parameter")
        message_handler.joka_tuutista.assert_called_with(huutista_message_1, "Dummy parameter")
        message_handler.msg_sorter(huutista_message_2, "Dummy parameter")
        message_handler.joka_tuutista.assert_called_with(huutista_message_2, "Dummy parameter")

    def test_msg_sorter_wisdom(self, mocker):
        mocker.patch("wisdom.respond_with_random_wisdom")
        message_handler.msg_sorter(wisdom_message_invalid, "Dummy parameter")
        message_handler.msg_sorter(wisdom_message_0, "Dummy parameter")
        wisdom.respond_with_random_wisdom.assert_called_once_with(wisdom_message_0, "Dummy parameter")
        message_handler.msg_sorter(wisdom_message_1, "Dummy parameter")
        wisdom.respond_with_random_wisdom.assert_called_with(wisdom_message_1, "Dummy parameter")
        message_handler.msg_sorter(wisdom_message_2, "Dummy parameter")
        wisdom.respond_with_random_wisdom.assert_called_with(wisdom_message_2, "Dummy parameter")

    def test_msg_sorter_add_wisdom(self, mocker):
        mocker.patch("wisdom.add_new_wisdom_to_database")
        message_handler.msg_sorter(new_wisdom_invalid_0, "Dummy parameter")
        message_handler.msg_sorter(new_wisdom_invalid_1, "Dummy parameter")
        message_handler.msg_sorter(new_wisdom_invalid_2, "Dummy parameter")
        message_handler.msg_sorter(new_wisdom_0, "Dummy parameter")
        wisdom.add_new_wisdom_to_database.assert_called_once_with(new_wisdom_0, "Dummy parameter")
        message_handler.msg_sorter(new_wisdom_1, "Dummy parameter")
        wisdom.add_new_wisdom_to_database.assert_called_with(new_wisdom_1, "Dummy parameter")
        message_handler.msg_sorter(new_wisdom_2, "Dummy parameter")
        wisdom.add_new_wisdom_to_database.assert_called_with(new_wisdom_2, "Dummy parameter")

    def test_joka_tuutista(self, mocker):
        mock_bot = MockBob()
        mocker.patch.object(mock_bot, 'sendMessage')
        message_handler.joka_tuutista(basic_message, mock_bot)
        mock_bot.sendMessage.assert_called_once_with(basic_message['chat']['id'], '..joka tuutista! 😂')

    def test_respond_with_random_wisdom(self, mocker):
        mock_bot = MockBob()
        mocker.patch.object(mock_bot, 'sendMessage')
        mocker.patch("wisdom.stale_proverb")
        wisdom.stale_proverb.return_value = "Homeinen viisaus"
        wisdom.respond_with_random_wisdom(basic_message, mock_bot)
        mock_bot.sendMessage.assert_called_once_with(basic_message['chat']['id'], "Homeinen viisaus")

    def test_respond_with_random_wisdom(self, mocker):
        mock_bot = MockBob()
        mocker.patch.object(mock_bot, 'sendMessage')
        mocker.patch("wisdom.stale_proverb")
        wisdom.stale_proverb.return_value = "Homeinen viisaus"
        wisdom.respond_with_random_wisdom(basic_message, mock_bot)
        mock_bot.sendMessage.assert_called_once_with(basic_message['chat']['id'], "Homeinen viisaus")


class MockBob:
    def sendMessage(self, message, mock_bot):
        return 0

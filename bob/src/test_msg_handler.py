import telepot
import sys
sys.path.append('.')
import message_handler
import bob
import proverb

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
proverb_message_0 = {
    "from": {"id": "1234"},
    "text": "Viisaus"
}
proverb_message_1 = {
    "from": {"id": "1234"},
    "text": "viisaus"
}
proverb_message_2 = {
    "from": {"id": "1234"},
    "text": "vIiSaUs"
}
proverb_message_invalid = {
    "from": {"id": "1234"},
    "text": "vIiSaUs!"
}
new_proverb_0 = {
    "from": {"id": "1234"},
    "text": "uusi viisaus: Tämä on uusi viisaus"
}
new_proverb_1 = {
    "from": {"id": "1234"},
    "text": "Uusi viisaus: ::!!Tämä on uusi viisaus!!"
}
new_proverb_2 = {
    "from": {"id": "1234"},
    "text": "uUsI ViIsAuS: ::!!Tämä on uusi viisaus!!"
}
new_proverb_invalid_0 = {
    "from": {"id": "1234"},
    "text": "uUsI ViIsAuS:"
}
new_proverb_invalid_1 = {
    "from": {"id": "1234"},
    "text": "uusi viisaus Tämä on uusi viisaus"
}
new_proverb_invalid_2 = {
    "from": {"id": "1234"},
    "text": "uusi viisaus:: Tämä on uusi viisaus"
}
moldy_proverb_0 = {
    "proverb": "Homeinen viisaus"
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

    def test_msg_sorter_proverb(self, mocker):
        mocker.patch("proverb.respond_with_random_proverb")
        message_handler.msg_sorter(proverb_message_invalid, "Dummy parameter")
        message_handler.msg_sorter(proverb_message_0, "Dummy parameter")
        proverb.respond_with_random_proverb.assert_called_once_with(proverb_message_0, "Dummy parameter")
        message_handler.msg_sorter(proverb_message_1, "Dummy parameter")
        proverb.respond_with_random_proverb.assert_called_with(proverb_message_1, "Dummy parameter")
        message_handler.msg_sorter(proverb_message_2, "Dummy parameter")
        proverb.respond_with_random_proverb.assert_called_with(proverb_message_2, "Dummy parameter")

    def test_msg_sorter_add_proverb(self, mocker):
        mocker.patch("proverb.add_new_proverb_to_database")
        message_handler.msg_sorter(new_proverb_invalid_0, "Dummy parameter")
        message_handler.msg_sorter(new_proverb_invalid_1, "Dummy parameter")
        message_handler.msg_sorter(new_proverb_invalid_2, "Dummy parameter")
        message_handler.msg_sorter(new_proverb_0, "Dummy parameter")
        proverb.add_new_proverb_to_database.assert_called_once_with(new_proverb_0, "Dummy parameter")
        message_handler.msg_sorter(new_proverb_1, "Dummy parameter")
        proverb.add_new_proverb_to_database.assert_called_with(new_proverb_1, "Dummy parameter")
        message_handler.msg_sorter(new_proverb_2, "Dummy parameter")
        proverb.add_new_proverb_to_database.assert_called_with(new_proverb_2, "Dummy parameter")

    def test_joka_tuutista(self, mocker):
        mock_bot = MockBob()
        mocker.patch.object(mock_bot, 'sendMessage')
        message_handler.joka_tuutista(basic_message, mock_bot)
        mock_bot.sendMessage.assert_called_once_with(basic_message['chat']['id'], '..joka tuutista! 😂')

    def test_respond_with_random_proverb(self, mocker):
        mock_bot = MockBob()
        mocker.patch.object(mock_bot, 'sendMessage')
        mocker.patch("proverb.get_last_proverb_with_randomness")
        mocker.patch("proverb.update_proverb_access_date_and_count")
        proverb.get_last_proverb_with_randomness.return_value = MockProverb()
        proverb.respond_with_random_proverb(basic_message, mock_bot)
        mock_bot.sendMessage.assert_called_once_with(basic_message['chat']['id'], "Homeinen viisaus ")

    def test_add_new_proverb_to_database(self, mocker):
        mock_bot = MockBob()

        # Negative test
        mocker.patch.object(mock_bot, 'sendMessage')
        proverb.add_new_proverb_to_database(new_proverb_invalid_0, mock_bot)
        proverb.add_new_proverb_to_database(new_proverb_invalid_1, mock_bot)
        proverb.add_new_proverb_to_database(new_proverb_invalid_2, mock_bot)
        mock_bot.sendMessage.assert_not_called()

        # Positive test
        proverb.add_new_proverb_to_database(new_proverb_0, mock_bot)
        mock_bot.sendMessage.assert_called_once_with(basic_message['chat']['id'], 'Viisaus tallennettu. ')
        mocker.reset_mock()

        proverb.add_new_proverb_to_database(new_proverb_1, mock_bot)
        mock_bot.sendMessage.assert_called_once_with(basic_message['chat']['id'], 'Viisaus tallennettu. ')
        mocker.reset_mock()

        proverb.add_new_proverb_to_database(new_proverb_2, mock_bot)
        mock_bot.sendMessage.assert_called_once_with(basic_message['chat']['id'], 'Viisaus tallennettu. ')
        mocker.reset_mock()


class MockBob:
    def sendMessage(self, message, mock_bot):
        return 0


class MockProverb:
    def __init__(self):
        self.author = None
        self.date = None
        self.proverb = "Homeinen viisaus"
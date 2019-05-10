import personal_assistant

Jarvis = personal_assistant.PersonalAssistant()

while Jarvis.is_active():
    input = Jarvis.listen_for_audio()
    Jarvis.handle_audio(input)
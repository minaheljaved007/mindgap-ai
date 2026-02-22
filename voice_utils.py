from gtts import gTTS


def text_to_voice(text,file="reply.mp3"):

 tts=gTTS(text)

 tts.save(file)

 return file

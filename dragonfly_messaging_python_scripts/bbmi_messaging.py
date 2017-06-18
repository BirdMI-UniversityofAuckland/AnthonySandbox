# bbmi messaging


# copy sound buffer to message
def copy_to_sound_msg(sound_msg, sound_buffer, buffer_index, BUFFER_SIZE):

    for i in range(0, BUFFER_SIZE):
        sound_msg.buffer[i] = sound_buffer[BUFFER_SIZE * (buffer_index - 1) + i]

    return

# copy sound message to buffer


def copy_to_sound_buffer(sound_msg, sound_buffer, buffer_index, BUFFER_SIZE):

    for i in range(0, BUFFER_SIZE):
        sound_buffer[BUFFER_SIZE * (buffer_index - 1) + i] = sound_msg.buffer[i]

    return

def save_msg_to_file(msg_p=None):
    if msg_p is None:
        msg_p = []
    msg_p.append(b'\x0a')
    msg_p.append(b'\x0f')
    print(type(msg_p))
    with open("output.bin", "wb") as f:
        for child in msg_p:
            f.write(child)

save_msg_to_file()
# -*- coding: utf-8 -*-

"""Special utils created to work with net and other interaction.
"""
import socket


def get_local_ip() -> str:
    """Get localhost address.
    """
    target_ip = '8.8.8.8'
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        s.connect((target_ip, 1))
        local_ip = s.getsockname()[0]
    except socket.error:
        local_ip = '127.0.0.1'
    finally:
        s.close()

    return local_ip

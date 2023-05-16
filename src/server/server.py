import socket
import threading
import pickle
from typing import List, Dict, Optional, Type

from metaclass.singleton import SingletonMeta
from data.processdata import ProcessData

HOST = None
PORT = None


class SocketServer(metaclass=SingletonMeta):
    def __init__(self):
        global HOST, PORT
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._host = HOST if HOST else socket.gethostbyname(socket.gethostname())
        self._port = PORT if PORT else 23009
        self._socket.bind((self._host, self._port))
        self._client_list: List[socket.socket] = []
        self._thread_list: List[threading.Thread] = []
        self._player_name_list: Dict[socket.socket, str] = []
        self._owner: Optional[socket.socket] = None
        return None

    def _start(self):
        while True:
            self._socket.listen()
            client_socket, client_address = self._socket.accept()
            self._client_list.append(client_socket)
            self._thread_list.append(
                threading.Thread(
                    target=self._handle_client, args=(client_socket, client_address)
                )
            )

    def _handle_client(
        self, client_socket: socket.socket, client_address: socket._RetAddress
    ) -> None:
        while client_socket in self._client_list:
            try:
                data: ProcessData = pickle.loads(client_socket.recv(4096))
                if not data:
                    break
                else:
                    print(f"{client_address}:{data}")
                    pass

                data.action = data.action.upper()

                if data.action == "NAME":
                    self._player_name_list[client_socket] = data.target
                    self._broadcast(data, client_socket, True)
                    pass
                # Room Owner
                elif client_socket is self._owner:
                    if data.action == "KICK":
                        if data.target is not None:
                            self._kick_client(data.target)
                            pass
                    pass
                # Room Member
                else:
                    pass
                pass

            except BaseException:
                break
            continue
        return None

    def _broadcast(
        self,
        data: Type[ProcessData],
        sender: socket.socket,
        send_to_sender: bool = False,
    ) -> None:
        message = pickle.dumps(data)
        for client in self._client_list:
            if client is not sender or send_to_sender:
                client.send(message)
                pass
            continue
        return None

    def _kick_client(self, target: str) -> None:
        for client in self._client_list:
            if self._player_name_list[client] == target:
                client.close()
                self._client_list.remove(client)
                self._player_name_list.pop(client)
                break
            continue
        return None

    @property
    def host(self):
        return self._host

    @property
    def port(self):
        return self._port

    @host.setter
    def host(self, host):
        self._host = host
        self._socket.bind((self._host, self._port))
        return None

    @port.setter
    def port(self, port):
        self._port = port
        self._socket.bind((self._host, self._port))
        return None

    pass

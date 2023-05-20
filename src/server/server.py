import socket
import threading
import pickle
from typing import List, Dict, Optional, Type, Tuple, Any
from typing_extensions import TypeAlias

from metaclass.singleton import SingletonMeta
from data.processdata import ProcessData

_RetAddress: TypeAlias = Any

HOST = None
PORT = None


class SocketServer(metaclass=SingletonMeta):
    # def __init__(self):
    #     return None

    def initialize(self) -> None:
        self.run_thread: bool = False
        if hasattr(self, "_thread") and self._thread:
            self._thread.join()
            del self._thread
            pass
        global HOST, PORT
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._host = HOST if HOST else socket.gethostbyname(socket.gethostname())
        self._port = PORT if PORT else 23009
        self._socket.bind((self._host, self._port))
        self._client_list: List[socket.socket] = []
        self._thread_list: List[threading.Thread] = []
        self._player_name_dict: Dict[socket.socket, str] = {}
        self._owner: Optional[socket.socket] = None
        self._thread: threading.Thread = threading.Thread(target=self._start)
        self.run_thread: bool = True
        self._thread.start()
        return None

    def _start(self) -> None:
        print(f"[Server] Start Listening on {self._host}:{self._port}")
        while self.run_thread:
            self._socket.listen()
            (
                client_socket,
                client_address,
            ) = self._socket.accept()  # type: Tuple[socket.socket, Tuple[str, int]]
            self._client_list.append(client_socket)
            self._thread_list.append(
                threading.Thread(
                    target=self._handle_client, args=(client_socket, client_address)
                )
            )
            self._thread_list[-1].start()
            continue
        for client in self._client_list:
            client.close()
            del client
            continue
        for thread in self._thread_list:
            thread.join()
            del thread
            continue
        self._socket.close()
        del self._socket
        print(f"[Server] Stop Listening on {self._host}:{self._port}")
        return None

    def _handle_client(
        self, client_socket: socket.socket, client_address: _RetAddress
    ) -> None:
        print(f"[Server] {client_address[0]}:{client_address[1]} connected")
        while client_socket in self._client_list:
            try:
                data: ProcessData = pickle.loads(client_socket.recv(4096))
                if not data:
                    break
                else:
                    print(f"{client_address[0]}:{client_address[1]}:{data}")
                    pass

                data.action = data.action.upper()

                if data.action == "NAME":
                    self._player_name_dict.update({client_socket: data.target})
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
                if client_socket in self._client_list:
                    self._client_list.remove(client_socket)
                    if client_socket in self._player_name_dict.keys():
                        name: str = self._player_name_dict.pop(client_socket)
                        self._broadcast(
                            ProcessData("DISCONNECT", name, None), client_socket, True
                        )
                        pass
                    pass
                client_socket.close()

                if self._client_list:
                    if client_socket is self._owner:
                        self._owner = self._client_list[0]
                        self._broadcast(
                            ProcessData(
                                "OWNER", self._player_name_dict.get(self._owner)
                            ),
                            self._owner,
                            True,
                        )
                        pass
                    pass
                break
            continue
        print(f"[Server] {client_address[0]}:{client_address[1]} disconnected")
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
            if self._player_name_dict.get(client) == target:
                client.close()
                self._client_list.remove(client)
                self._player_name_dict.pop(client)
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

import socket
from threading import Thread, Event
import pickle
from typing import List, Dict, Optional, Type, Tuple, Any, Final
from typing_extensions import TypeAlias

from metaclass.singleton import SingletonMeta
from data.processdata import ProcessData
import util.bcolors as color

_RetAddress: TypeAlias = Any

HOST = None
PORT = None

stop_thread: Event = Event()
max_players: Final[int] = 6


class SocketServer(metaclass=SingletonMeta):
    # def __init__(self):
    #     return None

    def initialize(self) -> bool:
        global HOST, PORT
        self._host = HOST if HOST else socket.gethostbyname(socket.gethostname())
        self._port = PORT if PORT else 23009
        self.close()
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            self._socket.bind((self._host, self._port))
            print(f"{color.CBLUEBG}[Server] Server started{color.CEND}")
            pass
        except BaseException:
            print(f"{color.CREDBG}[Server] Cannot start server{color.CEND}")
            return False
        self._client_list: List[socket.socket] = []
        self._thread_list: List[Thread] = []
        # self._client_addr_list: List[_RetAddress] = []
        self._player_name_dict: Dict[socket.socket, str] = {}
        self._player_name_list: List[str] = []
        self._owner: Optional[socket.socket] = None
        self._thread: Thread = Thread(target=self._start)
        stop_thread.clear()
        self._thread.start()
        return True

    def close(self) -> None:
        stop_thread.set()
        # if hasattr(self, "_socket") and self._socket:
        #     self._socket.shutdown(socket.SHUT_RDWR)
        if hasattr(self, "_socket") and self._socket:
            try:
                socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect(
                    (self._host, self._port)
                )
                pass
            except BaseException:
                pass
            self._socket.close()
            del self._socket
            pass
        if hasattr(self, "_thread") and self._thread:
            self._thread.join()
            del self._thread
            pass
        return None

    def _start(self) -> None:
        print(
            f"{color.CBLUEBG}[Server] Start Listening on {self._host}:{self._port}{color.CEND}"
        )
        while not stop_thread.is_set():
            self._socket.listen()
            (
                client_socket,
                client_address,
            ) = self._socket.accept()  # type: Tuple[socket.socket, _RetAddress]
            if len(self._client_list) >= max_players:
                client_socket.send(pickle.dumps(ProcessData("SERVER", "FULL", None)))
                client_socket.close()
                continue
            self._client_list.append(client_socket)
            self._thread_list.append(
                Thread(target=self._handle_client, args=(client_socket, client_address))
            )
            self._thread_list[-1].start()
            continue
        for client in self._client_list:
            client.close()
            self._client_list.remove(client)
            del client
            continue
        for thread in self._thread_list:
            thread.join()
            self._thread_list.remove(thread)
            del thread
            continue
        if hasattr(self, "_socket") and self._socket:
            self._socket.close()
            del self._socket
            pass
        print(
            f"{color.CYELLOWBG}[Server] Stop Listening on {self._host}:{self._port}{color.CEND}"
        )
        return None

    def _handle_client(
        self, client_socket: socket.socket, client_address: _RetAddress
    ) -> None:
        print(
            f"{color.CBLUEBG}[Server] {client_address[0]}:{client_address[1]} connected{color.CEND}"
        )
        while client_socket in self._client_list and not stop_thread.is_set():
            try:
                data: ProcessData = pickle.loads(client_socket.recv(4096))
                if not data:
                    break
                else:
                    print(
                        f"{color.CBLUEBG}[Server] {client_address[0]}:{client_address[1]} > {data}{color.CEND}"
                    )
                    pass

                data.action = data.action.upper()

                if data.action == "NAME":
                    while data.target in self._player_name_list:
                        data.target += "_"
                        continue
                    self._player_name_dict.update({client_socket: data.target})
                    self._player_name_list.remove(data.player)
                    self._player_name_list.append(data.target)
                    self._broadcast(data, client_socket)
                    pass
                elif data.action == "JOIN":
                    while data.player in self._player_name_list:
                        data.player += "_"
                        continue
                    client_socket.send(
                        pickle.dumps(
                            ProcessData(
                                "SERVER",
                                "INFO",
                                {
                                    "player_list": self._player_name_list,
                                    "owner": self._player_name_dict.get(self._owner),
                                    "username": data.player,
                                },
                            )
                        )
                    )
                    self._player_name_dict.update({client_socket: data.player})
                    self._player_name_list.append(data.player)
                    self._broadcast(data, client_socket)
                    if self._owner is None:
                        self._owner = client_socket
                        client_socket.send(
                            pickle.dumps(
                                ProcessData(data.player, "OWNER", client_address)
                            )
                        )
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
                        self._player_name_list.remove(name)
                        self._broadcast(
                            ProcessData(name, "DISCONNECT", None), client_socket
                        )
                        pass
                    pass
                client_socket.close()

                if self._client_list:
                    if client_socket is self._owner:
                        # self._owner = self._client_list[0]
                        # self._broadcast(
                        #     ProcessData(
                        #         self._player_name_dict.get(self._owner),
                        #         "OWNER",
                        #         self._owner.getpeername(),
                        #     ),
                        #     self._owner,
                        #     True,
                        # )
                        self._broadcast(
                            ProcessData(
                                "SERVER",
                                "CLOSE",
                            ),
                        )
                        pass
                    pass
                break
            continue
        print(
            f"{color.CBLUEBG}[Server] {client_address[0]}:{client_address[1]} disconnected{color.CEND}"
        )
        return None

    def _broadcast(
        self,
        data: Type[ProcessData],
        sender: Optional[socket.socket] = None,
    ) -> None:
        message = pickle.dumps(data)
        for client in self._client_list:
            if sender is None or client is not sender:
                client.send(message)
                pass
            continue
        return None

    def _kick_client(self, target: str) -> None:
        for client in self._client_list:
            if self._player_name_dict.get(client) == target:
                client.send(pickle.dumps(ProcessData("SERVER", "KICK", None)))
                client.close()
                self._client_list.remove(client)
                self._player_name_list.remove(self._player_name_dict.pop(client))
                self._broadcast(ProcessData(target, "DISCONNECT", None))
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

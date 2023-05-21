import socket
from threading import Thread, Event
import pickle
from typing import List, Optional
import copy

# from typing_extensions import TypeAlias

from metaclass.singleton import SingletonMeta
from data.processdata import ProcessData

# _RetAddress: TypeAlias = Any


SERVER_IP = None
SERVER_PORT = None

stop_thread: Event = Event()


class SocketClient(metaclass=SingletonMeta):
    def initialize(self) -> bool:
        self.close()
        global SERVER_IP, SERVER_PORT
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        if not hasattr(self, "_host") or self._host is None:
            self._host = (
                SERVER_IP if SERVER_IP else socket.gethostbyname(socket.gethostname())
            )
            pass
        self._port = SERVER_PORT if SERVER_PORT else 23009
        try:
            self._socket.connect((self._host, self._port))
            print(f"[Client] Connected to {self._host}:{self._port}")
            pass
        except BaseException:
            print("[Client] Cannot connect to server")
            return False
        self._data_queue: List[ProcessData] = []
        self._thread: Thread = Thread(target=self._start)
        stop_thread.clear()
        self._thread.start()
        return True

    def close(self) -> None:
        stop_thread.set()
        if hasattr(self, "_socket") and self._socket:
            self._socket.shutdown(socket.SHUT_RDWR)
        if hasattr(self, "_thread") and self._thread:
            self._thread.join()
            del self._thread
            pass
        return None

    def _start(self) -> None:
        print("[Client] Message receiving thread started")
        while not stop_thread.is_set():
            try:
                data: ProcessData = pickle.loads(self._socket.recv(4096))
                if not data:
                    break
                else:
                    print(f"[Client] {self._host}:{self._port} > {data}")
                    pass

                data.action = data.action.upper()

                if data.action == "JOIN":
                    print(f"[Client] {data.player} joined game room")
                    pass
                elif data.action == "NAME":
                    print(f"[Client] {data.player} changed name to {data.target}")
                    pass
                elif data.action == "DISCONNECT":
                    print(f"[Client] {data.player} left game room")
                elif data.action == "KICK":
                    print("[Client] Kicked by host")
                    self._socket.close()
                    self.run_thread = False
                    break
                elif data.action == "OWNER":
                    if data.target == self._socket.getsockname():
                        print("[Client] You are the owner")
                        pass
                    else:
                        print(f"[Client] {data.player} is the owner")
                        pass
                    pass
                else:
                    print(f"[Client] invalid data: {data}")
                    continue
                self._data_queue.append(copy.deepcopy(data))
            except BaseException:
                print("[Client] Connection to server lost")
                self._socket.close()
                stop_thread.set()
                break
        print("[Client] Message receiving thread terminated")
        return None

    def send_data(self, player: str, action: str, target: Optional[str] = None) -> None:
        data = ProcessData(player, action, target)
        print(f"[Client] {self._host}:{self._port} < {data}")
        self._socket.send(pickle.dumps(data))
        return None

    @property
    def host(self) -> str:
        return self._host

    @host.setter
    def host(self, value: str) -> None:
        self._host = value
        return None

    @property
    def port(self) -> int:
        return self._port

    @port.setter
    def port(self, value: int) -> None:
        self._port = value
        return None

    def get_data(self) -> List[ProcessData]:
        data = copy.deepcopy(self._data_queue)
        self._data_queue = []
        return data

    def poll_data(self) -> ProcessData:
        if len(self._data_queue) > 0:
            return copy.deepcopy(self._data_queue.pop(0))
        return None

    pass

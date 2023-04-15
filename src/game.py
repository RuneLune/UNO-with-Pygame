import copy
import random
from typing import List, Dict, Iterable, Type

from bot import Bot
import cards
from player import Player
from timer import Timer


class Game:
    # MAX_Inst = 1
    # Inst_created = 0

    # Game 클래스 생성자
    def __new__(cls, *args, **kwargs):
        # if cls.Inst_created >= cls.MAX_Inst:
        #     raise ValueError("Cannot create more Game object")
        # cls.Inst_created += 1
        return super(Game, cls).__new__(cls)

    # Game 객체 초기화 메서드
    def __init__(
        self,
        players_count: int,
        username: str = "Player",
        turn_seconds: int = 10,
        round_seconds: int = 0,
        max_rounds: int = 0,
        target_score: int = 500,
    ) -> None:
        self._init_variables(turn_seconds, round_seconds, max_rounds, target_score)
        self._add_players(username, players_count)
        self._make_draw_pile()
        self._deal_hands()
        self._flip_top()

        self._players[self._current_turn].turn_start()

        return super().__init__()

    # 멤버 변수 초기화 메서드
    def _init_variables(
        self,
        turn_seconds: int = 10,
        round_seconds: int = 0,
        max_rounds: int = 0,
        target_score: int = 500,
    ) -> None:
        self._players: List[Type[Player]] = []

        self._turn_timer: Timer = Timer()
        self._round_timer: Timer = Timer()

        self._turn_seconds: int = turn_seconds
        self._round_seconds: int = round_seconds
        self._max_rounds: int = max_rounds
        self._target_score: int = target_score

        self._force_draw: int = 0
        self._reverse_direction: bool = False
        self._current_turn: int = 1
        self._skip_turn: bool = False
        # self._player_drawed: bool = False

        return None

    # 봇 및 플레이어를 추가하는 메서드
    def _add_players(self, username: str = "Player", players_count: int = 4) -> None:
        self._user: Player = Player(self, username)
        self._players.append(self._user)
        for i in range(1, players_count):
            self._players.append(Bot(self, "Computer " + str(i)))
            continue
        random.shuffle(self._players)
        return None

    # Draw pile에 카드를 추가하고 섞는 메서드
    def _make_draw_pile(self) -> None:
        self._draw_pile: List[int] = (
            list(range(cards.blue_0, cards.blue_skip + 1))
            + list(range(cards.blue_1, cards.blue_skip + 1))
            + list(range(cards.green_0, cards.green_skip + 1))
            + list(range(cards.green_1, cards.green_skip + 1))
            + list(range(cards.red_0, cards.red_skip + 1))
            + list(range(cards.red_1, cards.red_skip + 1))
            + list(range(cards.yellow_0, cards.yellow_skip + 1))
            + list(range(cards.yellow_1, cards.yellow_skip + 1))
            + list(range(cards.wild_normal, cards.wild_draw4 + 1)) * 4
        )
        random.shuffle(self._draw_pile)
        return None

    # 플레이어에게 패를 분배하는 메서드
    def _deal_hands(self, count: int = 7) -> None:
        for i in range(0, len(self._players)):
            self._players[i].draw_cards(count)
            continue
        return None

    # Draw pile 맨 위에서 카드를 뒤집어 시작 카드를 정하는 메서드
    def _flip_top(self) -> None:
        self._discard_pile: List[int] = self._draw_pile[:1]
        self._draw_pile = self._draw_pile[1:]
        self._discarded_card: Dict[str, str | int] = cards.check_card(
            self._discard_pile[0]
        )

        while self._discarded_card.get("type", None) == "draw4":
            self._draw_pile += self._discard_pile
            self._discard_pile = self._draw_pile[:1]
            self._draw_pile = self._draw_pile[1:]
            self._discarded_card = cards.check_card(self._discard_pile[0])
            continue

        if self._discarded_card.get("type", None) == "draw2":
            self._force_draw = 2
            pass
        elif self._discarded_card.get("type", None) == "reverse":
            self._current_turn = 0
            self._reverse_direction = True
            pass
        elif self._discarded_card.get("type", None) == "skip":
            self._current_turn = 2 % len(self._players)
            pass
        elif self._discarded_card.get("color", None) == "wild":
            self._players[1].choose_color()
            pass

        return None

    # Discard pile에 있는 카드를 섞고 Draw pile에 추가하는 메서드
    def _shuffle(self) -> None:
        discarded_cards: List[int] = self._discard_pile[1:]
        random.shuffle(discarded_cards)
        self._draw_pile += discarded_cards
        self._discard_pile = self._discard_pile[:1]
        return None

    # 마지막으로 낸 카드 정보를 반환하는 메서드
    def get_discard_info(self) -> Dict[str, int | Dict[str, str | int]]:
        return {
            "force_draw": self._force_draw,
            "discarded_card": copy.deepcopy(self._discarded_card),
        }

    # player에게 Draw pile에서 count만큼 카드를 주는 메서드
    def draw_cards(self, count: int, player: Type[Player]) -> None:
        # 강제 드로우 수 확인
        if self._force_draw > 0:
            if count != self._force_draw:
                raise ValueError("must draw " + str(self._force_draw) + " cards")

        # 남은 카드가 부족하면 패 섞고 드로우
        if count >= len(self._draw_pile):
            self._shuffle()
        drawing_cards: List[int] = copy.deepcopy(self._draw_pile[:count])
        self._draw_pile = self._draw_pile[count:]
        player.get_cards(drawing_cards)
        # self._player_drawed = True
        # 뽑은 카드가 낼 수 있는 경우 처리(미구현)
        if len(drawing_cards) == 1:
            draw_card = cards.check_card(drawing_cards[0])
            if (
                draw_card.get("color") == "wild"
                or draw_card.get("color") == self._discarded_card.get("color")
                or draw_card.get("number") == self._discarded_card.get("number")
            ):
                self._players[self._current_turn].ask_discard()
        self._force_draw = 0
        return None

    # card를 Discard pile에 추가하고 처리하는 메서드
    def discard_card(self, card: int) -> None:
        self._discarded_card = cards.check_card(card)
        # 기술 카드 처리
        if self._discarded_card.get("type") == "draw2":
            self._force_draw += 2
        elif self._discarded_card.get("type") == "reverse":
            if self._reverse_direction is False:
                self._reverse_direction = True
            else:
                self._reverse_direction = False
        elif self._discarded_card.get("type") == "skip":
            self._skip_turn = True
        elif self._discarded_card.get("color") == "wild":
            if self._discarded_card.get("type") == "draw4":
                self._force_draw += 4
            elif self._discarded_card.get("type") == "shuffle":
                shuffle_pile: List[int] = []
                for i in range(0, len(self._players)):
                    shuffle_pile += self._players[i].get_hand_cards()
                    self._players[i].set_cards([])
                random.shuffle(shuffle_pile)
                while len(shuffle_pile) == 0:
                    self._players[
                        (self._current_turn + 1) % len(self._players)
                    ].get_cards([shuffle_pile.pop(0)])
            self._players[self._current_turn].choose_color(self)

        # self._next_turn()
        return None

    # 우승자(즉, 손에 카드가 없는 플레이어)가 있는지 확인하는 메서드
    def check_winner(self) -> None:
        if len(self._players[self._current_turn].get_hand_cards()) == 0:
            self._end_round()
        return None

    # 라운드 종료 후 점수를 계산하는 메서드
    def _end_round(self) -> None:
        points: int = 0
        for i in range(0, len(self._players)):
            if i != self._current_turn:
                points += self._calc_points(
                    self._players[self._current_turn].get_hand_cards()
                )
        self._players[self._current_turn].add_points(points)
        return None

    # cards_list에 있는 카드들의 점수를 계산하는 메서드
    def _calc_points(self, cards_list: Iterable[int]) -> int:
        points: int = 0
        for card in cards_list:
            card_info: Dict[str, str | int] = cards.check_card(card)
            if card_info.get("number") <= 9:
                points += card_info.get("number")
            elif card_info.get("number") <= 12:
                points += 20
            elif card_info.get("number") <= 14:
                points += 50
            elif card_info.get("number") <= 16:
                points += 40
        return points

    # player가 우노를 외칠 수 있는 상황인지 확인하고 처리하는 메서드
    def check_uno(self, player: Type[Player]) -> None:
        if (
            len(player.get_hand_cards()) == 2
            and len(player.get_discardable_cards_index()) >= 1
        ):
            pass
        else:
            self.draw_cards(3, player)
        return None

    # Game 객체 내의 플레이어 배열을 반환하는 메서드
    def get_players(self) -> List[Type[Player]]:
        return self._players

    # 플레이어가 턴 종료 시 호출하는 메서드
    def end_turn(self) -> None:
        while self._players[self._current_turn]._can_end_turn is False:
            self._players[self._current_turn].draw_cards(1)
        self._next_turn()
        return None

    # 다음 턴의 플레이어를 계산하는 메서드
    def _next_turn(self) -> None:
        # self._player_drawed = False

        # 스킵 및 방향 확인해 턴 넘기기
        if self._skip_turn is False:
            if self._reverse_direction is False:
                self._current_turn = (self._current_turn + 1) % len(self._players)
                pass
            else:
                self._current_turn = (self._current_turn - 1) % len(self._players)
                pass
            pass
        else:
            if self._reverse_direction is False:
                self._current_turn = (self._current_turn + 2) % len(self._players)
                pass
            else:
                self._current_turn = (self._current_turn - 2) % len(self._players)
                pass
            pass
        self._players[self._current_turn].turn_start()

        return None

    # Game 객체 내의 모든 타이머를 활성화하는 메서드
    def start_timer(self) -> None:
        self._turn_timer.start()
        self._round_timer.start()
        return None

    # Game 객체 내의 모든 타이머를 일시정지하는 메서드
    def pause_timer(self) -> None:
        self._turn_timer.pause()
        self._round_timer.pause()
        return None

    # Game 객체 내의 모든 일시정지된 타이머를 재개하는 메서드
    def resume_timer(self) -> None:
        self._turn_timer.resume()
        self._round_timer.resume()
        return None

    def set_color(self, color: int | str) -> None:
        if color == 1 or color == "blue":
            self._discarded_card.update(color="blue")
            pass
        elif color == 2 or color == "green":
            self._discarded_card.update(color="green")
            pass
        elif color == 3 or color == "red":
            self._discarded_card.update(color="red")
            pass
        elif color == 4 or color == "yellow":
            self._discarded_card.update(color="yellow")
            pass
        else:
            raise ValueError("Invalid Color")
        return None

from pathlib import Path

import pygame

from screens.loading import LoadingScreen
from screens.login import LoginScreen
from screens.music import discover_music_tracks
from screens.crt_effect import CRTPostProcessor
from screens.theme import CANVAS_SCALE, CANVAS_SIZE, DEEP_TEAL, INK, LOGICAL_SIZE, MINT, SALMON, WHITE, YELLOW, draw_rect, text
from screens.trading_floor import TradingFloorScreen


WINDOW_SIZE = CANVAS_SIZE
ASSET_PATH = Path(__file__).parent / "png's" / "image.jpg"
ROOM_PATH = Path(__file__).parent / "Trade_haus_XL.png"
LOADING_BACKGROUND_PATH = Path(__file__).parent / "screens" / "Miami Synthwave Trading Terrace.png"
LOGIN_BACKGROUND_PATH = Path(__file__).parent / "screens" / "Neon Cyber-Miami Trading Lounge.png"
MUSIC_DIRECTORY = Path(__file__).parent / "music"
MUSIC_PATH = MUSIC_DIRECTORY / "HOME - Resonance - Electronic Gems (128k).mp3"
LOGIN_MUSIC_PATH = MUSIC_DIRECTORY / "YUNG BAE - You're Love - ALUMINIUM TARMAC (128k).mp3"
IN_GAME_MUSIC_PATHS = discover_music_tracks(MUSIC_DIRECTORY)
EXIT_Y_BUTTON = pygame.Rect(190, 204, 110, 22)
EXIT_N_BUTTON = pygame.Rect(340, 204, 110, 22)


def exit_prompt_decision(event: pygame.event.Event, window_size: tuple[int, int]) -> bool | None:
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_y:
            return True
        if event.key in (pygame.K_n, pygame.K_ESCAPE):
            return False
        return None
    if event.type != pygame.MOUSEBUTTONDOWN or event.button != 1:
        return None

    window_width, window_height = window_size
    scale = min(window_width / CANVAS_SIZE[0], window_height / CANVAS_SIZE[1])
    offset_x = (window_width - CANVAS_SIZE[0] * scale) / 2
    offset_y = (window_height - CANVAS_SIZE[1] * scale) / 2
    logical_position = (
        int((event.pos[0] - offset_x) / (scale * CANVAS_SCALE)),
        int((event.pos[1] - offset_y) / (scale * CANVAS_SCALE)),
    )
    if EXIT_Y_BUTTON.collidepoint(logical_position):
        return True
    if EXIT_N_BUTTON.collidepoint(logical_position):
        return False
    return None


def present(logical_surface: pygame.Surface, window: pygame.Surface) -> None:
    window.fill((8, 39, 49))
    scale = min(window.get_width() / CANVAS_SIZE[0], window.get_height() / CANVAS_SIZE[1])
    scaled_size = (int(CANVAS_SIZE[0] * scale), int(CANVAS_SIZE[1] * scale))
    scaled = pygame.transform.scale(logical_surface, scaled_size)
    window.blit(
        scaled,
        ((window.get_width() - scaled_size[0]) // 2, (window.get_height() - scaled_size[1]) // 2),
    )
    pygame.display.flip()


def draw_exit_prompt(surface: pygame.Surface) -> None:
    shade = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
    shade.fill((2, 15, 23, 205))
    surface.blit(shade, (0, 0))
    draw_rect(surface, INK, (158, 125, 324, 110))
    draw_rect(surface, YELLOW, (158, 125, 324, 110), 2)
    draw_rect(surface, DEEP_TEAL, (166, 133, 308, 18))
    text(surface, "SYSTEM / EXIT", (176, 138), 8, MINT, True)
    text(surface, "DO YOU WANT TO EXIT?", (188, 168), 14, WHITE, True)
    draw_rect(surface, DEEP_TEAL, EXIT_Y_BUTTON)
    draw_rect(surface, MINT, EXIT_Y_BUTTON, 1)
    draw_rect(surface, DEEP_TEAL, EXIT_N_BUTTON)
    draw_rect(surface, SALMON, EXIT_N_BUTTON, 1)
    text(surface, "Y  YES", (EXIT_Y_BUTTON.x + 34, EXIT_Y_BUTTON.y + 7), 8, MINT, True)
    text(surface, "N  NO", (EXIT_N_BUTTON.x + 35, EXIT_N_BUTTON.y + 7), 8, SALMON, True)


def main() -> None:
    pygame.init()
    pygame.display.set_caption("TRADEHAUS | Trade from the villa")
    window = pygame.display.set_mode(WINDOW_SIZE, pygame.RESIZABLE)
    pygame.display.set_icon(pygame.image.load(str(ASSET_PATH)).convert())
    canvas = pygame.Surface(CANVAS_SIZE)
    clock = pygame.time.Clock()
    loading = LoadingScreen(ASSET_PATH, MUSIC_PATH, LOADING_BACKGROUND_PATH)
    crt_effect = CRTPostProcessor()
    login: LoginScreen | None = None
    trading_floor: TradingFloorScreen | None = None
    active_screen = loading
    running = True
    exit_prompt = False

    while running:
        elapsed = clock.tick(60) / 1000
        for event in pygame.event.get():
            event = crt_effect.unwarp_event(event, window.get_size(), CANVAS_SIZE)
            if event.type == pygame.QUIT:
                exit_prompt = True
            elif exit_prompt:
                decision = exit_prompt_decision(event, window.get_size())
                if decision is True:
                    running = False
                elif decision is False:
                    exit_prompt = False
            elif isinstance(active_screen, LoadingScreen) and event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                exit_prompt = True
            elif isinstance(active_screen, LoadingScreen):
                if active_screen.handle_event(event):
                    loading.close()
                    login = LoginScreen(ASSET_PATH, LOGIN_MUSIC_PATH, LOGIN_BACKGROUND_PATH)
                    active_screen = login
            elif login is not None:
                login.handle_event(event)
            elif trading_floor is not None:
                trading_floor.handle_event(event)

        if not running:
            break
        if isinstance(active_screen, LoadingScreen):
            active_screen.update(elapsed)
            if active_screen.finished:
                loading.close()
                login = LoginScreen(ASSET_PATH, LOGIN_MUSIC_PATH, LOGIN_BACKGROUND_PATH)
                active_screen = login
        elif login is not None and login.connector.is_connected:
            connector = login.transfer_connector()
            login = None
            trading_floor = TradingFloorScreen(
                connector,
                ASSET_PATH,
                ROOM_PATH,
                None,
                IN_GAME_MUSIC_PATHS,
                threaded_feed=True,
            )
            active_screen = trading_floor

        if trading_floor is not None:
            trading_floor.update(elapsed)
            if trading_floor.logout_requested:
                trading_floor.logout_requested = False
                exit_prompt = True

        active_screen.draw(canvas)
        if exit_prompt:
            draw_exit_prompt(canvas)
        present(crt_effect.apply(canvas, elapsed), window)

    if login is not None:
        login.close()
    loading.close()
    if trading_floor is not None:
        trading_floor.close()
    pygame.quit()


if __name__ == "__main__":
    main()

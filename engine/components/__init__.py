"""Reusable on-screen components. Import what you need in scenes.py:

    from engine.components import Headline, kicker, appear, window, ChatTrack, ...
"""
from .headline import Headline, kicker
from .motion import appear, fade, typed, type_end, type_cues, stagger, count, fmt_id, wobble, bezier_partial
from .pill import chip, tag, word_pill, size_label, select_box, strike
from .chat import ChatTrack
from .widgets import stat, big_number, waveform, rec_bar, filmstrip, phone, comment, Cursor
from .recap import step_row, rule_box, connector, segments, follow_button, contact_pill
from . import window, icons
from .charts import (bill_counter, cost_chart, usage_meter, seat_grid, price_bars, day_timeline, block_split,
                     odometer, clock24, moon, receipt, stamp, note, chart_point)
from .infra import (particle_flow, toll_plaza, booth, car, arch_diagram, arch_node, load_graph, stack_layers,
                    slab_y, PURPLE)
from .migrate import (keycap, bookshelf, shelf_books, sync_pipe, twin_table, cutover_switch, padlock,
                      series_bumper, GREEN)
from .kitchen import (flame, burner, oven, order_ticket, ticket_rail, dag_flow, dag_state, lake_pantry,
                      server_rack, ORANGE)
from .blueprint import (bp_grid, bp_house, house_rooms, outline_text, dimension, phone_wire, city_map, TEAL)
from .payday import (tear_calendar, suspect_card, red_string, pin, cashier, queue_dots, ledger, paper_sheet,
                     torn_flight, RED)
from .tickets import big_clock, print_slip, dispenser, loket, refresh_icon, refresh_storm, GREEN as TICKET_GREEN
from .transit import route_strip, train, cert_card, save_button, station_dots, ORANGE as LINE_ORANGE
from .relay import qr_code, qris_stand, es_teh, relay_track, slowmo_badge, mesh_hub
from .kuliner import ruko, kios, flip_sign, flip_cues, gapura, visitor, walk_path, fade_ends, GREEN as KULINER_GREEN
from .kampung import kentongan, sound_rings, rumah, rumah_gede, gang, portal, ronda_man, TEAL as KAMPUNG_TEAL
from .cover import cover

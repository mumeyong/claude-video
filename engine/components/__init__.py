"""Reusable on-screen components. Import what you need in scenes.py:

    from engine.components import Headline, kicker, appear, window, ChatTrack, ...
"""
from .headline import Headline, kicker
from .motion import appear, fade, typed, type_end, type_cues, stagger, count, fmt_id, wobble, bezier_partial
from .pill import chip, tag, word_pill, size_label, select_box, strike
from .chat import ChatTrack
from .widgets import stat, big_number, waveform, rec_bar, filmstrip, phone, comment, Cursor
from .recap import step_row, rule_box, connector, segments, follow_button, contact_pill
from . import window, icons, material
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
from .badminton import (gpu_card, lapangan, pemain, shuttle, shuttle_arc, pelontar, rep_dots, jadwal, gor,
                        ORANGE as BADMINTON_ORANGE)
from .berkas import lembar, stopmap, meja_cs, bubble, profile_360, lapis, id_card, SOURCES, PURPLE as BERKAS_PURPLE
from .kuliner import ruko, kios, flip_sign, flip_cues, gapura, visitor, walk_path, fade_ends, GREEN as KULINER_GREEN
from .kampung import kentongan, sound_rings, rumah, rumah_gede, gang, portal, ronda_man, TEAL as KAMPUNG_TEAL
from .cover import cover
from .listrik import pulse_phase, rate_at, token_meter, stop_kontak, steker, alat, TEAL as LISTRIK_TEAL
from .brand import mumei_mark, brand_sting, brand_sting2, brand_intro, STING as BRAND_STING, STING2 as BRAND_STING2
from .fx import settle, land, squash, contact_shadow, ghost_trail
from .kinetic import (spring_p, spring_at, anticipate, Rig, motion_blur, drift, drifting, parallax, track_line,
                      mask_word, dim_color, dim_alpha, sheen, swap, lockup, curtain)
from .keynote import (Morph, bento, turn_at, yaw, press, sheet, ios_at, ios_dur, arrive, follow, presence, rise, wipe,
                      depth_swap, focus_pull, dolly, push, cut)
from .beats import (pop_tag, tag_center, check_badge, series_outro, heads, draw_heads, punch_word,
                    standard_outro)
from .wifi import modem, modem_led, led_state, fiber_route, route_point, patchcord, LEDS, ODP_F, PURPLE as WIFI_PURPLE
from .komplek import wifi_icon, pos_satpam, buku_alamat, ORANGE as KOMPLEK_ORANGE
from .pelabuhan import crane, peti_kemas, paket, kurir, GREEN as PORT_GREEN
from .loker import loker, loker_cell, kotak, kunci, centang, foto, TERRA as LOKER_TERRA
from .skilltree import branch, skill_tile, skill_tree, name_card, RED as TREE_RED
from .kuis import flip_card, countdown_ring, TEAL as KUIS_TEAL
from .tebak import keyboard_hp, suggest_bar, token_line, KB_RATIO, PURPLE as TEBAK_PURPLE
from .radio import on_air, mic_studio, slip, paku_nota, airwaves, data_center, ORANGE as RADIO_ORANGE
from .setrika import setrika, uap_panas, pembangkit, CORAL as SETRIKA_CORAL
from .hujan import hujan, tetes, odp_box, rumah_potong, rumah_geo, along, TEAL as HUJAN_TEAL
from .kasir import struk, struk_h, stempel, saklar, GREEN as KASIR_GREEN
from .panggung import panggung, panggung_geo, sorot, PURPLE as PANGGUNG_PURPLE
from .bukutamu import buku_tamu, buku_geo, RED as BUKU_RED
from .pdam import rusun_air, rusun_geo, aliran, pressure, TEAL as PDAM_TEAL
from .papan import papan_tulis, papan_geo, penghapus, memori, ORANGE as PAPAN_ORANGE
from .obrolan import chat_phone, chat_geo
from .kantorpos import amplop, belt, loket, hp_otp, hp_box, log_card, notif, GREEN as POS_GREEN
from .minimarket import rak, rak_geo, filler, produk, empty_spot, label_stok, tangan
from .reel import (smear, smear_p, out_p, smear_words, viewfinder, dot_gather, orbit, iris, pixel_wipe, highlight,
                   highlight_phrase, type_clip, reel_chip, float_chips, pill as reel_pill, count_pill, formula,
                   pop_card, tilt_plane, stat_panel, verb_slam, end_card, reel_sfx, ink_on, WORLDS as REEL_WORLDS)
from .craft import (pts_poly, pts_bezier, pts_circle, pts_rrect, pts_cairo, path_len, trim, path_point,
                    stroke_partial, draw_on, draw_chain, mark, split_rise, count_up, resample, morph_pair, morph_path,
                    path_at, shutter, carry, rack_cut)

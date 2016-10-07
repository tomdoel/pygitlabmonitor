import tkinter as tk

from pygitlabmonitor import settings
from pygitlabmonitor.color import Color

SELECTED_COLORS = [Color(178, 99, 0), Color(220, 36, 31), Color(255, 211, 41), Color(0, 125, 50), Color(244, 169, 190),
                   Color(161, 165, 167), Color(155, 0, 88), Color(0, 0, 0), Color(0, 25, 168), Color(0, 152, 216),
                   Color(147, 206, 186), Color(239, 123, 16), Color(0, 189, 25), Color(0, 175, 173),
                   Color(147, 100, 204), Color(0, 160, 226), Color(220, 36, 31)]


class MonitorFrame(tk.Frame):

    MAX_ROWS = 36
    FONT_SIZE = 30

    def __init__(self, root, project_cache):
        tk.Frame.__init__(self, root)

        self.project_cache = project_cache
        self._draw_table()

    def _draw_table(self):
        current_row = 0
        current_colour = 0

        status_list = self.project_cache.get_list_of_statuses()

        for status in status_list:
            if status.status:
                background_colour = SELECTED_COLORS[current_colour]
                text_colour = background_colour.get_contrast_colour()
                status_text = status.status
                if status_text == 'success':
                    status_text = 'OK'
                    status_text_color = 'red'
                else:
                    status_text_color = 'black'

                label_icon = tk.Label(self, image=status.icon, bg='white', width=5)
                label_icon.grid(row=current_row, column=0, sticky="ew", padx=5, pady=3)

                label_name = tk.Label(self, text=status.name, fg=text_colour.get_str(), bg=background_colour.get_str(),
                                      font=(settings.FONT, self.FONT_SIZE, "bold"), width=20)
                label_name.grid(row=current_row, column=1, sticky="nsew", padx=5, pady=3)

                label_status = tk.Label(self, text=status_text, fg=status_text_color, bg='floral white',
                                        font=(settings.FONT, self.FONT_SIZE, "bold"), width=20)
                label_status.grid(row=current_row, column=2, sticky="nsew", padx=5, pady=3)
                current_row += 1
                current_colour += 1
                if current_colour >= len(SELECTED_COLORS):
                        current_colour = 0

        self.pack(expand=1, fill="both")

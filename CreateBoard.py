def create_board_ui():
    global lbl_status, top_frame, list_labels
    top_frame = tk.Frame(window_main)
    for x in range(3):
        for y in range(3):
            lbl = tk.Label(top_frame, text=" ", font="Helvetica 45 bold", height=2, width=5, highlightbackground="grey",
                           highlightcolor="grey", highlightthickness=1)
            lbl.bind("<Button-1>", lambda e, xy=[x, y]: get_coordinate(xy))
            lbl.grid(row=x, column=y)

            dict_labels = {"xy": [x, y], "symbol": "", "label": lbl, "ticked": False}
            list_labels.append(dict_labels)

    lbl_status = tk.Label(top_frame, text="Status: Not connected to server", font="Helvetica 14 bold")
    lbl_status.grid(row=3, columnspan=3)

    top_frame.pack_forget()

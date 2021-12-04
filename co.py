def get_coordinate(xy):
    global client, your_turn
    # convert 2D to 1D cordinate i.e. index = x * num_cols + y
    label_index = xy[0] * num_cols + xy[1]
    label = list_labels[label_index]

    if your_turn:
        if label["ticked"] is False:
            label["label"].config(foreground=your_details["color"])
            label["label"]["text"] = your_details["symbol"]
            label["ticked"] = True
            label["symbol"] = your_details["symbol"]
            # send xy cordinate to server
            client.send("$xy$" + str(xy[0]) + "$" + str(xy[1]))
            your_turn = False

            # Does this play leads to a win or a draw
            result = game_logic()
            if result[0] is True and result[1] != "":  # a win
                your_details["score"] = your_details["score"] + 1
                lbl_status["text"] = "Game over, You won! You(" + str(your_details["score"]) + ") - " \
                    "" + opponent_details["name"] + "(" + str(opponent_details["score"]) + ")"
                lbl_status.config(foreground="green")
                threading._start_new_thread(init, ("", ""))

            elif result[0] is True and result[1] == "":  # a draw
                lbl_status["text"] = "Game over, Draw! You(" + str(your_details["score"]) + ") - " \
                    "" + opponent_details["name"] + "(" + str(opponent_details["score"]) + ")"
                lbl_status.config(foreground="blue")
                threading._start_new_thread(init, ("", ""))

            else:
                lbl_status["text"] = "STATUS: " + opponent_details["name"] + "'s turn!"
    else:
        lbl_status["text"] = "STATUS: Wait for your turn!"
        lbl_status.config(foreground="red")

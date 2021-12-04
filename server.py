def receive_message_from_server(sck, m):
    global your_details, opponent_details, your_turn, you_started
    while True:
        from_server = sck.recv(4096)

        if not from_server: break

        if from_server.startswith("welcome"):
            if from_server == "welcome1":
                your_details["color"] = "purple"
                opponent_details["color"] = "orange"
                lbl_status["text"] = "Server: Welcome " + your_details["name"] + "! Waiting for player 2"
            elif from_server == "welcome2":
                lbl_status["text"] = "Server: Welcome " + your_details["name"] + "! Game will start soon"
                your_details["color"] = "orange"
                opponent_details["color"] = "purple"

        elif from_server.startswith("opponent_name$"):
            temp = from_server.replace("opponent_name$", "")
            temp = temp.replace("symbol", "")
            name_index = temp.find("$")
            symbol_index = temp.rfind("$")
            opponent_details["name"] = temp[0:name_index]
            your_details["symbol"] = temp[symbol_index:len(temp)]

            # set opponent symbol
            if your_details["symbol"] == "O":
                opponent_details["symbol"] = "X"
            else:
                opponent_details["symbol"] = "O"

            lbl_status["text"] = "STATUS: " + opponent_details["name"] + " is connected!"
            sleep(3)
            # is it your turn to play? hey! 'O' comes before 'X'
            if your_details["symbol"] == "O":
                lbl_status["text"] = "STATUS: Your turn!"
                your_turn = True
                you_started = True
            else:
                lbl_status["text"] = "STATUS: " + opponent_details["name"] + "'s turn!"
                you_started = False
                your_turn = False
        elif from_server.startswith("$xy$"):
            temp = from_server.replace("$xy$", "")
            _x = temp[0:temp.find("$")]
            _y = temp[temp.find("$") + 1:len(temp)]

            # update board
            label_index = int(_x) * num_cols + int(_y)
            label = list_labels[label_index]
            label["symbol"] = opponent_details["symbol"]
            label["label"]["text"] = opponent_details["symbol"]
            label["label"].config(foreground=opponent_details["color"])
            label["ticked"] = True

            # Does this coordinate leads to a win or a draw
            result = game_logic()
            if result[0] is True and result[1] != "":  # opponent win
                opponent_details["score"] = opponent_details["score"] + 1
                if result[1] == opponent_details["symbol"]:  #
                    lbl_status["text"] = "Game over, You Lost! You(" + str(your_details["score"]) + ") - " \
                        "" + opponent_details["name"] + "(" + str(opponent_details["score"]) + ")"
                    lbl_status.config(foreground="red")
                    threading._start_new_thread(init, ("", ""))
            elif result[0] is True and result[1] == "":  # a draw
                lbl_status["text"] = "Game over, Draw! You(" + str(your_details["score"]) + ") - " \
                    "" + opponent_details["name"] + "(" + str(opponent_details["score"]) + ")"
                lbl_status.config(foreground="blue")
                threading._start_new_thread(init, ("", ""))
            else:
                your_turn = True
                lbl_status["text"] = "STATUS: Your turn!"
                lbl_status.config(foreground="black")
    sck.close()

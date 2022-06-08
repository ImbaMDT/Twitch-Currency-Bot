## Ping Art 1

    def check_for_ping(self, data, kind):
        last_ping = time.time()
        if data.find("PING") != -1:
            self.sock[kind].send("PONG " + data.split()[1] + "\r\n")
            last_ping = time.time()
        if (time.time() - last_ping) > threshold:
            sys.exit()
			
			
##########################

## Ping Art 2

            # So twitch doesn't timeout the bot.
            if "PING" in line and Console(line):
                msgg = "PONG tmi.twitch.tv\r\n".encode()
                s.send(msgg)
                print(msgg)
                break
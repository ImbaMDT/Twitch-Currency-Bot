import socket
import sqlite3
import time

HOST = "irc.twitch.tv"
PORT = 6667
NICK = "<channel auf dem connected wird"
PASS = 'oauth key'

# Tabellen und Datenbank erzeugen falls nicht vorhanden
connection = sqlite3.connect('twitchcurrency.db')
cursor = connection.cursor()

kontoTable = 'CREATE TABLE IF NOT EXISTS kontoTable(name text,points INTEGER)'
cursor.execute(kontoTable)

bargeldTable = 'CREATE TABLE IF NOT EXISTS bargeldTable(name text,points INTEGER)'
cursor.execute(bargeldTable)
def whisper(message):
    s.send(bytes ("PRIVMSG #jtv :.w " + username + " " + message + "\r\n", "UTF-8"))

def send_message(message):
    s.send(bytes("PRIVMSG #" + NICK + " :" + message + "\r\n", "UTF-8"))

def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)

def kontoAnlegen(message):
    cursor.execute('SELECT * FROM kontoTable WHERE name=?',(username,))

    entryKonto = cursor.fetchone()

    if entryKonto is None:
        cursor.execute('INSERT INTO kontoTable VALUES (?,?)', (username,0))
        connection.commit()
        send_message(username + ' dein Konto wurde angelegt!')
    else:
        print('')


    cursor.execute('SELECT * FROM bargeldTable WHERE name=?',(username,))

    entryBargeld = cursor.fetchone()

    if entryBargeld is None:
        cursor.execute('INSERT INTO bargeldTable VALUES (?,?)', (username,0))
        connection.commit()
        print( username + ' angelegt')
    else:
        print('')

def abheben(message):

    kontoAnlegen(message)
    
    Betrag = int(parts[2].split()[1])
    
    pointsKonto = cursor.execute('SELECT points FROM kontoTable WHERE name=?', (username,))

    for k in pointsKonto:
        kontostand = k[0]



    pointsBargeld = cursor.execute('SELECT points FROM bargeldTable WHERE name=?', (username,))
    
    for b in pointsBargeld:
        bargeld = b[0]

    if Betrag <= kontostand:
        

        neuKontostand = kontostand-Betrag
        neuBargeld = bargeld+Betrag


        cursor.execute("UPDATE kontoTable SET points=? WHERE name=?", (neuKontostand,username))
        cursor.execute("UPDATE bargeldTable SET points=? WHERE name=?", (neuBargeld,username))
        connection.commit()
        whisper(str(Betrag) +' Berry erfolgreich ausgezahlt.' )
    else:
        send_message('Du hast nicht so viel Geld auf dem Konto')


def einzahlen(message):
    kontoAnlegen(message)
    
    Betrag = int(parts[2].split()[1])
    
    ##### Kontostand und Bargeldstand auslesen ####
    pointsKonto = cursor.execute('SELECT points FROM kontoTable WHERE name=?', (username,))

    for k in pointsKonto:
        kontostand = k[0]



    pointsBargeld = cursor.execute('SELECT points FROM bargeldTable WHERE name=?', (username,))
    
    for b in pointsBargeld:
        bargeld = b[0]





    if Betrag <= bargeld:
        

        neuKontostand = kontostand+Betrag
        neuBargeld = bargeld-Betrag


        cursor.execute("UPDATE kontoTable SET points=? WHERE name=?", (neuKontostand,username))
        cursor.execute("UPDATE bargeldTable SET points=? WHERE name=?", (neuBargeld,username))
        connection.commit()
        whisper(str(Betrag) + ' Berry erfolgreich eingezahlt. Neuer Kontostand: ' + str(neuKontostand) + ' Berry.')
        
        
    else:
        send_message('So viel Bargeld hast du nicht ' + username)

    

def senden(message):
    

    kontoAnlegen(message)

    user = str(parts[2].split()[2])
    Betrag = int(parts[2].split()[1])

    # Pruefen ob Empfaenger existiert

    cursor.execute('SELECT * FROM kontoTable WHERE name=?',(user,))

    entrySenden = cursor.fetchone()

    if entrySenden is None:
        send_message('Der Empfaenger hat kein Konto oder du hast !senden <Betrag> <Empfaenger> falsch genutzt.')

    else:

        #bargeld des senders
        bargeldSender = cursor.execute('SELECT points FROM bargeldTable WHERE name=?', (username,))

        for s in bargeldSender:
            S = s[0]

        # Bargeld des empfaengers
        bargeldEmpfang = cursor.execute('SELECT points FROM bargeldTable WHERE name=?', (user,))

        for b in bargeldEmpfang:
            B = b[0]
        
            

        if Betrag <= S:
            
    # Bargeld vom Sender Updaten
            cursor.execute("UPDATE bargeldTable SET points=? WHERE name=?", (S-Betrag,username))
    # Bargeld vom Empfaenger updaten
            cursor.execute("UPDATE bargeldTable SET points=? WHERE name=?", (B+Betrag,user))

            connection.commit()
            send_message(str(Betrag) + ' Berry an ' + user + ' gesendet.')
        else:
            send_message('So viel Bargeld hast du nicht ' + username)




s = socket.socket()
if True:
    s.connect((HOST, PORT))
    s.send(bytes("PASS " + PASS + "\r\n", "UTF-8"))
    s.send(bytes("NICK " + NICK + "\r\n", "UTF-8"))
    s.send(bytes("JOIN #" + NICK + " \r\n", "UTF-8"))
    print("Erfolgreiche Verbindung zu Channel " + NICK)
else:
    print("Fehler")

while True:
    line = str(s.recv(1024))
    if "End of /NAMES list" in line:
        break

while True:



    for line in str(s.recv(1024)).split('\\r\\n'):
        parts = line.split(':')
        if len(parts) < 3:
            continue

        if "QUIT" not in parts[1] and "JOIN" not in parts[1] and "PART" not in parts[1]:
            message = parts[2][:len(parts[2])]


        usernamesplit = parts[1].split("!")
        username = usernamesplit[0]

        print(username + ": " + message)
        if message == "Hey ":
            send_message("Welcome to my stream, " + username)
            print(parts[2])

        if message == "exit":
            s.shutdown()

##############     COMMAND SECTION  ########################
        # zahlt ein
        if "!einzahlen" in parts[2]:
            if hasNumbers(parts[2]) == True:
                
                einzahlen(message)

            else:

                send_message("Du hast keinen Betrag angegeben " + username)


        # hebt Geld vom Konto ab 
        if "!abheben" in parts[2]:
            if hasNumbers(parts[2]) == True:
                
                abheben(message)

            else:
                send_message("Du hast keinen Betrag angegeben " + username)


        # Geld senden
        if "!senden" in parts[2]:
            if hasNumbers(parts[2]) == True:
               senden(message)
        
            else:
                send_message('!senden <Betrag> <Empfaenger>')


        # Kontostand checken
        if message == "!konto":
            kontoAnlegen(message)
            kontostand = cursor.execute('SELECT points FROM kontoTable WHERE name=?', (username,))
            for i in kontostand:
                i

            points = i[0]
            send_message(str(points) + ' Berry')
            
        # Bargeld checken
        if message == '!bargeld':
            bargeldstand = cursor.execute('SELECT points FROM bargeldTable WHERE name=?', (username,))
            for b in bargeldstand:
                b

            points = b[0]
            send_message(str(points) + ' Berry')
                
            
            
# http://tmi.twitch.tv/group/user/s0pht/chatters
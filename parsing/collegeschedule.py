# Schedule is hard coded in the writeGameInsert function
#NOTES: Change the following team names
# :%s/Unlv/UNLV/g
# :%s/Miami (fl)/Miami
# Usc USC
# Ucla #UCLA
# m Rattlers
# m Aggies
# m Panthers
# Utep, Tcu, Lsu, Ucf, Uab, Utep,
# (Oh), (OH)
from BeautifulSoup import BeautifulSoup
import dateutil.parser, re, urllib2, time

def main():
    results = open('college_schedule.sql', 'w+')

    for week in range(2,15):
        soup = getsoup(week)

        tables = getgametables(soup)
        for table in tables:
            gamedate = getgamedate(table)
            games = getGamesByDate(table)

            for game in games:
                writeGameInsert(gamedate, game, results, week)

    results.close()

def convert_to_local_time(dt_aware):
    tz = pytz.timezone('America/New_York') # Replace this with your time zone string
    dt_my_tz = dt_aware.astimezone(tz)
    dt_naive = dt_my_tz.replace(tzinfo=None)
    return dt_naive

def writeGameInsert(gd, game, results, week):
    # gd is the game date string from the table header
    # the game time is in the first cell

    if game == []:
        return
    gameTime = game.td.contents[0]
    if gameTime == 'TBA':
        gameTime = '12:00 PM ET'

    gamedate = dateutil.parser.parse(gameTime + ' -0400 ' + gd)
    away, home = getteams(game)
    print week, away, home, gamedate

    results.write("select game_insert('2013-2014', %s, '%s', '%s', 0.0, " \
                  "0.0, '%s', 'Ncaagame');\n" % (week, home, away, time.strftime("%Y-%m-%d %H:%M:%S", gamedate.utctimetuple())))


def getteams(game):
    # there are 5 links in each game.  The first two
    # hold the team links, the first is away, the second is home.
    links = game.findAll("a")
    away = getTeam(links[0])
    home = getTeam(links[1])
    return away, home

def getTeam(link):
    # form : http://espn.go.com/college-football/team/_/id/99/lsu-tigers
    teamData = link['href'].split('/')[-1].split('-')
    team = ''
    for x in teamData:
        team += x.capitalize() + ' '

    return team.strip()

def getGamesByDate(table):
    evengames = table.findAll(attrs={'class' : re.compile('evenrow.+')})
    oddgames = table.findAll(attrs={'class' : re.compile('oddrow.+')})
    games = evengames
    for result in oddgames:
        games.append(result)

    return games

def getgamedate(table):
    # Comes in the format of Tuesday, November 22
    return table.tr.td.contents[0]

def getgametables(soup):
    return soup.findAll("table", {"class" : "tablehead"})

def getsoup(week):
    f = urllib2.urlopen("http://espn.go.com/college-football/schedule/_/week/"
            + str(week))
    soup = BeautifulSoup(f.read())
    f.close()
    return soup


if __name__ == '__main__':
    main()

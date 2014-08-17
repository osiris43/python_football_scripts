#  This script will parse the schedule from ESPN as long as they don't change
#  their format. Before running, change the year at the top and the date range
#  at the bottom.
#  Also, once the file has been written, the following modifications
#  have to be made:
#
#   1.  Change New York Giants and New York Jets to New York

from BeautifulSoup import BeautifulSoup
import time
from dateutil.parser import parse

globalyear = 2014
schedule = {}
mascots = {'Washington':'Redskins', 'New York Giants':'Giants',
           'Tampa Bay':'Buccaneers', 'New Orleans':'Saints',
           'St. Louis':'Rams', 'Philadelphia':'Eagles',
           'New York Jets':'Jets', 'Miami':'Dolphins',
           'Kansas City':'Chiefs', 'New England':'Patriots',
           'Houston':'Texans', 'Pittsburgh':'Steelers',
           'Cincinnati':'Bengals', 'Baltimore':'Ravens',
           'Detroit':'Lions', 'Atlanta':'Falcons',
           'Seattle':'Seahawks', 'Buffalo':'Bills',
           'Jacksonville':'Jaguars', 'Tennessee':'Titans',
           'Dallas':'Cowboys', 'Cleveland':'Browns',
           'Carolina':'Panthers', 'San Diego':'Chargers',
           'Arizona':'Cardinals', 'San Francisco':'49ers',
           'Chicago':'Bears', 'Indianapolis':'Colts',
           'Minnesota':'Vikings', 'Green Bay':'Packers',
           'Denver':'Broncos', 'Oakland':'Raiders'}


class Game(object):
  def __init__(self, week, away, away_mascot, home, home_mascot, city, date):
    self.week = week
    self.away = away
    self.away_mascot = away_mascot
    self.home = home
    self.home_mascot = home_mascot
    self.city = city
    self.gamedate = date

def main():
  f = open('2014_preseason_week1.html', 'r+')
  soup = BeautifulSoup(f.read())
  weektables = get_weektables(soup)
  get_weeks(weektables)
  write_file()

def get_weeks(weektables):

  for table in weektables:
    games = []
    rows = table.findAll('tr')

    for row in rows:
      if len(row.attrs):
        rowtype = row.attrs[0][1]
      else:
        continue
      print rowtype

      if rowtype == 'stathead':
        week = row.td.contents[1].string.split(' ')[1]
      elif rowtype == 'colhead':
        date_string = row.find('td', {'width': '170'}).string
      elif len(rowtype.split(' ')) > 1:
        print row.td

        game = process_row(row, week, date_string)
        games.append(game)

    print len(games)
    schedule[week] = games


def process_row(row, week, date_string):
  print week, date_string
  cells = row.findAll('td')
  teamsWithLinks = row.td.findAll('a')
  away = teamsWithLinks[0].contents[0].replace('NY', 'New York')
  home = teamsWithLinks[1].contents[0].replace('NY', 'New York')

  print away, home
  time = cells[1].string
  gamedate = parse(time + " EST -0400 " + date_string)
  #gamedate = parse(' '.join([date_string, time]))
  print gamedate
  g = Game(week, away, mascots[away], home, mascots[home], home, gamedate)
  return g

def get_weektables(soup):
  weeks = soup.findAll('table' , {'class' : 'tablehead'})
  print 'number of weeks: %s' % len(weeks)
  return weeks

def write_file():
  results = open('results.txt', 'w+')

  for k,v in schedule.iteritems():
    for game in v:
      # the first line creates a schedule for MS Sql, the old Pool of greatness.
      # The second creates one for Sports Pool Paradise.
      #results.write("exec GameINS %s, %s, '%s', '%s', '%s', '%s', '%s', '%s'\n" %
      #              (globalyear, k,game.gamedate, game.city, game.home, game.home_mascot, game.away, game.away_mascot))
      results.write("select game_insert('2014-2015', %s, '%s %s', '%s %s', 0.0, 0.0, '%s', 'Nflgame');\n" %
                    (k, game.home, game.home_mascot, game.away, game.away_mascot, time.strftime("%Y-%m-%dT%H:%M:%S", game.gamedate.utctimetuple())))

  results.close()

if __name__ == '__main__':
  main()

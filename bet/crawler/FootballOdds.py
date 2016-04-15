__author__ = 'tintsing'
from SportsOdds import SportsOdds


class FootballOdds (SportsOdds):
    def __init__(self):
        super(FootballOdds, self).__init__()

        self.host_rank = -1
        self.away_rank = -1


    def __unicode__(self):
        str = u'%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' % (self.league, self.start_time, self.host,
                self.away, self.host_rank, self.away_rank, self.let_odd_1, self.let_odd_2, self.let_condition,
                self.win_odd, self.draw_odd, self.lose_odd, self.host_score, self.away_score)
        return str



